-- Проверяем наличие базы данных и создаем её только если не существует
CREATE DATABASE IF NOT EXISTS research;

-- Проверяем существование пользователя и создаем его при необходимости
CREATE USER IF NOT EXISTS 'testuser'@'%' IDENTIFIED BY 'testpassword';

-- Даем все привилегии на базу данных research
GRANT ALL PRIVILEGES ON research.* TO 'testuser'@'%';

-- Применяем привилегии
FLUSH PRIVILEGES;

USE research;

-- DROP TABLE IF EXISTS test;

CREATE TABLE IF NOT EXISTS test(
    id int AUTO_INCREMENT PRIMARY KEY,
    code varchar(100),
    name varchar(200)
);

INSERT INTO 
    test(code, name) 
VALUES
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('10', 'amount');
