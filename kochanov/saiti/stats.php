<?php
// stats.php
session_start();
require_once 'config.php';
require_once 'auth.php';
require_once 'functions.php';

// Проверка авторизации
if (!isLoggedIn()) {
    header('Location: login.php');
    exit;
}

$currentUser = getCurrentUser($pdo);

// Статистика
$stats = [
    'total_properties' => $pdo->query("SELECT COUNT(*) FROM property")->fetchColumn(),
    'active_properties' => $pdo->query("SELECT COUNT(*) FROM property WHERE is_active = true")->fetchColumn(),
    'total_bookings' => $pdo->query("SELECT COUNT(*) FROM booking")->fetchColumn(),
    'active_bookings' => $pdo->query("SELECT COUNT(*) FROM booking WHERE status IN ('confirmed', 'active')")->fetchColumn(),
    'total_guests' => $pdo->query("SELECT COUNT(*) FROM guest")->fetchColumn(),
    'total_employees' => $pdo->query("SELECT COUNT(*) FROM employee")->fetchColumn(),
    'total_payments' => $pdo->query("SELECT COUNT(*) FROM payment")->fetchColumn(),
    'revenue' => $pdo->query("SELECT SUM(amount) FROM payment WHERE payment_status = 'completed'")->fetchColumn(),
];

// Статистика по месяцам
$monthlyBookings = $pdo->query("
    SELECT 
        TO_CHAR(check_in_date, 'YYYY-MM') as month,
        COUNT(*) as bookings,
        SUM(total_price) as revenue
    FROM booking
    WHERE check_in_date >= NOW() - INTERVAL '6 months'
    GROUP BY TO_CHAR(check_in_date, 'YYYY-MM')
    ORDER BY month DESC
    LIMIT 6
")->fetchAll(PDO::FETCH_ASSOC);

// Популярные объекты
$popularProperties = $pdo->query("
    SELECT 
        p.property_id,
        p.title,
        p.city,
        COUNT(b.booking_id) as bookings_count,
        AVG(b.total_price) as avg_price
    FROM property p
    LEFT JOIN booking b ON p.property_id = b.property_id
    GROUP BY p.property_id, p.title, p.city
    ORDER BY bookings_count DESC
    LIMIT 5
")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Статистика - Система управления арендой</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .stat-card {
            border-radius: 10px;
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-card .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .stat-card .stat-value {
            font-size: 2rem;
            font-weight: bold;
        }
        .stat-card .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <?php include 'navbar.php'; ?>
    
    <div class="container-fluid mt-4">
        <h2 class="mb-4">
            <i class="fas fa-chart-bar text-primary"></i>
            Статистика системы
        </h2>
        
        <!-- Основные метрики -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="stat-icon">
                        <i class="fas fa-home"></i>
                    </div>
                    <div class="stat-value"><?= $stats['active_properties'] ?></div>
                    <div class="stat-label">Активных объектов</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="stat-icon">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <div class="stat-value"><?= $stats['active_bookings'] ?></div>
                    <div class="stat-label">Активных бронирований</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <div class="stat-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="stat-value"><?= $stats['total_guests'] ?></div>
                    <div class="stat-label">Зарегистрированных гостей</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <div class="stat-icon">
                        <i class="fas fa-ruble-sign"></i>
                    </div>
                    <div class="stat-value"><?= number_format($stats['revenue'] ?? 0, 0, '', ' ') ?> ₽</div>
                    <div class="stat-label">Общая выручка</div>
                </div>
            </div>
        </div>
        
        <!-- Графики -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-chart-line"></i> Бронирования по месяцам
                    </div>
                    <div class="card-body">
                        <canvas id="bookingsChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-star"></i> Популярные объекты
                    </div>
                    <div class="card-body">
                        <div class="list-group">
                            <?php foreach ($popularProperties as $property): ?>
                            <div class="list-group-item">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1"><?= htmlspecialchars($property['title']) ?></h6>
                                    <span class="badge bg-primary"><?= $property['bookings_count'] ?> броней</span>
                                </div>
                                <small class="text-muted"><?= htmlspecialchars($property['city']) ?></small>
                                <div class="mt-1">
                                    <small>Ср. цена: <strong><?= number_format($property['avg_price'] ?? 0, 0, '', ' ') ?> ₽</strong></small>
                                </div>
                            </div>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Подробная статистика -->
        <div class="card mb-4">
            <div class="card-header">
                <i class="fas fa-table"></i> Подробная статистика
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Показатель</th>
                                <th>Значение</th>
                                <th>Описание</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><i class="fas fa-database text-primary"></i> Всего таблиц</td>
                                <td><span class="badge bg-primary"><?= count(getAllTables($pdo)) ?></span></td>
                                <td>Количество таблиц в базе данных</td>
                            </tr>
                            <tr>
                                <td><i class="fas fa-home text-success"></i> Всего объектов</td>
                                <td><span class="badge bg-success"><?= $stats['total_properties'] ?></span></td>
                                <td>Общее количество объектов недвижимости</td>
                            </tr>
                            <tr>
                                <td><i class="fas fa-calendar text-info"></i> Всего бронирований</td>
                                <td><span class="badge bg-info"><?= $stats['total_bookings'] ?></span></td>
                                <td>Общее количество бронирований</td>
                            </tr>
                            <tr>
                                <td><i class="fas fa-user-tie text-warning"></i> Сотрудников</td>
                                <td><span class="badge bg-warning"><?= $stats['total_employees'] ?></span></td>
                                <td>Количество сотрудников агентства</td>
                            </tr>
                            <tr>
                                <td><i class="fas fa-money-check-alt text-danger"></i> Платежей</td>
                                <td><span class="badge bg-danger"><?= $stats['total_payments'] ?></span></td>
                                <td>Общее количество финансовых транзакций</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // График бронирований
        const bookingsCtx = document.getElementById('bookingsChart').getContext('2d');
        const bookingsChart = new Chart(bookingsCtx, {
            type: 'line',
            data: {
                labels: <?= json_encode(array_column(array_reverse($monthlyBookings), 'month')) ?>,
                datasets: [{
                    label: 'Количество бронирований',
                    data: <?= json_encode(array_column(array_reverse($monthlyBookings), 'bookings')) ?>,
                    borderColor: '#4a6fa5',
                    backgroundColor: 'rgba(74, 111, 165, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
