ALTER TABLE `bgirl`.`group`
ADD COLUMN `supplier_id` VARCHAR(45) NULL DEFAULT 0 AFTER `thumb3`,
ADD COLUMN `shoot_time` DATE NOT NULL DEFAULT NULL AFTER `supplier_id`,
ADD COLUMN `group_no` VARCHAR(45) NULL AFTER `shoot_time`;