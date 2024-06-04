CREATE TABLE `present_list` (
  `list` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `present_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`list`),
  KEY `present_id_idx` (`present_id`),
  KEY `list_id_idx` (`user_id`),
  CONSTRAINT `present_id` FOREIGN KEY (`present_id`) REFERENCES `present` (`present_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
)//