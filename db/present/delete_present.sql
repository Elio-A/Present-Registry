DROP PROCEDURE IF EXISTS `delete_present`

DELIMITER //

CREATE PROCEDURE delete_present(IN pres INT)
BEGIN
	delete from present where present_id = pres;
END //

DELIMITER ;
