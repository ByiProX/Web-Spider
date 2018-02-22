-- CREATE DATABASE scrapyDB CHARACTER SET 'utf8' COLLATE 'utf8_general_Ci';
-- USE scrapyDB;

CREATE TABLE weather(
    id INT AUTO_INCREMENT,
    cityName char(12),
    week char(24),
    weather char(24),
    air char(24),
    img char(48),
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;
