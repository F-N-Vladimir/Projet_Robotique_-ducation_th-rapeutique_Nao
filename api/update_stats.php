<?php
header("Content-Type: application/json");
ini_set('display_errors', 1);
error_reporting(E_ALL);
require_once __DIR__ . '/config_db.php';

$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) {
    echo json_encode(["erreur" => "Connexion : " . $conn->connect_error]);
    exit;
}

$data = json_decode(file_get_contents("php://input"), true);
if (!$data) {
    echo json_encode(["erreur" => "JSON invalide"]);
    exit;
}

$nom        = $conn->real_escape_string($data["nom"]             ?? "");
$score_quiz = (int)($data["score_quiz"]                          ?? 0);
$total      = (int)($data["total_questions"]                     ?? 1);
$theme      = $conn->real_escape_string($data["theme"]           ?? "hypoglycemie");
$nb_erreurs = (int)($data["nb_erreurs"]                          ?? 0);
$date       = $conn->real_escape_string($data["date"]            ?? date("Y-m-d H:i:s"));

if (!$nom) {
    echo json_encode(["erreur" => "Nom manquant"]);
    exit;
}

$res    = $conn->query("SELECT * FROM enfants WHERE nom = '$nom'");
$enfant = $res ? $res->fetch_assoc() : null;

if (!$enfant) {
    $conn->query("INSERT INTO enfants (nom, nb_sessions, score_moyen, theme_difficile)
                  VALUES ('$nom', 0, 0, 'aucun')");
    $res2   = $conn->query("SELECT * FROM enfants WHERE nom = '$nom'");
    $enfant = $res2->fetch_assoc();
}

$ancien_score  = (int)($enfant["score_moyen"] ?? 0);
$nb_sessions   = (int)($enfant["nb_sessions"] ?? 0);
$score_pct     = $total > 0 ? round(($score_quiz / $total) * 100) : 0;
$nouveau_score = $nb_sessions > 0
    ? round(($ancien_score * $nb_sessions + $score_pct) / ($nb_sessions + 1))
    : $score_pct;

$theme_difficile = $enfant["theme_difficile"] ?? "aucun";
if ($nb_erreurs >= 1) {
    $theme_difficile = $theme;
}

$nouvelles_sessions = $nb_sessions + 1;
$sql = "UPDATE enfants SET
    nb_sessions      = $nouvelles_sessions,
    score_moyen      = $nouveau_score,
    theme_difficile  = '$theme_difficile',
    derniere_session = '$date'
WHERE nom = '$nom'";

if ($conn->query($sql)) {
    echo json_encode([
        "success"          => true,
        "nom"              => $nom,
        "nb_sessions"      => $nouvelles_sessions,
        "score_moyen"      => $nouveau_score,
        "theme_difficile"  => $theme_difficile,
        "derniere_session" => $date
    ]);
} else {
    echo json_encode(["erreur" => "UPDATE : " . $conn->error]);
}
$conn->close();
?>
