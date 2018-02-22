-- 创建数据库
CREATE DATABASE scrapyDB CHARACTER SET 'utf8' COLLATE 'utf8_general_Ci';
USE scrapyDB;

-- 创建表
CREATE TABLE weather(
    id INT AUTO_INCREMENT,
    cityName char(12),
    week char(24),
    weather char(24),
    air char(24),
    img char(255),
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- 创建普通用户，在该项目中直接使用的root用户，以下仅供参考

-- 创建一个用户名为crawlUSER的远程用户，该用户只能远程登录，不能本地登录
INSERT INTO mysql.user(Host,User,Password)
    VALUES('%','crawlUSER',password("wangkunxiang"));

-- 创建一个用户名为crawlUSER的本地用户，该用户只能本地登录，不能远程登录
INSERT INTO mysql.user(Host,User,Password)
    VALUES('localhost','crawlUSER',password("wangkunxiang"));

-- 以下两条命令赋予了crawlUSER用户管理scrapyDB数据库的所有权限
GRANT all privileges ON scrapyDB.* to crawlUSER@all IDENTIFIED BY 'wangkunxiang';

GRANT all privileges ON scrapyDB.* to crawlUSER@localhost IDENTIFIED BY 'wangkunxiang';
