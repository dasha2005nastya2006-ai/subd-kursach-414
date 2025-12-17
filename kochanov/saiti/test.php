<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
session_start();

echo "<h1>Тест системы</h1>";

// Проверяем существование файлов
$files = [
    'config.php',
    'functions.php', 
    'auth.php',
    'navbar.php',
    'logout.php',
    'login.php',
    'index.php',
    'register.php',
    'style.css'
];

foreach ($files as $file) {
    if (file_exists($file)) {
        echo "<p style='color:green;'>✓ $file найден</p>";
    } else {
        echo "<p style='color:orange;'>⚠ $file не найден</p>";
    }
}

// Проверяем важные функции
if (file_exists('config.php')) {
    require_once 'config.php';
    echo "<p style='color:green;'>✓ config.php загружен</p>";
    
    try {
        $test = $pdo->query("SELECT 1")->fetchColumn();
        echo "<p style='color:green;'>✓ Подключение к БД работает</p>";
    } catch (Exception $e) {
        echo "<p style='color:red;'>✗ Ошибка БД: " . $e->getMessage() . "</p>";
    }
}

echo "<hr><a href='login.php'>Перейти к странице входа</a>";
?>
