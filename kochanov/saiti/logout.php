sudo tee /var/www/html/rental_simple/logout.php << 'EOF'
<?php
// logout.php
session_start();
session_destroy();
header('Location: login.php');
exit;
?>
EOF
