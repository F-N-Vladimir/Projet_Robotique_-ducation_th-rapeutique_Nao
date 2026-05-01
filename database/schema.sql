CREATE DATABASE nao_db;

USE nao_db;

CREATE TABLE interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    age INT,
    question TEXT,
    reponse TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
