DROP PROCEDURE IF EXISTS `getUserwithUsername`;

DELIMITER //

CREATE PROCEDURE getUserwithUsername(IN usr varchar(225))
BEGIN
	SELECT * from user where username = usr;
END //

DELIMITER ;