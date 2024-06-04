DROP procedure IF EXISTS `addPresent`;

DELIMITER //
CREATE PROCEDURE `addPresent`(IN present_name VARCHAR(225), IN vendor VARCHAR(225), IN cost double)
BEGIN
	INSERT INTO present (present_name, vendor, cost) values (present_name, vendor, cost);
	select LAST_INSERT_ID();
END//

DELIMITER ;
