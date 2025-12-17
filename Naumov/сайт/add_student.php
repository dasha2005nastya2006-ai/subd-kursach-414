<?php
include 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $sql = "INSERT INTO student (familiya, imya, email, data_rozhdeniya)
            VALUES (?, ?, ?, ?)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        $_POST['familiya'],
        $_POST['imya'],
        $_POST['email'],
        $_POST['data_rozhdeniya']
    ]);
    header("Location: students.php");
}
include 'header.php';
?>

<h2>Добавить студента</h2>

<form method="post">
    <input name="familiya" placeholder="Фамилия" required><br><br>
    <input name="imya" placeholder="Имя" required><br><br>
    <input name="email" placeholder="Email"><br><br>
    <input type="date" name="data_rozhdeniya" required><br><br>
    <button>Сохранить</button>
</form>

<?php include 'footer.php'; ?>
