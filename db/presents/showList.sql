DROP PROCEDURE IF EXISTS `showList`;

DELIMITER //

CREATE PROCEDURE `showList`(IN usr int)
BEGIN
	SELECT present_ID, present_name, cost, SUM(quantity) as quantity from present_list natural join present where user_id = usr Group By present_ID;
END //

DELIMITER ;