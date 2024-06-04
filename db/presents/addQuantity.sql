create procedure `addQuantity`(IN pres INT, IN quant INT, IN usr INT)
BEGIN
    update present_list
    set quantity = (quantity + quant)
    where present_id = pres
    and user_id = usr;

    if row_count() = 0 then
        signal SQLSTATE '45000' set message_text = 'Error adding Present';
    END IF;
END //