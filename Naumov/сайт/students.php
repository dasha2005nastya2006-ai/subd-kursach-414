<?php
include 'config.php';
include 'header.php';

$stmt = $pdo->query("SELECT familiya, imya, email FROM student");
?>

<h2>Список студентов</h2>

<table>
<tr>
    <th>Фамилия</th>
    <th>Имя</th>
    <th>Email</th>
</tr>

<?php foreach ($stmt as $row): ?>
<tr>
    <td><?= htmlspecialchars($row['familiya']) ?></td>
    <td><?= htmlspecialchars($row['imya']) ?></td>
    <td><?= htmlspecialchars($row['email']) ?></td>
</tr>
<?php endforeach; ?>
</table>

<?php include 'footer.php'; ?>
