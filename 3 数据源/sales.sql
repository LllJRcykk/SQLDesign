-- -----------------------------------------------------
-- 修正建议：使用 DROP TABLE IF EXISTS ... 避免在表不存在时报错
-- -----------------------------------------------------

DROP TABLE IF EXISTS tb_pay_detail;
DROP TABLE IF EXISTS tb_pay_main;
DROP TABLE IF EXISTS tb_good;
DROP TABLE IF EXISTS tb_customer;
DROP TABLE IF EXISTS tb_employee;
DROP TABLE IF EXISTS test1;


-- -----------------------------------------------------
-- 客户/供应商表 (tb_customer)
-- -----------------------------------------------------
CREATE TABLE tb_customer
(
  Cid VARCHAR(20) NOT NULL PRIMARY KEY,  -- 客户编号，根据课设要求gys+4位数字，长度设为20更安全
  CcompanyName  VARCHAR(30) NOT NULL,
  CcompanySName  VARCHAR(10) NOT NULL,
  CcompanyAddress VARCHAR(40) NOT NULL,
  CcompanyPhone VARCHAR(15) DEFAULT NULL,
  Cemail VARCHAR(30) DEFAULT NULL,       -- Email地址可能较长，建议增加长度
  CName VARCHAR(10) NOT NULL,
  CtelPhone VARCHAR(11) NOT NULL,
  other VARCHAR(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 员工表 (tb_employee)
-- -----------------------------------------------------
CREATE TABLE tb_employee
(
  Eid VARCHAR(20) NOT NULL PRIMARY KEY, -- 员工编号，根据课设要求yg+4位数字，长度设为20更安全
  EName VARCHAR(10) NOT NULL,
  EPas VARCHAR(10) NOT NULL,
  Elevel VARCHAR(2) NOT NULL,
  EtelPhone VARCHAR(11) NOT NULL,
  ESalary DECIMAL(10, 2) DEFAULT NULL, -- 使用DECIMAL存储工资、金额，避免精度丢失
  other  VARCHAR(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 商品表 (tb_good)
-- 修正：Gid应作为唯一主键，Cid是外键
-- -----------------------------------------------------
CREATE TABLE tb_good
(
  Gid VARCHAR(20) NOT NULL PRIMARY KEY, -- 商品编号，根据课设要求sp+8位数字，长度设为20更安全
  GName VARCHAR(30) NOT NULL,
  GPay DECIMAL(10, 2) NOT NULL,         -- 使用DECIMAL存储单价
  Cid VARCHAR(20) NOT NULL,
  GIntroduction VARCHAR(40) DEFAULT NULL,
  other VARCHAR(20) DEFAULT NULL,
  CONSTRAINT fk_good_customer FOREIGN KEY (Cid) REFERENCES tb_customer(Cid) -- 标准外键约束
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 采购主表 (tb_pay_main)
-- 修正：Pid应作为唯一主键，Eid是外键。使用AUTO_INCREMENT实现ID自增
-- -----------------------------------------------------
CREATE TABLE tb_pay_main
(
  Pid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, -- 使用INT AUTO_INCREMENT作为主键更合理
  Eid VARCHAR(20) NOT NULL,
  Pcount INT NOT NULL,
  Ptotal DECIMAL(10, 2) NOT NULL,             -- 使用DECIMAL存储总价
  Pdate VARCHAR(8) NOT NULL,
  other VARCHAR(20) DEFAULT NULL,
  CONSTRAINT fk_pay_main_employee FOREIGN KEY (Eid) REFERENCES tb_employee(Eid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 采购明细表 (tb_pay_detail)
-- -----------------------------------------------------
CREATE TABLE tb_pay_detail
(
  PDid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, -- 使用INT AUTO_INCREMENT作为明细主键
  Pid  INT NOT NULL,
  Gid VARCHAR(20) NOT NULL,
  Pcount2 INT NOT NULL,
  Gpay DECIMAL(10, 2) NOT NULL,
  total DECIMAL(10, 2) NOT NULL,
  other VARCHAR(20) DEFAULT NULL,
  CONSTRAINT fk_detail_main FOREIGN KEY (Pid) REFERENCES tb_pay_main(Pid),
  CONSTRAINT fk_detail_good FOREIGN KEY (Gid) REFERENCES tb_good(Gid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 测试表 (test1)
-- -----------------------------------------------------
CREATE TABLE test1 
(
  id INT NOT NULL PRIMARY KEY,
  name VARCHAR(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 插入数据
-- 注意：因为tb_pay_main的Pid已改为自增，插入时可不指定或指定为NULL
-- -----------------------------------------------------
INSERT INTO tb_employee (Eid, EName, EPas, Elevel, EtelPhone, ESalary, other) VALUES ('yg10004', 'wzm', '1', '00', '13300000000', 2000.00, '采购员');

-- 插入主表时，数据库会自动分配Pid
INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) VALUES ('yg10004', 1, 2.00, '20170703', '');
INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) VALUES ('yg10004', 112, 24.00, '20170702', '13');
INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) VALUES ('yg10004', 2, 2.00, '20170702', '14');
INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) VALUES ('yg10004', 3, 55.00, '20170702', '15');

INSERT INTO test1 (id, name) VALUES (1, '23');
INSERT INTO test1 (id, name) VALUES (2, '23');
INSERT INTO test1 (id, name) VALUES (12, 'qwer');

-- 提交事务，在很多客户端中是自动的，但显式写出是好习惯
COMMIT;