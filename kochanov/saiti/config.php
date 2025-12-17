<?php
// Конфигурация базы данных
define('DB_HOST', 'localhost');
define('DB_PORT', '5432');
define('DB_NAME', 'kursovaya');
define('DB_USER', 'postgres');
define('DB_PASS', '22081921');

// Подключение к PostgreSQL
function connectDB() {
    try {
        $dsn = "pgsql:host=" . DB_HOST . ";port=" . DB_PORT . ";dbname=" . DB_NAME;
        $pdo = new PDO($dsn, DB_USER, DB_PASS);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->exec("SET NAMES 'UTF8'");
        return $pdo;
    } catch (PDOException $e) {
        die("Ошибка подключения к БД: " . $e->getMessage());
    }
}

// Глобальная переменная для подключения
$pdo = connectDB();
?>
