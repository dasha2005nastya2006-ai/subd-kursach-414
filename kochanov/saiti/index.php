<?php
// index.php - Главная страница системы управления
session_start();
require_once 'config.php';
require_once 'functions.php';
require_once 'auth.php';

// Проверка авторизации
if (!isLoggedIn()) {
    header('Location: login.php');
    exit;
}

// Получение информации о текущем пользователе
$currentUser = getCurrentUser($pdo);

// Получение параметров
$currentTable = $_GET['table'] ?? '';
$action = $_GET['action'] ?? 'view';
$limit = $_GET['limit'] ?? 100;
$sqlQuery = $_POST['sql'] ?? '';

// Получить все таблицы
$tables = getAllTables($pdo);
$tableCount = count($tables);

// Если выбрана таблица
$tableStructure = [];
$tableData = [];
$rowCount = 0;

if ($currentTable && tableExists($pdo, $currentTable)) {
    $tableStructure = getTableStructure($pdo, $currentTable);
    $tableData = getTableData($pdo, $currentTable, $limit);
    $rowCount = getRowCount($pdo, $currentTable);
}

// Выполнение SQL запроса
$sqlResult = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($sqlQuery)) {
    $sqlResult = executeSQL($pdo, $sqlQuery);
    
    // Логируем SQL запросы от пользователей
    if ($currentUser) {
        logAction($pdo, $currentUser['user_id'], 'sql_execute', $currentTable, null);
    }
}

// Получение статистики для левой панели
$stats = [
    'properties' => $pdo->query("SELECT COUNT(*) FROM property WHERE is_active = true")->fetchColumn(),
    'active_bookings' => $pdo->query("SELECT COUNT(*) FROM booking WHERE status IN ('confirmed', 'active')")->fetchColumn(),
    'total_guests' => $pdo->query("SELECT COUNT(*) FROM guest")->fetchColumn(),
    'pending_cleanings' => $pdo->query("SELECT COUNT(*) FROM cleaning_task WHERE status = 'scheduled'")->fetchColumn(),
    'pending_payments' => $pdo->query("SELECT COUNT(*) FROM payment WHERE payment_status IN ('pending', 'processing')")->fetchColumn(),
];

// Проверка ролей для отображения дополнительных опций
$isAdmin = hasRole('admin');
$isEmployee = hasRole('employee') || hasRole('admin');
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Управление базой данных аренды квартир</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Дополнительные стили */
        .user-badge {
            font-size: 0.8em;
            padding: 2px 8px;
        }
        .table-list-item:hover {
            background-color: #f1f8ff;
            transform: translateX(3px);
            transition: all 0.2s;
        }
        .card-header {
            font-weight: 600;
        }
        .sql-editor {
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .table-structure td {
            vertical-align: middle;
        }
        .quick-stats {
            font-size: 0.9rem;
        }
        .quick-stats .badge {
            font-size: 0.8em;
        }
        /* Стили для разных ролей */
        .role-admin {
            color: #dc3545;
        }
        .role-employee {
            color: #0d6efd;
        }
        .role-guest {
            color: #198754;
        }
        .role-cleaner {
            color: #6f42c1;
        }
    </style>
</head>
<body>
    <!-- Навигационная панель -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4 shadow">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.php">
                <i class="fas fa-database me-2"></i>
                <span class="fw-bold">Управление арендой</span>
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link <?= !$currentTable ? 'active' : '' ?>" href="index.php">
                            <i class="fas fa-home me-1"></i> Главная
                        </a>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href="stats.php">
                            <i class="fas fa-chart-bar me-1"></i> Статистика
                        </a>
                    </li>
                    
                    <?php if ($isEmployee): ?>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-tools me-1"></i> Управление
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="?table=booking"><i class="fas fa-calendar me-2"></i> Бронирования</a></li>
                            <li><a class="dropdown-item" href="?table=property"><i class="fas fa-home me-2"></i> Объекты</a></li>
                            <li><a class="dropdown-item" href="?table=guest"><i class="fas fa-users me-2"></i> Гости</a></li>
                            <li><a class="dropdown-item" href="?table=payment"><i class="fas fa-money-bill me-2"></i> Платежи</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="?table=cleaning_task"><i class="fas fa-broom me-2"></i> Уборки</a></li>
                            <li><a class="dropdown-item" href="?table=review"><i class="fas fa-star me-2"></i> Отзывы</a></li>
                            <?php if ($isAdmin): ?>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="?table=users"><i class="fas fa-user-cog me-2"></i> Пользователи</a></li>
                            <li><a class="dropdown-item" href="?table=employee"><i class="fas fa-user-tie me-2"></i> Сотрудники</a></li>
                            <li><a class="dropdown-item" href="?table=blacklist"><i class="fas fa-ban me-2"></i> Черный список</a></li>
                            <?php endif; ?>
                        </ul>
                    </li>
                    <?php endif; ?>
                    
                    <?php if ($isAdmin): ?>
                    <li class="nav-item">
                        <a class="nav-link text-warning" href="admin.php">
                            <i class="fas fa-crown me-1"></i> Админ-панель
                        </a>
                    </li>
                    <?php endif; ?>
                </ul>
                
                <!-- Информация о пользователе -->
                <div class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-user-circle fa-lg me-2"></i>
                                <div class="text-start">
                                    <div class="fw-bold"><?= htmlspecialchars($currentUser['first_name'] ?? 'Пользователь') ?></div>
                                    <div class="small text-white-50">
                                        <?php 
                                        $roleClass = 'role-' . ($_SESSION['role'] ?? 'guest');
                                        echo '<span class="' . $roleClass . '">' . ($_SESSION['role'] ?? 'guest') . '</span>';
                                        ?>
                                    </div>
                                </div>
                            </div>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end shadow">
                            <li>
                                <div class="dropdown-item-text">
                                    <div class="small text-muted">Вход выполнен:</div>
                                    <div class="fw-bold"><?= htmlspecialchars($currentUser['email'] ?? '') ?></div>
                                    <?php if (!empty($currentUser['last_login'])): ?>
                                    <div class="small text-muted mt-1">
                                        <i class="fas fa-clock me-1"></i>
                                        <?= date('d.m.Y H:i', strtotime($currentUser['last_login'])) ?>
                                    </div>
                                    <?php endif; ?>
                                </div>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="profile.php">
                                    <i class="fas fa-user-cog me-2"></i> Мой профиль
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="?table=<?= urlencode('users') ?>&action=data&id=<?= $currentUser['user_id'] ?? '' ?>">
                                    <i class="fas fa-eye me-2"></i> Мои данные
                                </a>
                            </li>
                            <?php if ($isEmployee && !empty($currentUser['user_id'])): ?>
                            <li>
                                <a class="dropdown-item" href="?table=<?= urlencode('employee') ?>&action=data">
                                    <i class="fas fa-id-card me-2"></i> Информация о сотруднике
                                </a>
                            </li>
                            <?php endif; ?>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-danger" href="logout.php">
                                    <i class="fas fa-sign-out-alt me-2"></i> Выйти из системы
                                </a>
                            </li>
                        </ul>
                    </li>
                </div>
            </div>
        </div>
    </nav>

    <!-- Основной контент -->
    <div class="container-fluid">
        <!-- Системные уведомления -->
        <?php if (isset($_GET['message'])): ?>
            <?php 
            $messages = [
                'logout_success' => ['type' => 'success', 'text' => 'Вы успешно вышли из системы'],
                'login_success' => ['type' => 'success', 'text' => 'Вход выполнен успешно'],
                'access_denied' => ['type' => 'danger', 'text' => 'Доступ запрещен'],
                'error' => ['type' => 'danger', 'text' => 'Произошла ошибка'],
            ];
            if (isset($messages[$_GET['message']])): 
                $msg = $messages[$_GET['message']];
            ?>
                <div class="alert alert-<?= $msg['type'] ?> alert-dismissible fade show" role="alert">
                    <i class="fas fa-<?= $msg['type'] === 'success' ? 'check-circle' : 'exclamation-triangle' ?> me-2"></i>
                    <?= $msg['text'] ?>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            <?php endif; ?>
        <?php endif; ?>

        <!-- Заголовок и информация о системе -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-body py-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h1 class="h4 mb-1">
                                    <i class="fas fa-database text-primary me-2"></i>
                                    База данных агентства аренды квартир
                                </h1>
                                <p class="text-muted mb-0">
                                    <i class="fas fa-info-circle me-1"></i>
                                    Управление и мониторинг данных системы
                                    <?php if ($currentTable): ?>
                                    | Текущая таблица: <span class="fw-bold text-primary"><?= $currentTable ?></span>
                                    <?php endif; ?>
                                </p>
                            </div>
                            <div class="text-end">
                                <div class="quick-stats">
                                    <span class="badge bg-secondary me-2">
                                        <i class="fas fa-table me-1"></i><?= $tableCount ?> таблиц
                                    </span>
                                    <span class="badge bg-success">
                                        <i class="fas fa-user me-1"></i>Вход: <?= $_SESSION['role'] ?? 'guest' ?>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Левая колонка: список таблиц и статистика -->
            <div class="col-md-3">
                <!-- Карточка с таблицами -->
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-table me-2"></i>
                                <span class="fw-bold">Таблицы</span>
                            </div>
                            <span class="badge bg-light text-dark"><?= $tableCount ?></span>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush">
                            <?php 
                            $tableGroups = [
                                'Основные' => ['property', 'booking', 'guest', 'payment'],
                                'Справочники' => ['property_type', 'property_category', 'rental_plan', 'service'],
                                'Операции' => ['cleaning_task', 'booking_service', 'inventory_check'],
                                'Пользователи' => ['users', 'employee', 'user_sessions'],
                                'Контент' => ['review', 'message', 'notification'],
                                'Настройки' => ['site_setting', 'promo_code', 'blacklist'],
                            ];
                            
                            foreach ($tableGroups as $groupName => $groupTables):
                                // Фильтруем только существующие таблицы
                                $existingTables = array_intersect($groupTables, $tables);
                                if (empty($existingTables)) continue;
                            ?>
                                <div class="list-group-item bg-light fw-bold small py-2">
                                    <i class="fas fa-folder me-1"></i><?= $groupName ?>
                                </div>
                                <?php foreach ($existingTables as $table): 
                                    $count = getRowCount($pdo, $table);
                                    $isActive = $table === $currentTable;
                                ?>
                                    <a href="?table=<?= urlencode($table) ?>" 
                                       class="list-group-item list-group-item-action table-list-item <?= $isActive ? 'active' : '' ?> py-2">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <i class="fas fa-table text-muted me-2"></i>
                                                <span class="<?= $isActive ? 'text-white fw-bold' : '' ?>">
                                                    <?= $table ?>
                                                </span>
                                            </div>
                                            <span class="badge bg-<?= $isActive ? 'light text-dark' : 'secondary' ?>">
                                                <?= $count ?>
                                            </span>
                                        </div>
                                    </a>
                                <?php endforeach; ?>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </div>

                <!-- Быстрая статистика -->
                <div class="card shadow-sm">
                    <div class="card-header bg-info text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-chart-bar me-2"></i>
                                <span class="fw-bold">Системные показатели</span>
                            </div>
                            <i class="fas fa-arrow-up text-success"></i>
                        </div>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled mb-0">
                            <li class="mb-2 d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-home text-success me-2"></i>
                                    <span class="small">Активные объекты</span>
                                </div>
                                <span class="badge bg-success"><?= $stats['properties'] ?></span>
                            </li>
                            <li class="mb-2 d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-calendar-check text-primary me-2"></i>
                                    <span class="small">Активные брони</span>
                                </div>
                                <span class="badge bg-primary"><?= $stats['active_bookings'] ?></span>
                            </li>
                            <li class="mb-2 d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-users text-warning me-2"></i>
                                    <span class="small">Всего гостей</span>
                                </div>
                                <span class="badge bg-warning"><?= $stats['total_guests'] ?></span>
                            </li>
                            <li class="mb-2 d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-broom text-danger me-2"></i>
                                    <span class="small">Уборки в ожидании</span>
                                </div>
                                <span class="badge bg-danger"><?= $stats['pending_cleanings'] ?></span>
                            </li>
                            <li class="mb-2 d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-money-bill-wave text-info me-2"></i>
                                    <span class="small">Ожидают оплаты</span>
                                </div>
                                <span class="badge bg-info"><?= $stats['pending_payments'] ?></span>
                            </li>
                        </ul>
                        
                        <!-- Кнопки быстрого доступа -->
                        <?php if ($isEmployee): ?>
                        <hr class="my-3">
                        <div class="text-center">
                            <a href="?table=booking&action=data" class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-calendar-plus"></i>
                            </a>
                            <a href="?table=property&action=data" class="btn btn-sm btn-outline-success me-1">
                                <i class="fas fa-home"></i>
                            </a>
                            <a href="?table=guest&action=data" class="btn btn-sm btn-outline-warning me-1">
                                <i class="fas fa-user-plus"></i>
                            </a>
                            <a href="stats.php" class="btn btn-sm btn-outline-info">
                                <i class="fas fa-chart-pie"></i>
                            </a>
                        </div>
                        <?php endif; ?>
                    </div>
                </div>
            </div>

            <!-- Правая колонка: основное содержимое -->
            <div class="col-md-9">
                <?php if ($currentTable): ?>
                <!-- Информация о выбранной таблице -->
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-success text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-info-circle me-2"></i>
                                <span class="fw-bold">Таблица: <?= $currentTable ?></span>
                                <span class="badge bg-light text-dark ms-2"><?= $rowCount ?> записей</span>
                            </div>
                            <div>
                                <div class="btn-group btn-group-sm">
                                    <a href="?table=<?= urlencode($currentTable) ?>&action=structure" 
                                       class="btn btn-light <?= $action === 'structure' ? 'active' : '' ?>">
                                        <i class="fas fa-cog me-1"></i> Структура
                                    </a>
                                    <a href="?table=<?= urlencode($currentTable) ?>&action=data" 
                                       class="btn btn-light <?= $action === 'data' ? 'active' : '' ?>">
                                        <i class="fas fa-list me-1"></i> Данные
                                    </a>
                                    <?php if ($isAdmin): ?>
                                    <a href="#" class="btn btn-light" data-bs-toggle="modal" data-bs-target="#addRecordModal">
                                        <i class="fas fa-plus me-1"></i> Добавить
                                    </a>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Структура таблицы -->
                    <?php if ($action === 'structure'): ?>
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-code me-2"></i>Структура таблицы
                        </h5>
                        <div class="table-responsive">
                            <table class="table table-striped table-hover table-structure">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Имя поля</th>
                                        <th>Тип данных</th>
                                        <th>NULL</th>
                                        <th>Значение по умолчанию</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($tableStructure as $column): 
                                        $isNullable = $column['is_nullable'] === 'YES';
                                        $isPrimaryKey = stripos($column['column_default'] ?? '', 'nextval') !== false;
                                    ?>
                                    <tr>
                                        <td>
                                            <span class="fw-bold"><?= $column['column_name'] ?></span>
                                            <?php if ($isPrimaryKey): ?>
                                            <span class="badge bg-danger ms-1" title="Первичный ключ">PK</span>
                                            <?php endif; ?>
                                        </td>
                                        <td>
                                            <code class="<?= $isPrimaryKey ? 'text-danger' : '' ?>">
                                                <?= $column['data_type'] ?>
                                            </code>
                                        </td>
                                        <td>
                                            <span class="badge <?= $isNullable ? 'bg-warning' : 'bg-success' ?>">
                                                <?= $isNullable ? 'ДА' : 'НЕТ' ?>
                                            </span>
                                        </td>
                                        <td>
                                            <small class="font-monospace">
                                                <?= $column['column_default'] ? htmlspecialchars($column['column_default']) : '<span class="text-muted">NULL</span>' ?>
                                            </small>
                                        </td>
                                        <td>
                                            <?php
                                            // Автоматическое описание по имени поля
                                            $descriptions = [
                                                'id' => 'Идентификатор записи',
                                                'email' => 'Email адрес',
                                                'phone' => 'Номер телефона',
                                                'price' => 'Стоимость',
                                                'date' => 'Дата',
                                                'status' => 'Статус записи',
                                                'created_at' => 'Дата создания',
                                                'updated_at' => 'Дата обновления',
                                            ];
                                            
                                            $desc = '';
                                            foreach ($descriptions as $key => $value) {
                                                if (stripos($column['column_name'], $key) !== false) {
                                                    $desc = $value;
                                                    break;
                                                }
                                            }
                                            echo $desc ? '<small class="text-muted">' . $desc . '</small>' : '-';
                                            ?>
                                        </td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Данные таблицы -->
                    <?php elseif ($action === 'data'): ?>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h5 class="card-title mb-0">
                                <i class="fas fa-list me-2"></i>Данные таблицы
                                <small class="text-muted">(первые <?= $limit ?> записей)</small>
                            </h5>
                            <div>
                                <a href="?table=<?= urlencode($currentTable) ?>&action=data&limit=50" 
                                   class="btn btn-sm btn-outline-secondary <?= $limit == 50 ? 'active' : '' ?>">50</a>
                                <a href="?table=<?= urlencode($currentTable) ?>&action=data&limit=100" 
                                   class="btn btn-sm btn-outline-secondary <?= $limit == 100 ? 'active' : '' ?>">100</a>
                                <a href="?table=<?= urlencode($currentTable) ?>&action=data&limit=500" 
                                   class="btn btn-sm btn-outline-secondary <?= $limit == 500 ? 'active' : '' ?>">500</a>
                            </div>
                        </div>
                        
                        <?php if (!empty($tableData)): ?>
                        <div class="table-responsive">
                            <table class="table table-striped table-hover table-sm">
                                <thead class="table-dark">
                                    <tr>
                                        <?php foreach (array_keys($tableData[0]) as $column): ?>
                                        <th>
                                            <div class="d-flex align-items-center">
                                                <?= $column ?>
                                                <?php if (in_array($column, ['id', 'user_id', 'property_id'])): ?>
                                                <i class="fas fa-key text-warning ms-1" title="Ключевое поле"></i>
                                                <?php endif; ?>
                                            </div>
                                        </th>
                                        <?php endforeach; ?>
                                        <?php if ($isAdmin): ?>
                                        <th class="text-center">Действия</th>
                                        <?php endif; ?>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($tableData as $index => $row): ?>
                                    <tr>
                                        <?php foreach ($row as $value): ?>
                                        <td>
                                            <?php 
                                            if (is_bool($value)) {
                                                echo '<span class="badge bg-' . ($value ? 'success' : 'secondary') . '">';
                                                echo $value ? 'true' : 'false';
                                                echo '</span>';
                                            } elseif ($value === null) {
                                                echo '<span class="badge bg-light text-muted">NULL</span>';
                                            } elseif (strlen($value) > 50) {
                                                echo '<span title="' . htmlspecialchars($value) . '">';
                                                echo htmlspecialchars(substr($value, 0, 50)) . '...';
                                                echo '</span>';
                                            } else {
                                                echo htmlspecialchars($value);
                                            }
                                            ?>
                                        </td>
                                        <?php endforeach; ?>
                                        <?php if ($isAdmin): ?>
                                        <td class="text-center">
                                            <div class="btn-group btn-group-sm">
                                                <button class="btn btn-outline-primary" 
                                                        onclick="editRow(this)" 
                                                        data-row="<?= $index ?>"
                                                        title="Редактировать">
                                                    <i class="fas fa-edit"></i>
                                                </button>
                                                <button class="btn btn-outline-danger" 
                                                        onclick="deleteRow(this)"
                                                        title="Удалить">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                        </td>
                                        <?php endif; ?>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                        
                        <!-- Пагинация -->
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <div class="small text-muted">
                                Показано <?= min($limit, count($tableData)) ?> из <?= $rowCount ?> записей
                            </div>
                            <?php if ($rowCount > $limit): ?>
                            <div>
                                <a href="#" class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-arrow-left me-1"></i>Назад
                                </a>
                                <a href="#" class="btn btn-sm btn-outline-primary">
                                    Вперед<i class="fas fa-arrow-right ms-1"></i>
                                </a>
                            </div>
                            <?php endif; ?>
                        </div>
                        
                        <?php else: ?>
                        <div class="alert alert-info">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-info-circle fa-2x me-3"></i>
                                <div>
                                    <h5 class="alert-heading">Таблица пуста</h5>
                                    <p class="mb-0">В таблице <strong><?= $currentTable ?></strong> нет данных.</p>
                                    <?php if ($isAdmin): ?>
                                    <p class="mb-0 mt-2">
                                        <a href="#" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#addRecordModal">
                                            <i class="fas fa-plus me-1"></i>Добавить первую запись
                                        </a>
                                    </p>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </div>
                        <?php endif; ?>
                    </div>
                    <?php endif; ?>
                </div>

                <!-- SQL редактор (только для админов и сотрудников) -->
                <?php if ($isEmployee): ?>
                <div class="card shadow-sm">
                    <div class="card-header bg-dark text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-terminal me-2"></i>
                                <span class="fw-bold">SQL редактор</span>
                                <small class="text-white-50 ms-2">для таблицы <code><?= $currentTable ?></code></small>
                            </div>
                            <span class="badge bg-warning">Только чтение</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <form method="POST" id="sqlForm">
                            <div class="mb-3">
                                <label class="form-label">
                                    <i class="fas fa-code me-1"></i>SQL запрос
                                    <?php if (!$isAdmin): ?>
                                    <small class="text-muted">(только SELECT запросы)</small>
                                    <?php endif; ?>
                                </label>
                                <textarea name="sql" id="sqlQuery" 
                                          class="form-control sql-editor" 
                                          rows="4" 
                                          placeholder="<?= $isAdmin ? 'Введите SQL запрос...' : 'SELECT * FROM ' . $currentTable . ' LIMIT 10' ?>"
                                          <?= !$isAdmin ? 'readonly' : '' ?>><?= htmlspecialchars($sqlQuery) ?></textarea>
                                
                                <!-- Быстрые примеры запросов -->
                                <div class="mt-2 small">
                                    <span class="text-muted me-2">Примеры:</span>
                                    <?php
                                    $examples = [
                                        'SELECT * FROM ' . $currentTable . ' LIMIT 10',
                                        'SELECT COUNT(*) FROM ' . $currentTable,
                                        'SELECT * FROM ' . $currentTable . ' ORDER BY 1 DESC LIMIT 5',
                                    ];
                                    foreach ($examples as $example): 
                                    ?>
                                        <button type="button" class="btn btn-sm btn-outline-secondary me-1 mb-1" 
                                                onclick="document.getElementById('sqlQuery').value = '<?= $example ?>'">
                                            <?= htmlspecialchars(substr($example, 0, 30)) ?>...
                                        </button>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                            
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <button type="submit" class="btn btn-primary" <?= !$isAdmin ? 'disabled' : '' ?>>
                                        <i class="fas fa-play me-1"></i> Выполнить
                                    </button>
                                    <button type="button" class="btn btn-outline-secondary" 
                                            onclick="document.getElementById('sqlQuery').value = 'SELECT * FROM <?= $currentTable ?> LIMIT 10'">
                                        <i class="fas fa-redo me-1"></i> Сброс
                                    </button>
                                </div>
                                <?php if ($isAdmin): ?>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="safeMode" checked>
                                    <label class="form-check-label small" for="safeMode">
                                        Безопасный режим
                                    </label>
                                </div>
                                <?php endif; ?>
                            </div>
                        </form>

                        <!-- Результаты SQL запроса -->
                        <?php if ($sqlResult): ?>
                        <div class="mt-4">
                            <h6 class="border-bottom pb-2">
                                <i class="fas fa-poll me-2"></i>Результат запроса:
                                <?php if (isset($sqlResult['error'])): ?>
                                <span class="badge bg-danger">Ошибка</span>
                                <?php elseif (isset($sqlResult['affected_rows'])): ?>
                                <span class="badge bg-success">Успешно</span>
                                <?php else: ?>
                                <span class="badge bg-info">Данные: <?= count($sqlResult) ?> строк</span>
                                <?php endif; ?>
                            </h6>
                            
                            <?php if (isset($sqlResult['error'])): ?>
                            <div class="alert alert-danger">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-exclamation-triangle fa-2x me-3"></i>
                                    <div>
                                        <h5 class="alert-heading">Ошибка выполнения запроса</h5>
                                        <pre class="mb-0"><?= htmlspecialchars($sqlResult['error']) ?></pre>
                                    </div>
                                </div>
                            </div>
                            
                            <?php elseif (isset($sqlResult['affected_rows'])): ?>
                            <div class="alert alert-success">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-check-circle fa-2x me-3"></i>
                                    <div>
                                        <h5 class="alert-heading">Запрос выполнен успешно</h5>
                                        <p class="mb-0">
                                            Затронуто строк: <strong><?= $sqlResult['affected_rows'] ?></strong>
                                            <?php if ($sqlResult['affected_rows'] == 0): ?>
                                            <span class="ms-2 text-muted">(ни одна строка не была изменена)</span>
                                            <?php endif; ?>
                                        </p>
                                    </div>
                                </div>
                            </div>
                            
                            <?php elseif (is_array($sqlResult) && !empty($sqlResult)): ?>
                            <div class="table-responsive">
                                <table class="table table-sm table-striped table-bordered">
                                    <thead class="table-light">
                                        <tr>
                                            <?php foreach (array_keys($sqlResult[0]) as $column): ?>
                                            <th><?= $column ?></th>
                                            <?php endforeach; ?>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach (array_slice($sqlResult, 0, 100) as $row): ?>
                                        <tr>
                                            <?php foreach ($row as $value): ?>
                                            <td>
                                                <?php 
                                                if (is_bool($value)) {
                                                    echo $value ? '<span class="badge bg-success">true</span>' : '<span class="badge bg-secondary">false</span>';
                                                } elseif ($value === null) {
                                                    echo '<span class="badge bg-light text-muted">NULL</span>';
                                                } elseif (is_numeric($value)) {
                                                    echo number_format($value, 0, '', ' ');
                                                } elseif (strlen($value) > 30) {
                                                    echo '<span title="' . htmlspecialchars($value) . '">';
                                                    echo htmlspecialchars(substr($value, 0, 30)) . '...';
                                                    echo '</span>';
                                                } else {
                                                    echo htmlspecialchars($value);
                                                }
                                                ?>
                                            </td>
                                            <?php endforeach; ?>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                                <?php if (count($sqlResult) > 100): ?>
                                <div class="alert alert-warning mt-2">
                                    <i class="fas fa-info-circle me-2"></i>
                                    Показаны только первые 100 строк из <?= count($sqlResult) ?>
                                </div>
                                <?php endif; ?>
                            </div>
                            <?php else: ?>
                            <div class="alert alert-info">
                                <i class="fas fa-info-circle me-2"></i>
                                Запрос выполнен, но не вернул данных
                            </div>
                            <?php endif; ?>
                        </div>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endif; ?>

                <?php else: ?>
                <!-- Если таблица не выбрана - приветственный экран -->
                <div class="card shadow-sm">
                    <div class="card-body text-center py-5">
                        <div class="mb-4">
                            <i class="fas fa-database fa-5x text-primary mb-3"></i>
                            <h2>Добро пожаловать в систему управления!</h2>
                            <p class="lead text-muted mb-0">
                                <?= htmlspecialchars($currentUser['first_name'] ?? 'Пользователь') ?>, вы вошли как 
                                <span class="badge bg-<?= 
                                    ($_SESSION['role'] ?? 'guest') === 'admin' ? 'danger' : 
                                    (($_SESSION['role'] ?? 'guest') === 'employee' ? 'primary' : 'success')
                                ?>">
                                    <?= $_SESSION['role'] ?? 'guest' ?>
                                </span>
                            </p>
                        </div>
                        
                        <p class="text-muted mb-4">
                            Выберите таблицу из списка слева для работы с данными
                        </p>
                        
                        <div class="row mt-4">
                            <div class="col-md-6 mb-4">
                                <div class="card border-primary h-100">
                                    <div class="card-header bg-primary text-white">
                                        <i class="fas fa-home me-2"></i>Основные таблицы
                                    </div>
                                    <div class="card-body">
                                        <ul class="list-unstyled">
                                            <li class="mb-2">
                                                <a href="?table=property" class="text-decoration-none">
                                                    <i class="fas fa-building text-primary me-2"></i>
                                                    <strong>property</strong> - объекты недвижимости
                                                    <span class="badge bg-primary float-end"><?= getRowCount($pdo, 'property') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=booking" class="text-decoration-none">
                                                    <i class="fas fa-calendar text-success me-2"></i>
                                                    <strong>booking</strong> - бронирования
                                                    <span class="badge bg-success float-end"><?= getRowCount($pdo, 'booking') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=guest" class="text-decoration-none">
                                                    <i class="fas fa-users text-warning me-2"></i>
                                                    <strong>guest</strong> - гости
                                                    <span class="badge bg-warning float-end"><?= getRowCount($pdo, 'guest') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=payment" class="text-decoration-none">
                                                    <i class="fas fa-money-bill text-info me-2"></i>
                                                    <strong>payment</strong> - платежи
                                                    <span class="badge bg-info float-end"><?= getRowCount($pdo, 'payment') ?></span>
                                                </a>
                                            </li>
                                            <li>
                                                <a href="?table=cleaning_task" class="text-decoration-none">
                                                    <i class="fas fa-broom text-danger me-2"></i>
                                                    <strong>cleaning_task</strong> - задачи на уборку
                                                    <span class="badge bg-danger float-end"><?= getRowCount($pdo, 'cleaning_task') ?></span>
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-6 mb-4">
                                <div class="card border-success h-100">
                                    <div class="card-header bg-success text-white">
                                        <i class="fas fa-cogs me-2"></i>Системные таблицы
                                    </div>
                                    <div class="card-body">
                                        <ul class="list-unstyled">
                                            <li class="mb-2">
                                                <a href="?table=users" class="text-decoration-none">
                                                    <i class="fas fa-user-cog text-primary me-2"></i>
                                                    <strong>users</strong> - пользователи системы
                                                    <span class="badge bg-primary float-end"><?= getRowCount($pdo, 'users') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=employee" class="text-decoration-none">
                                                    <i class="fas fa-user-tie text-success me-2"></i>
                                                    <strong>employee</strong> - сотрудники
                                                    <span class="badge bg-success float-end"><?= getRowCount($pdo, 'employee') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=review" class="text-decoration-none">
                                                    <i class="fas fa-star text-warning me-2"></i>
                                                    <strong>review</strong> - отзывы
                                                    <span class="badge bg-warning float-end"><?= getRowCount($pdo, 'review') ?></span>
                                                </a>
                                            </li>
                                            <li class="mb-2">
                                                <a href="?table=blacklist" class="text-decoration-none">
                                                    <i class="fas fa-ban text-danger me-2"></i>
                                                    <strong>blacklist</strong> - черный список
                                                    <span class="badge bg-danger float-end"><?= getRowCount($pdo, 'blacklist') ?></span>
                                                </a>
                                            </li>
                                            <li>
                                                <a href="?table=site_setting" class="text-decoration-none">
                                                    <i class="fas fa-sliders-h text-info me-2"></i>
                                                    <strong>site_setting</strong> - настройки
                                                    <span class="badge bg-info float-end"><?= getRowCount($pdo, 'site_setting') ?></span>
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Быстрый доступ для сотрудников -->
                        <?php if ($isEmployee): ?>
                        <div class="card border-warning mt-4">
                            <div class="card-header bg-warning text-dark">
                                <i class="fas fa-bolt me-2"></i>Быстрые действия
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-md-3 mb-2">
                                        <a href="?table=booking&action=data" class="btn btn-outline-primary btn-block">
                                            <i class="fas fa-plus-circle fa-2x mb-2"></i><br>
                                            Новое бронирование
                                        </a>
                                    </div>
                                    <div class="col-md-3 mb-2">
                                        <a href="?table=property&action=data" class="btn btn-outline-success btn-block">
                                            <i class="fas fa-home fa-2x mb-2"></i><br>
                                            Добавить объект
                                        </a>
                                    </div>
                                    <div class="col-md-3 mb-2">
                                        <a href="stats.php" class="btn btn-outline-info btn-block">
                                            <i class="fas fa-chart-bar fa-2x mb-2"></i><br>
                                            Статистика
                                        </a>
                                    </div>
                                    <div class="col-md-3 mb-2">
                                        <a href="?table=guest&action=data" class="btn btn-outline-warning btn-block">
                                            <i class="fas fa-user-plus fa-2x mb-2"></i><br>
                                            Новый гость
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Подвал -->
        <footer class="mt-5 pt-4 pb-3 text-center border-top">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <i class="fas fa-database fa-lg text-primary me-2"></i>
                    <strong>PostgreSQL <?= $pdo->query('SELECT version()')->fetchColumn(0) ?></strong>
                </div>
                <div class="col-md-4 mb-3">
                    <i class="fas fa-server fa-lg text-success me-2"></i>
                    <strong>Apache + PHP <?= phpversion() ?></strong>
                </div>
                <div class="col-md-4 mb-3">
                    <i class="fas fa-table fa-lg text-info me-2"></i>
                    <strong><?= $tableCount ?> таблиц</strong>
                </div>
            </div>
            <div class="mt-3">
                <small class="text-muted">
                    Система управления арендой квартир &copy; <?= date('Y') ?> | 
                    <i class="fas fa-user me-1"></i> <?= htmlspecialchars($currentUser['first_name'] ?? 'Гость') ?> 
                    (<?= $_SESSION['role'] ?? 'guest' ?>) |
                    Время: <?= date('H:i:s') ?>
                </small>
            </div>
        </footer>
    </div>

    <!-- Модальное окно для добавления записи -->
    <?php if ($isAdmin && $currentTable): ?>
    <div class="modal fade" id="addRecordModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-plus-circle me-2"></i>
                        Добавить запись в таблицу: <?= $currentTable ?>
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <form method="POST" action="add_record.php">
                    <div class="modal-body">
                        <input type="hidden" name="table" value="<?= $currentTable ?>">
                        <div class="row">
                            <?php foreach ($tableStructure as $column): 
                                if (stripos($column['column_default'] ?? '', 'nextval') !== false) continue; // Пропускаем автоинкремент
                            ?>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">
                                    <?= $column['column_name'] ?>
                                    <?php if ($column['is_nullable'] === 'NO'): ?>
                                    <span class="text-danger">*</span>
                                    <?php endif; ?>
                                </label>
                                
                                <?php 
                                $inputType = 'text';
                                $placeholder = '';
                                
                                if (stripos($column['data_type'], 'int') !== false) {
                                    $inputType = 'number';
                                } elseif (stripos($column['data_type'], 'bool') !== false) {
                                    // Булево поле - чекбокс
                                } elseif (stripos($column['column_name'], 'email') !== false) {
                                    $inputType = 'email';
                                } elseif (stripos($column['column_name'], 'date') !== false) {
                                    $inputType = 'date';
                                } elseif (stripos($column['column_name'], 'time') !== false) {
                                    $inputType = 'time';
                                }
                                ?>
                                
                                <?php if (stripos($column['data_type'], 'bool') !== false): ?>
                                <select class="form-select" name="<?= $column['column_name'] ?>">
                                    <option value="true">Да (true)</option>
                                    <option value="false">Нет (false)</option>
                                </select>
                                <?php else: ?>
                                <input type="<?= $inputType ?>" 
                                       class="form-control" 
                                       name="<?= $column['column_name'] ?>" 
                                       placeholder="<?= $column['column_default'] ?>" 
                                       <?= $column['is_nullable'] === 'NO' ? 'required' : '' ?>>
                                <?php endif; ?>
                                
                                <div class="form-text small">
                                    <code><?= $column['data_type'] ?></code>
                                    <?php if ($column['column_default']): ?>
                                    <span class="ms-2">По умолчанию: <?= $column['column_default'] ?></span>
                                    <?php endif; ?>
                                </div>
                            </div>
                            <?php endforeach; ?>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-save me-1"></i> Сохранить
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- Bootstrap JS и кастомные скрипты -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    // Автоматическое выделение текста в SQL редакторе
    document.addEventListener('DOMContentLoaded', function() {
        const sqlTextarea = document.getElementById('sqlQuery');
        if (sqlTextarea) {
            sqlTextarea.focus();
        }
        
        // Инициализация всех тултипов
        const tooltips = document.querySelectorAll('[title]');
        tooltips.forEach(el => {
            new bootstrap.Tooltip(el);
        });
    });
    
    // Функции для работы с таблицей данных
    function editRow(button) {
        const row = button.closest('tr');
        const cells = row.querySelectorAll('td:not(:last-child)');
        
        cells.forEach(cell => {
            if (!cell.querySelector('input')) {
                const text = cell.textContent.trim();
                cell.innerHTML = `<input type="text" class="form-control form-control-sm" value="${text}">`;
            }
        });
        
        const actionsCell = row.querySelector('td:last-child');
        actionsCell.innerHTML = `
            <div class="btn-group btn-group-sm">
                <button class="btn btn-success" onclick="saveRow(this)">
                    <i class="fas fa-check"></i>
                </button>
                <button class="btn btn-secondary" onclick="cancelEdit(this)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    }
    
    function saveRow(button) {
        // Здесь будет AJAX запрос для сохранения изменений
        alert('Функция сохранения будет реализована позже');
        location.reload();
    }
    
    function cancelEdit(button) {
        location.reload();
    }
    
    function deleteRow(button) {
        if (confirm('Вы уверены, что хотите удалить эту запись?')) {
            // Здесь будет AJAX запрос для удаления
            alert('Функция удаления будет реализована позже');
            location.reload();
        }
    }
    
    // Подсказки для SQL
    const sqlExamples = {
        'property': 'SELECT * FROM property WHERE is_active = true ORDER BY property_id DESC LIMIT 10',
        'booking': 'SELECT b.*, g.first_name, g.last_name FROM booking b JOIN guest g ON b.guest_id = g.guest_id WHERE b.status = \'active\'',
        'guest': 'SELECT * FROM guest WHERE verified = true ORDER BY last_name, first_name',
        'payment': 'SELECT p.*, b.booking_number FROM payment p JOIN booking b ON p.booking_id = b.booking_id ORDER BY p.created_at DESC',
        'users': 'SELECT u.*, COALESCE(g.first_name, e.first_name) as first_name FROM users u LEFT JOIN guest g ON u.user_id = g.user_id LEFT JOIN employee e ON u.user_id = e.user_id'
    };
    
    // Автозаполнение SQL редактора при смене таблицы
    const currentTable = '<?= $currentTable ?>';
    if (currentTable && sqlExamples[currentTable]) {
        document.addEventListener('DOMContentLoaded', function() {
            const textarea = document.getElementById('sqlQuery');
            if (textarea && !textarea.value) {
                textarea.value = sqlExamples[currentTable];
            }
        });
    }
    
    // Безопасный режим для SQL редактора
    document.getElementById('safeMode')?.addEventListener('change', function(e) {
        const textarea = document.getElementById('sqlQuery');
        if (!e.target.checked) {
            if (!confirm('Выключая безопасный режим, вы разрешаете выполнение любых SQL запросов. Продолжить?')) {
                e.target.checked = true;
                return;
            }
            textarea.placeholder = 'Введите любой SQL запрос...';
        } else {
            textarea.placeholder = 'SELECT * FROM <?= $currentTable ?> LIMIT 10';
        }
    });
    </script>
</body>
</html>
