<?php
header("Content-Type: application/json");

// DEBUG (A désactiver quand tout marchera)
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/config_db.php';

$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

if ($conn->connect_error) {
    echo json_encode(["erreur" => "Connexion DB: " . $conn->connect_error]);
    exit;
}

// Lire JSON
$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

if (!$data) {
    echo json_encode(["erreur" => "JSON invalide", "recu" => $raw]);
    exit;
}

// Sécurisation et Récupération des données
$nom      = $conn->real_escape_string($data["nom"] ?? "");
$age      = (int)($data["age"] ?? 0);
$question = $conn->real_escape_string($data["question"] ?? "");
$reponse  = $conn->real_escape_string($data["reponse"] ?? "");
$type     = $data["type_data"] ?? "interaction"; // On récupère le type d'envoi

if (!$nom) {
    echo json_encode(["erreur" => "Nom manquant"]);
    exit;
}

// INSERT
if ($type === "nouveau_profil") {
    $photo = "faces/" . $nom . ".jpg";
    // On insère dans la table enfants
    $sql = "INSERT INTO enfants (nom, age, photo_path, date_creation) 
            VALUES ('$nom', $age, '$photo', NOW())";
} else {
    // CORRECTION ICI : On utilise $nom (qu'on a défini plus haut) 
    // et NOW() pour la date automatique de MySQL
    $sql = "INSERT INTO interactions (enfant_nom, question, reponse, date_interaction) 
            VALUES ('$nom', '$question', '$reponse', NOW())";
}

// EXECUTION
if ($conn->query($sql)) {
    echo json_encode(["success" => true]);
} else {
    echo json_encode([
        "erreur" => "SQL",
        "message" => $conn->error,
        "query" => $sql
    ]);
}

$conn->close();
?>
