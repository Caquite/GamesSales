<?php
header('Content-Type: application/json');

$q = trim($_GET['q'] ?? '');
if (strlen($q) < 2) {
    echo json_encode([]);
    exit;
}

$type = $_GET['type'] ?? '';

$pdo = new PDO(
    'mysql:host=localhost;dbname=gamesale;charset=utf8',
    'root',
    '' 
);

if ($type === 'editeur') {
    $stmt = $pdo->prepare("SELECT DISTINCT id_editeur, editeur FROM editeur WHERE editeur LIKE ? LIMIT 10");
    $stmt->execute(["%$q%"]);
} elseif ($type === 'developpeur') {
    $stmt = $pdo->prepare("SELECT DISTINCT id_developpeur, developpeur FROM developpeur WHERE developpeur LIKE ? LIMIT 10");
    $stmt->execute(["%$q%"]);
} else {
    echo json_encode([]);
    exit;
}

echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));