<?php
session_start();
require_once 'config.php';
require_once 'auth.php';

if (!isLoggedIn()) {
    header('Location: login.php');
    exit;
}

$currentUser = getCurrentUser($pdo);
$userRole = $_SESSION['role'] ?? 'guest';
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой профиль</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <?php include 'navbar.php'; ?>
    
    <div class="container mt-4">
        <h2><i class="fas fa-user-circle me-2"></i>Мой профиль</h2>
        
        <div class="card mt-3">
            <div class="card-header">
                <h5>Основная информация</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Имя:</strong> <?= htmlspecialchars($currentUser['first_name'] ?? '') ?></p>
                        <p><strong>Фамилия:</strong> <?= htmlspecialchars($currentUser['last_name'] ?? '') ?></p>
                        <p><strong>Email:</strong> <?= htmlspecialchars($currentUser['email'] ?? '') ?></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Телефон:</strong> <?= htmlspecialchars($currentUser['phone'] ?? '') ?></p>
                        <p><strong>Роль:</strong> <span class="badge bg-primary"><?= $userRole ?></span></p>
                        <?php if ($userRole === 'employee' || $userRole === 'cleaner'): ?>
                        <p><strong>Должность:</strong> <?= htmlspecialchars($currentUser['position'] ?? '') ?></p>
                        <p><strong>Отдел:</strong> <?= htmlspecialchars($currentUser['department'] ?? '') ?></p>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <a href="index.php" class="btn btn-primary">На главную</a>
        </div>
    </div>
</body>
</html>
