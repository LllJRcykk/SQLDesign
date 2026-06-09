USE design;

-- =========================
-- 触发器部分
-- =========================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_pay_detail_before_insert $$
CREATE TRIGGER trg_pay_detail_before_insert
BEFORE INSERT ON tb_pay_detail
FOR EACH ROW
BEGIN
    SET NEW.total = NEW.Pcount2 * NEW.Gpay;
END $$

DROP TRIGGER IF EXISTS trg_pay_detail_before_update $$
CREATE TRIGGER trg_pay_detail_before_update
BEFORE UPDATE ON tb_pay_detail
FOR EACH ROW
BEGIN
    SET NEW.total = NEW.Pcount2 * NEW.Gpay;
END $$

DROP TRIGGER IF EXISTS trg_pay_detail_after_insert $$
CREATE TRIGGER trg_pay_detail_after_insert
AFTER INSERT ON tb_pay_detail
FOR EACH ROW
BEGIN
    UPDATE tb_pay_main
    SET
        Pcount = (
            SELECT IFNULL(SUM(Pcount2), 0)
            FROM tb_pay_detail
            WHERE Pid = NEW.Pid
        ),
        Ptotal = (
            SELECT IFNULL(SUM(total), 0)
            FROM tb_pay_detail
            WHERE Pid = NEW.Pid
        )
    WHERE Pid = NEW.Pid;
END $$

DROP TRIGGER IF EXISTS trg_pay_detail_after_update $$
CREATE TRIGGER trg_pay_detail_after_update
AFTER UPDATE ON tb_pay_detail
FOR EACH ROW
BEGIN
    UPDATE tb_pay_main
    SET
        Pcount = (
            SELECT IFNULL(SUM(Pcount2), 0)
            FROM tb_pay_detail
            WHERE Pid = OLD.Pid
        ),
        Ptotal = (
            SELECT IFNULL(SUM(total), 0)
            FROM tb_pay_detail
            WHERE Pid = OLD.Pid
        )
    WHERE Pid = OLD.Pid;

    UPDATE tb_pay_main
    SET
        Pcount = (
            SELECT IFNULL(SUM(Pcount2), 0)
            FROM tb_pay_detail
            WHERE Pid = NEW.Pid
        ),
        Ptotal = (
            SELECT IFNULL(SUM(total), 0)
            FROM tb_pay_detail
            WHERE Pid = NEW.Pid
        )
    WHERE Pid = NEW.Pid;
END $$

DROP TRIGGER IF EXISTS trg_pay_detail_after_delete $$
CREATE TRIGGER trg_pay_detail_after_delete
AFTER DELETE ON tb_pay_detail
FOR EACH ROW
BEGIN
    UPDATE tb_pay_main
    SET
        Pcount = (
            SELECT IFNULL(SUM(Pcount2), 0)
            FROM tb_pay_detail
            WHERE Pid = OLD.Pid
        ),
        Ptotal = (
            SELECT IFNULL(SUM(total), 0)
            FROM tb_pay_detail
            WHERE Pid = OLD.Pid
        )
    WHERE Pid = OLD.Pid;
END $$

DELIMITER ;

-- =========================
-- 视图部分
-- =========================

DROP VIEW IF EXISTS v_pay_info;
CREATE VIEW v_pay_info AS
SELECT
    pm.Pid AS pay_id,
    pm.Pdate AS pay_date,
    pm.Eid AS employee_id,
    e.EName AS employee_name,
    pm.Pcount AS main_total_count,
    pm.Ptotal AS main_total_amount,
    pd.PDid AS detail_id,
    pd.Gid AS good_id,
    g.GName AS good_name,
    pd.Pcount2 AS detail_count,
    pd.Gpay AS good_price,
    pd.total AS detail_total,
    pm.other AS main_other,
    pd.other AS detail_other
FROM tb_pay_main pm
JOIN tb_employee e ON pm.Eid = e.Eid
LEFT JOIN tb_pay_detail pd ON pm.Pid = pd.Pid
LEFT JOIN tb_good g ON pd.Gid = g.Gid;

DROP VIEW IF EXISTS v_good_customer_info;
CREATE VIEW v_good_customer_info AS
SELECT
    g.Gid AS good_id,
    g.GName AS good_name,
    g.GPay AS good_price,
    g.GIntroduction AS good_intro,
    c.Cid AS customer_id,
    c.CcompanyName AS customer_name,
    c.CcompanySName AS customer_short_name,
    c.CName AS contact_name,
    c.CtelPhone AS contact_phone
FROM tb_good g
JOIN tb_customer c ON g.Cid = c.Cid;

DROP VIEW IF EXISTS v_employee_purchase_stat;
CREATE VIEW v_employee_purchase_stat AS
SELECT
    e.Eid AS employee_id,
    e.EName AS employee_name,
    e.Elevel AS employee_level,
    COUNT(pm.Pid) AS purchase_count,
    IFNULL(SUM(pm.Pcount), 0) AS total_goods_count,
    IFNULL(SUM(pm.Ptotal), 0) AS total_purchase_amount
FROM tb_employee e
LEFT JOIN tb_pay_main pm ON e.Eid = pm.Eid
GROUP BY e.Eid, e.EName, e.Elevel;

-- =========================
-- 存储过程部分
-- =========================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_add_pay_detail $$
CREATE PROCEDURE sp_add_pay_detail(
    IN p_pid INT,
    IN p_gid VARCHAR(20),
    IN p_pcount2 INT,
    IN p_gpay DECIMAL(10,2),
    IN p_other VARCHAR(20)
)
BEGIN
    DECLARE v_total DECIMAL(10,2);

    SET v_total = p_pcount2 * p_gpay;

    INSERT INTO tb_pay_detail(Pid, Gid, Pcount2, Gpay, total, other)
    VALUES (p_pid, p_gid, p_pcount2, p_gpay, v_total, p_other);
END $$

DROP PROCEDURE IF EXISTS sp_delete_pay_detail $$
CREATE PROCEDURE sp_delete_pay_detail(
    IN p_pdid INT
)
BEGIN
    DELETE FROM tb_pay_detail
    WHERE PDid = p_pdid;
END $$

DROP PROCEDURE IF EXISTS sp_query_pay_main_by_date_range $$
CREATE PROCEDURE sp_query_pay_main_by_date_range(
    IN p_start_date VARCHAR(8),
    IN p_end_date VARCHAR(8)
)
BEGIN
    SELECT *
    FROM tb_pay_main
    WHERE Pdate BETWEEN p_start_date AND p_end_date
    ORDER BY Pid DESC;
END $$

DROP PROCEDURE IF EXISTS sp_query_pay_detail_by_pid $$
CREATE PROCEDURE sp_query_pay_detail_by_pid(
    IN p_pid INT
)
BEGIN
    SELECT
        pm.Pid,
        pm.Pdate,
        pm.Eid,
        e.EName,
        pd.PDid,
        pd.Gid,
        g.GName,
        pd.Pcount2,
        pd.Gpay,
        pd.total,
        pm.Pcount,
        pm.Ptotal
    FROM tb_pay_main pm
    JOIN tb_employee e ON pm.Eid = e.Eid
    LEFT JOIN tb_pay_detail pd ON pm.Pid = pd.Pid
    LEFT JOIN tb_good g ON pd.Gid = g.Gid
    WHERE pm.Pid = p_pid;
END $$

DELIMITER ;