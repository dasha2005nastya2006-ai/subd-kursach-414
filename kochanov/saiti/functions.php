<?php
// functions.php - основные функции

// Проверка существования таблицы
function tableExists($pdo, $tableName) {
    $stmt = $pdo->query("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$tableName')");
    return $stmt->fetchColumn();
}

// Получить все таблицы
function getAllTables($pdo) {
    $stmt = $pdo->query("
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name
    ");
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

// Получить структуру таблицы
function getTableStructure($pdo, $tableName) {
    $stmt = $pdo->prepare("
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = ?
        ORDER BY ordinal_position
    ");
    $stmt->execute([$tableName]);
    return $stmt->fetchAll();
}

// Получить данные из таблицы
function getTableData($pdo, $tableName, $limit = 100) {
    // Проверка валидности имени таблицы
    if (!preg_match('/^[a-zA-Z_][a-zA-Z0-9_]*$/', $tableName)) {
        throw new Exception('Некорректное имя таблицы');
    }
    
    $stmt = $pdo->prepare("SELECT * FROM \"$tableName\" LIMIT ?");
    $stmt->bindValue(1, $limit, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Получить количество записей
function getRowCount($pdo, $tableName) {
    $stmt = $pdo->query("SELECT COUNT(*) FROM $tableName");
    return $stmt->fetchColumn();
}

// Выполнить произвольный SQL
function executeSQL($pdo, $sql) {
    // Запрещенные операции для обычных пользователей
    $forbidden = [
        'DROP', 'TRUNCATE', 'DELETE FROM', 'ALTER TABLE', 
        'CREATE TABLE', 'GRANT', 'REVOKE'
    ];
    
    $currentRole = $_SESSION['role'] ?? 'guest';
    
    if ($currentRole !== 'admin') {
        foreach ($forbidden as $keyword) {
            if (stripos($sql, $keyword) !== false) {
                return ['error' => 'Данная операция доступна только администраторам'];
            }
        }
    }
    
    try {
        // Ограничение на количество возвращаемых строк для SELECT
        if (stripos(trim($sql), 'SELECT') === 0) {
            // Добавляем LIMIT если его нет
            if (stripos($sql, 'LIMIT') === false) {
                $sql .= ' LIMIT 1000';
            }
        }
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        
        if (stripos($sql, 'SELECT') === 0) {
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } else {
            return ['affected_rows' => $stmt->rowCount()];
        }
    } catch (PDOException $e) {
        return ['error' => $e->getMessage()];
    }
}
?>
