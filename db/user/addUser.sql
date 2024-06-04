DROP procedure IF EXISTS 'addUser';

DELIMITER //
CREATE PROCEDURE addUser (IN username VARCHAR(225))
BEGIN
	INSERT INTO user (username) values (username);
END//

DELIMITER ;
