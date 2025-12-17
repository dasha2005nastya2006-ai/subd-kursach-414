<?php
// auth.php - Функции для аутентификации

// Регистрация нового пользователя
function registerUser($pdo, $email, $password, $firstName, $lastName, $phone, $role = 'guest') {
    try {
        // Проверка существования email
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE email = ?");
        $stmt->execute([$email]);
        if ($stmt->fetchColumn() > 0) {
            return ['success' => false, 'message' => 'Email уже зарегистрирован'];
        }

        // Хеширование пароля
        $passwordHash = password_hash($password, PASSWORD_BCRYPT);
        
        // Начало транзакции
        $pdo->beginTransaction();
        
        // Вставка в users
        $stmt = $pdo->prepare("
            INSERT INTO users (email, password_hash, role, phone, email_verified, created_at) 
            VALUES (?, ?, ?, ?, false, NOW())
            RETURNING user_id
        ");
        $stmt->execute([$email, $passwordHash, $role, $phone]);
        $userId = $stmt->fetchColumn();
        
        // Если роль guest - создаем запись в guest
        if ($role === 'guest') {
            $stmt = $pdo->prepare("
                INSERT INTO guest (user_id, first_name, last_name, email, phone, created_at)
                VALUES (?, ?, ?, ?, ?, NOW())
            ");
            $stmt->execute([$userId, $firstName, $lastName, $email, $phone]);
        }
        
        // Если роль employee - создаем запись в employee
        if ($role === 'employee' || $role === 'admin' || $role === 'cleaner') {
            $stmt = $pdo->prepare("
                INSERT INTO employee (user_id, first_name, last_name, position, hire_date, department)
                VALUES (?, ?, ?, 'Новый сотрудник', NOW(), 'general')
            ");
            $stmt->execute([$userId, $firstName, $lastName]);
        }
        
        $pdo->commit();
        
        return ['success' => true, 'user_id' => $userId];
        
    } catch (Exception $e) {
        $pdo->rollBack();
        return ['success' => false, 'message' => 'Ошибка регистрации: ' . $e->getMessage()];
    }
}

// Вход пользователя
function loginUser($pdo, $email, $password) {
    try {
        $stmt = $pdo->prepare("
            SELECT user_id, email, password_hash, role, is_active 
            FROM users 
            WHERE email = ?
        ");
        $stmt->execute([$email]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if (!$user) {
            return ['success' => false, 'message' => 'Пользователь не найден'];
        }
        
        if (!$user['is_active']) {
            return ['success' => false, 'message' => 'Аккаунт деактивирован'];
        }
        
        if (!password_verify($password, $user['password_hash'])) {
            return ['success' => false, 'message' => 'Неверный пароль'];
        }
        
        // Обновляем время последнего входа
        $stmt = $pdo->prepare("UPDATE users SET last_login = NOW() WHERE user_id = ?");
        $stmt->execute([$user['user_id']]);
        
        // Создаем сессию
        $_SESSION['user_id'] = $user['user_id'];
        $_SESSION['email'] = $user['email'];
        $_SESSION['role'] = $user['role'];
        $_SESSION['logged_in'] = true;
        
        // Логируем вход
        logAction($pdo, $user['user_id'], 'login', 'user', $user['user_id']);
        
        return ['success' => true, 'role' => $user['role']];
        
    } catch (Exception $e) {
        return ['success' => false, 'message' => 'Ошибка входа: ' . $e->getMessage()];
    }
}

// Выход пользователя
function logoutUser($pdo) {
    if (isset($_SESSION['user_id'])) {
        logAction($pdo, $_SESSION['user_id'], 'logout', 'user', $_SESSION['user_id']);
    }
    session_destroy();
    session_start(); // Начинаем новую сессию для возможных сообщений
}

// Проверка авторизации
function isLoggedIn() {
    return isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true;
}

// Проверка роли
function hasRole($role) {
    return isset($_SESSION['role']) && $_SESSION['role'] === $role;
}

// Получить информацию о текущем пользователе
function getCurrentUser($pdo) {
    if (!isset($_SESSION['user_id'])) {
        return null;
    }
    
    try {
        $stmt = $pdo->prepare("
            SELECT u.*, 
                   COALESCE(g.first_name, e.first_name) as first_name,
                   COALESCE(g.last_name, e.last_name) as last_name
            FROM users u
            LEFT JOIN guest g ON u.user_id = g.user_id
            LEFT JOIN employee e ON u.user_id = e.user_id
            WHERE u.user_id = ?
        ");
        $stmt->execute([$_SESSION['user_id']]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        return null;
    }
}

// Логирование действий
function logAction($pdo, $userId, $action, $entityType = null, $entityId = null) {
    try {
        $stmt = $pdo->prepare("
            INSERT INTO audit_log (user_id, action, entity_type, entity_id, ip_address, user_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, NOW())
        ");
        $stmt->execute([
            $userId,
            $action,
            $entityType,
            $entityId,
            $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
        ]);
    } catch (Exception $e) {
        // Безопасно игнорируем ошибки логирования
    }
}
?>
