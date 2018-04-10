-- 创建数据库
CREATE DATABASE artsoDB CHARACTER SET 'utf8' COLLATE 'utf8_general_Ci';
USE artsoDB;

-- 创建表
CREATE TABLE xiangyaAuction(
    id INT AUTO_INCREMENT,
    name char(32),
    writer char(32),
    size char(32),
    era char(32),
    type char(32),
    expected_price char(32),

    real_priceRMB char(32),
    real_priceHKD char(32),
    real_priceUSD char(32),
    real_priceEUR char(32),

    special_performance char(32),
    auction_time char(32),
    auction_company char(32),
    auction char(32),
    url char(255),
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
