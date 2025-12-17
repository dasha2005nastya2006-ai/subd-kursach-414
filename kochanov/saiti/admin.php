<?php
session_start();
require_once 'config.php';
require_once 'auth.php';

if (!isLoggedIn() || !hasRole('admin')) {
    header('Location: login.php');
    exit;
}

$currentUser = getCurrentUser($pdo);
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Админ-панель</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <?php include 'navbar.php'; ?>
    
    <div class="container mt-4">
        <h2><i class="fas fa-crown me-2"></i>Административная панель</h2>
        
        <div class="row mt-4">
            <div class="col-md-4 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-users fa-3x text-primary mb-3"></i>
                        <h5>Пользователи</h5>
                        <a href="?table=users" class="btn btn-primary mt-2">Управление</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-cogs fa-3x text-success mb-3"></i>
                        <h5>Настройки</h5>
                        <a href="?table=site_setting" class="btn btn-success mt-2">Настроить</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-chart-line fa-3x text-warning mb-3"></i>
                        <h5>Отчеты</h5>
                        <a href="stats.php" class="btn btn-warning mt-2">Смотреть</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
