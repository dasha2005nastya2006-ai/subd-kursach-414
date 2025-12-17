<?php
// navbar.php - навигационная панель
?>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container-fluid">
        <a class="navbar-brand" href="index.php">
            <i class="fas fa-database"></i> Управление арендой
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="mainNavbar">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="index.php">
                        <i class="fas fa-home"></i> Главная
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="stats.php">
                        <i class="fas fa-chart-bar"></i> Статистика
                    </a>
                </li>
                
                <?php if (hasRole('admin') || hasRole('employee')): ?>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-tools"></i> Управление
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="?table=booking"><i class="fas fa-calendar"></i> Бронирования</a></li>
                        <li><a class="dropdown-item" href="?table=property"><i class="fas fa-home"></i> Объекты</a></li>
                        <li><a class="dropdown-item" href="?table=guest"><i class="fas fa-users"></i> Гости</a></li>
                        <li><a class="dropdown-item" href="?table=payment"><i class="fas fa-money-bill"></i> Платежи</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <?php if (hasRole('admin')): ?>
                        <li><a class="dropdown-item" href="?table=users"><i class="fas fa-user-cog"></i> Пользователи</a></li>
                        <li><a class="dropdown-item" href="?table=employee"><i class="fas fa-user-tie"></i> Сотрудники</a></li>
                        <?php endif; ?>
                    </ul>
                </li>
                <?php endif; ?>
                
                <?php if (hasRole('admin')): ?>
                <li class="nav-item">
                    <a class="nav-link text-warning" href="admin.php">
                        <i class="fas fa-crown"></i> Админ-панель
                    </a>
                </li>
                <?php endif; ?>
            </ul>
            
            <div class="navbar-nav">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle"></i> 
                        <?= htmlspecialchars($currentUser['first_name'] ?? 'Пользователь') ?>
                        <span class="badge bg-<?= 
                            ($_SESSION['role'] ?? 'guest') === 'admin' ? 'danger' : 
                            (($_SESSION['role'] ?? 'guest') === 'employee' ? 'primary' : 'success')
                        ?> ms-1">
                            <?= $_SESSION['role'] ?? 'guest' ?>
                        </span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <span class="dropdown-item-text">
                                <small class="text-muted"><?= htmlspecialchars($currentUser['email'] ?? '') ?></small>
                            </span>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item" href="profile.php">
                                <i class="fas fa-user-cog"></i> Профиль
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item text-danger" href="logout.php">
                                <i class="fas fa-sign-out-alt"></i> Выйти
                            </a>
                        </li>
                    </ul>
                </li>
            </div>
        </div>
    </div>
</nav>
