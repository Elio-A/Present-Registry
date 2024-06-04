CREATE PROCEDURE `addPresentToList`(IN user_id int, IN present_id int, IN quantity INT)
BEGIN
	IF Exists(select * from present_list p where p.user_id=user_id and p.present_id=present_id) then
		call addQuantity(present_id, quantity, user_id);
	ELSE
		INSERT INTO present_list (user_id, present_id, quantity) values (user_id, present_id, quantity);
	END IF;
END //