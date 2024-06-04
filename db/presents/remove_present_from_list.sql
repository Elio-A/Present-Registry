drop procedure if exists `remove_present_from_list`

delimiter //

CREATE PROCEDURE `remove_present_from_list`(IN present INT, IN usr INT)
BEGIN
	DELETE from present_list where present_id = present and user_id = usr LIMIT 1;
END //

delimiter ;
