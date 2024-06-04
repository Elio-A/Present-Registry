DROP PROCEDURE IF EXISTS `updateQuantity`//

DELIMITER //

CREATE PROCEDURE `updateQuantity`(IN pres INT, IN quant Int, IN usr INT)
BEGIN
	UPDATE present_list
    set quantity = quant
    where present_id = pres
    and user_id = usr
    LIMIT 1;

    if row_count() = 0 then
		  signal SQLSTATE '45000' SET message_text = "Error updating present quantity"
	END IF;
END //

DELIMTER ;