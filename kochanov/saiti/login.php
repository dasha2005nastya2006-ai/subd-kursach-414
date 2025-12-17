<?php
// login.php
session_start();
require_once 'config.php';
require_once 'auth.php';

$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    
    if (empty($email) || empty($password)) {
        $error = 'Заполните все поля';
    } else {
        $result = loginUser($pdo, $email, $password);
        if ($result['success']) {
            header('Location: index.php');
            exit;
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
    <title>Вход - Система управления арендой</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        .login-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .login-header {
            background: linear-gradient(135deg, #4a6fa5 0%, #2c3e50 100%);
            color: white;
            border-radius: 20px 20px 0 0;
            padding: 30px;
        }
        .login-footer {
            border-top: 1px solid #eee;
            padding-top: 20px;
            margin-top: 20px;
        }
        .btn-login {
            background: linear-gradient(135deg, #4a6fa5 0%, #2c3e50 100%);
            border: none;
            padding: 12px;
            font-weight: 600;
        }
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="login-card">
                    <div class="login-header text-center">
                        <i class="fas fa-database fa-3x mb-3"></i>
                        <h2>Система управления арендой</h2>
                        <p class="mb-0">Войдите в свой аккаунт</p>
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
                        
                        <form method="POST" action="">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-envelope"></i>
                                    </span>
                                    <input type="email" name="email" class="form-control" 
                                           placeholder="admin@agency.ru" required autofocus>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Пароль</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-lock"></i>
                                    </span>
                                    <input type="password" name="password" class="form-control" 
                                           placeholder="Ваш пароль" required>
                                </div>
                            </div>
                            
                            <div class="d-grid gap-2 mb-3">
                                <button type="submit" class="btn btn-login text-white">
                                    <i class="fas fa-sign-in-alt me-2"></i>Войти
                                </button>
                            </div>
                            
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" name="remember" id="remember">
                                <label class="form-check-label" for="remember">
                                    Запомнить меня
                                </label>
                            </div>
                        </form>
                        
                        <div class="login-footer text-center">
                            <p class="mb-2">Демо доступ:</p>
                            <div class="row g-2">
                                <div class="col-6">
                                    <div class="card border-primary">
                                        <div class="card-body p-2">
                                            <small class="text-muted">Админ</small>
                                            <p class="mb-0"><strong>admin@agency.ru</strong></p>
                                            <small class="text-muted">admin123</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="card border-success">
                                        <div class="card-body p-2">
                                            <small class="text-muted">Менеджер</small>
                                            <p class="mb-0"><strong>manager@agency.ru</strong></p>
                                            <small class="text-muted">manager123</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-4 text-white">
                    <p>Нет аккаунта? <a href="register.php" class="text-white fw-bold">Зарегистрироваться</a></p>
                    <p class="small">
                        <i class="fas fa-info-circle me-1"></i>
                        Тестовые данные загружены автоматически
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
