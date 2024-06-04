DROP PROCEDURE IF EXISTS `getPresent`;

DELIMITER //

CREATE PROCEDURE getPresent(IN pres INT)
BEGIN
	Select * from present where present_id = pres;
END //

DELIMITER ;
