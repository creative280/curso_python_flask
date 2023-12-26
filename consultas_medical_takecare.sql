CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    firstname VARCHAR(120),
    lastname VARCHAR(120),
    birth DATETIME,
    address VARCHAR(120),
    number VARCHAR(80),
    city VARCHAR(120),
    email VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(80),
);

ALTER TABLE user
ADD COLUMN is_admin BOOLEAN DEFAULT 0;


ALTER TABLE user
CHANGE firtname firstname VARCHAR(120);



CREATE TABLE post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(120),
    body VARCHAR(500),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);


INSERT INTO user (username, email, password) VALUES ('admin_ats', 'admin2@example.com', '123456789');

INSERT INTO post (id, title, body, timestamp, user_id) VALUES (1, 'post_title_example', 'Text example area for the post', NOW(),16);

-- Insertar más ejemplos
INSERT INTO post (id, title, body, timestamp, user_id) VALUES (2, 'Segundo Post', 'Contenido del segundo post', NOW(), 17);
INSERT INTO post (id, title, body, timestamp, user_id) VALUES (3, 'Tercer Post', 'Contenido del tercer post', NOW(), 18);
INSERT INTO post (id, title, body, timestamp, user_id) VALUES (4, 'Cuarto Post', 'Contenido del cuarto post', NOW(), 19);
INSERT INTO post (id, title, body, timestamp, user_id) VALUES (5, 'Quinto Post', 'Contenido del quinto post', NOW(), 16);
INSERT INTO post (id, title, body, timestamp, user_id) VALUES (6, 'Sexto Post', 'Contenido del sexto post', NOW(), 16);


SELECT * FROM user;

SELECT * FROM post;

ALTER TABLE user MODIFY COLUMN password VARCHAR(255);

ALTER TABLE post
MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

UPDATE user
SET is_admin = 1
WHERE id = 16;