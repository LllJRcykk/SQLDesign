DROP TABLE tb_customer;
CREATE TABLE tb_customer
(
  Cid varchar2(10) NOT NULL primary key,
  CcompanyName  varchar2(30) NOT NULL,

  CcompanySName  varchar2(10) NOT NULL,
  CcompanyAddress varchar2(40) NOT NULL,
 
  CcompanyPhone varchar2(15) DEFAULT NULL,
  Cemail varchar2(10) DEFAULT NULL,
 
  CName varchar(10) NOT NULL,
  CtelPhone varchar(11) NOT NULL,
  
  other varchar(20) DEFAULT NULL
);

DROP TABLE tb_employee;
CREATE TABLE tb_employee
(
 Eid varchar2(10) NOT NULL primary key,
  EName varchar2(10) NOT NULL,
  EPas varchar2(10) NOT NULL,

  Elevel varchar2(2) NOT NULL,

  EtelPhone varchar2(11) NOT NULL,
 
  ESalary number(11) DEFAULT NULL,
 
  other  varchar2(20) DEFAULT NULL
);


DROP TABLE tb_good;
CREATE TABLE tb_good
(
 Gid varchar2(10) NOT NULL unique,
  GName varchar2(30) NOT NULL,

  GPay number NOT NULL,
  
  Cid varchar2(10) NOT NULL references tb_customer(Cid), 
  GIntroduction varchar2(40) DEFAULT NULL,
 
  other varchar2(20) DEFAULT NULL,

  PRIMARY KEY (Gid,Cid)
);


DROP TABLE tb_pay_main;
CREATE TABLE tb_pay_main
( Pid number(13) NOT NULL unique, 
  Eid varchar2(10) NOT NULL references tb_employee(Eid),
  Pcount number(11) NOT NULL,

  Ptotal  number NOT NULL,
  
  Pdate varchar2(8) NOT NULL,
 
  other varchar2(20) DEFAULT NULL,
 
  PRIMARY KEY (Pid, Eid)
);


DROP TABLE tb_pay_detail;
CREATE TABLE tb_pay_detail
(
  PDid number(14) NOT NULL,
  
  Pid  number(13) NOT NULL references tb_pay_main(Pid), 
  Gid varchar2(10) NOT NULL references tb_good(Gid),
  Pcount2 number(11) NOT NULL,
 
  Gpay number NOT NULL,
  
  total number NOT NULL,
  
  other varchar2(20) DEFAULT NULL,

  PRIMARY KEY (PDid, Pid, Gid)
);


DROP TABLE test1;
CREATE TABLE test1 
(
  id number(4) NOT NULL primary key,
   name varchar2(10) DEFAULT NULL
);



INSERT INTO tb_employee VALUES ('yg10004', 'wzm', '1', '00', '13300000000', '2000', '采购员');
INSERT INTO tb_pay_main VALUES ('1', 'yg10004', '1', '2', '20170703', '');
INSERT INTO tb_pay_main VALUES ('17', 'yg10004', '112', '24', '20170702', '13');
INSERT INTO tb_pay_main VALUES ('18', 'yg10004', '2', '2', '20170702', '14');
INSERT INTO tb_pay_main VALUES ('19', 'yg10004', '3', '55', '20170702', '15');
INSERT INTO test1 VALUES ('1', '23');
INSERT INTO test1 VALUES ('2', '23');
INSERT INTO test1 VALUES ('12', 'qwer');
commit;
