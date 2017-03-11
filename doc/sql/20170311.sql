ALTER TABLE `bgirl`.`page_content`
CHANGE COLUMN `category` `category` INT(11) NULL DEFAULT 0 COMMENT '类型' ,
CHANGE COLUMN `pic_id` `pic_id` INT(11) NULL DEFAULT 0 COMMENT '图片id' ;
