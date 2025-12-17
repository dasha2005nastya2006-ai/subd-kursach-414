<?php
// register.php
session_start();
require_once 'config.php';
require_once 'auth.php';

$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $confirmPassword = $_POST['confirm_password'] ?? '';
    $firstName = trim($_POST['first_name'] ?? '');
    $lastName = trim($_POST['last_name'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $role = $_POST['role'] ?? 'guest';
    
    // Валидация
    if (empty($email) || empty($password) || empty($firstName) || empty($lastName) || empty($phone)) {
        $error = 'Заполните все обязательные поля';
    } elseif ($password !== $confirmPassword) {
        $error = 'Пароли не совпадают';
    } elseif (strlen($password) < 6) {
        $error = 'Пароль должен быть не менее 6 символов';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = 'Некорректный email';
    } else {
        $result = registerUser($pdo, $email, $password, $firstName, $lastName, $phone, $role);
        if ($result['success']) {
            $success = 'Регистрация успешна! Теперь вы можете войти.';
            // Очищаем поля после успешной регистрации
            $_POST = [];
        } else {
            $error = $result['message'];
        }
    }
}

// Если уже авторизован - перенаправляем
if (isLoggedIn()) {
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация - Система управления арендой</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        .register-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .register-header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 20px 20px 0 0;
            padding: 30px;
        }
        .btn-register {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            padding: 12px;
            font-weight: 600;
        }
        .btn-register:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .password-strength {
            height: 5px;
            margin-top: 5px;
            border-radius: 3px;
            transition: all 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="register-card">
                    <div class="register-header text-center">
                        <i class="fas fa-user-plus fa-3x mb-3"></i>
                        <h2>Регистрация в системе</h2>
                        <p class="mb-0">Создайте новый аккаунт</p>
                    </div>
                    
                    <div class="card-body p-5">
                        <?php if ($error): ?>
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <?= htmlspecialchars($error) ?>
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        <?php endif; ?>
                        
                        <?php if ($success): ?>
                            <div class="alert alert-success alert-dismissible fade show" role="alert">
                                <?= htmlspecialchars($success) ?>
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        <?php endif; ?>
                        
                        <form method="POST" action="" id="registerForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Имя *</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="fas fa-user"></i>
                                        </span>
                                        <input type="text" name="first_name" class="form-control" 
                                               value="<?= htmlspecialchars($_POST['first_name'] ?? '') ?>"
                                               placeholder="Иван" required>
                                    </div>
                                </div>
                                
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Фамилия *</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="fas fa-user"></i>
                                        </span>
                                        <input type="text" name="last_name" class="form-control" 
                                               value="<?= htmlspecialchars($_POST['last_name'] ?? '') ?>"
                                               placeholder="Иванов" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Email *</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-envelope"></i>
                                    </span>
                                    <input type="email" name="email" class="form-control" 
                                           value="<?= htmlspecialchars($_POST['email'] ?? '') ?>"
                                           placeholder="ivan@example.com" required>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Телефон *</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-phone"></i>
                                    </span>
                                    <input type="tel" name="phone" class="form-control" 
                                           value="<?= htmlspecialchars($_POST['phone'] ?? '') ?>"
                                           placeholder="+79161234567" required>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Пароль *</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="fas fa-lock"></i>
                                        </span>
                                        <input type="password" name="password" id="password" 
                                               class="form-control" placeholder="Не менее 6 символов" required>
                                    </div>
                                    <div class="password-strength" id="passwordStrength"></div>
                                </div>
                                
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Подтвердите пароль *</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="fas fa-lock"></i>
                                        </span>
                                        <input type="password" name="confirm_password" 
                                               class="form-control" placeholder="Повторите пароль" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Роль</label>
                                <select name="role" class="form-select">
                                    <option value="guest" <?= ($_POST['role'] ?? 'guest') === 'guest' ? 'selected' : '' ?>>Гость (арендатор)</option>
                                    <option value="employee" <?= ($_POST['role'] ?? '') === 'employee' ? 'selected' : '' ?>>Сотрудник</option>
                                    <option value="cleaner" <?= ($_POST['role'] ?? '') === 'cleaner' ? 'selected' : '' ?>>Уборщик</option>
                                </select>
                                <small class="text-muted">Администратора может создать только существующий администратор</small>
                            </div>
                            
                            <div class="mb-3 form-check">
                                <input type="checkbox" class="form-check-input" id="terms" required>
                                <label class="form-check-label" for="terms">
                                    Я согласен с <a href="#" data-bs-toggle="modal" data-bs-target="#termsModal">условиями использования</a>
                                </label>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-register text-white">
                                    <i class="fas fa-user-plus me-2"></i>Зарегистрироваться
                                </button>
                                <a href="login.php" class="btn btn-outline-secondary">
                                    <i class="fas fa-sign-in-alt me-2"></i>Уже есть аккаунт? Войти
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Модальное окно с условиями -->
    <div class="modal fade" id="termsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Условия использования</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p><strong>Система управления арендой квартир</strong></p>
                    <p>1. Регистрируясь в системе, вы соглашаетесь на обработку ваших персональных данных</p>
                    <p>2. Вы обязуетесь использовать систему только в законных целях</p>
                    <p>3. Администрация оставляет за собой право блокировать аккаунты за нарушения</p>
                    <p>4. Вы несете ответственность за безопасность своих учетных данных</p>
                    <p>5. Система предназначена для управления процессами аренды недвижимости</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Проверка сложности пароля
        document.getElementById('password').addEventListener('input', function(e) {
            const password = e.target.value;
            const strengthBar = document.getElementById('passwordStrength');
            
            let strength = 0;
            if (password.length >= 6) strength++;
            if (password.length >= 8) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;
            
            const colors = ['#dc3545', '#ffc107', '#28a745'];
            const texts = ['Слабый', 'Средний', 'Сильный'];
            
            strengthBar.style.width = ((strength / 5) * 100) + '%';
            strengthBar.style.backgroundColor = colors[Math.min(2, Math.floor(strength / 2))];
            
            // Показываем подсказку
            strengthBar.title = texts[Math.min(2, Math.floor(strength / 2))];
        });
        
        // Проверка совпадения паролей
        document.getElementById('registerForm').addEventListener('submit', function(e) {
            const password = document.querySelector('input[name="password"]').value;
            const confirm = document.querySelector('input[name="confirm_password"]').value;
            
            if (password !== confirm) {
                e.preventDefault();
                alert('Пароли не совпадают!');
                return false;
            }
            
            if (password.length < 6) {
                e.preventDefault();
                alert('Пароль должен быть не менее 6 символов');
                return false;
            }
        });
    </script>
</body>
</html>
