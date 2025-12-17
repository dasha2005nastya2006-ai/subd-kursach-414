<?php
$host = "localhost";
$db   = "unium_db";
$user = "unium_user";
$pass = "Unium1"; // поменяешь на Linux

try {
    $pdo = new PDO(
        "pgsql:host=$host;dbname=$db",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    die("Ошибка подключения к БД");
}
