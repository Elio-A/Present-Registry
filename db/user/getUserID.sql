DROP PROCEDURE IF EXISTS `getUserID`;

DELIMITER //

CREATE PROCEDURE `getUserID`(IN username VARCHAR(225))
BEGIN
	SELECT user_id from user u where u.username = username;
END //

DELIMITER ;
