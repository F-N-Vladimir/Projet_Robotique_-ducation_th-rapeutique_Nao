CREATE DATABASE nao_db;

USE nao_db;

-- TABLE 1 : enfants
-- Stocke le profil et les statistiques de chaque enfant

CREATE TABLE IF NOT EXISTS enfants (
    id               INT          AUTO_INCREMENT PRIMARY KEY,
    nom              VARCHAR(100) NOT NULL,
    age              INT,
    photo_path       VARCHAR(255),
    date_creation    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    nb_sessions      INT          DEFAULT 0,
    score_moyen      INT          DEFAULT 0,
    theme_difficile  VARCHAR(50)  DEFAULT 'aucun',
    derniere_session DATETIME     DEFAULT NULL
);


-- TABLE 2 : interactions
-- Stocke l'historique complet de toutes les interactions

CREATE TABLE IF NOT EXISTS interactions (
    id               INT          AUTO_INCREMENT PRIMARY KEY,
    enfant_nom       VARCHAR(100),
    question         TEXT,
    reponse          TEXT,
    date_interaction TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
