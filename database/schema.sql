CREATE DATABASE nao_db;

USE nao_db;

-- TABLE 1 : enfants
-- Stocke le profil et les statistiques de chaque enfant

CREATE TABLE enfants (
    id               INT          PRIMARY KEY,
    nom              VARCHAR(100) ,
    age              INT,
    photo_path       VARCHAR(255),
    date_creation    TIMESTAMP   ,
    nb_sessions      INT         ,
    score_moyen      INT         ,
    theme_difficile  VARCHAR(50) ,
    derniere_session DATETIME    
);


-- TABLE 2 : interactions
-- Stocke l'historique complet de toutes les interactions

CREATE TABLE interactions (
    id               INT       PRIMARY KEY,
    enfant_nom       VARCHAR(100),
    question         TEXT,
    reponse          TEXT,
    date_interaction TIMESTAMP  
);
