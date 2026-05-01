<?php
header("Content-Type: application/json");
require_once __DIR__ . '/config_db.php';

$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) {
    echo json_encode(["erreur" => $conn->connect_error]);
    exit;
}

$nom = $conn->real_escape_string($_GET["nom"] ?? "");
if (!$nom) {
    echo json_encode(["erreur" => "Parametre nom manquant"]);
    exit;
}

$res    = $conn->query("SELECT * FROM enfants WHERE nom = '$nom'");
$enfant = $res ? $res->fetch_assoc() : null;

if (!$enfant) {
    echo json_encode([
        "nom"              => $nom,
        "nb_sessions"      => 0,
        "score_moyen"      => 0,
        "theme_difficile"  => "aucun",
        "derniere_session" => "jamais"
    ]);
} else {
    echo json_encode([
        "nom"              => $enfant["nom"],
        "nb_sessions"      => (int)$enfant["nb_sessions"],
        "score_moyen"      => (int)$enfant["score_moyen"],
        "theme_difficile"  => $enfant["theme_difficile"],
        "derniere_session" => $enfant["derniere_session"] ?? "jamais"
    ]);
}
$conn->close();
?>
