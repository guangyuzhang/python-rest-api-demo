-- MyEMS System Database

-- ---------------------------------------------------------------------------------------------------------------------
-- Schema myems_demo_db
-- ---------------------------------------------------------------------------------------------------------------------
DROP DATABASE IF EXISTS `myems_demo_db` ;
CREATE DATABASE IF NOT EXISTS `myems_demo_db` ;
USE `myems_demo_db` ;


-- ---------------------------------------------------------------------------------------------------------------------
-- Table `myems_demo_db`.`tbl_meters`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `myems_demo_db`.`tbl_meters` ;

CREATE TABLE IF NOT EXISTS `myems_demo_db`.`tbl_meters` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `uuid` CHAR(36) NOT NULL,
  `description` VARCHAR(255),
  PRIMARY KEY (`id`));
CREATE INDEX `tbl_meters_index_1` ON  `myems_demo_db`.`tbl_meters`   (`name`);
-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `myems_demo_db`.`tbl_meters`
-- ---------------------------------------------------------------------------------------------------------------------
 START TRANSACTION;
 USE `myems_demo_db`;

 INSERT INTO `myems_demo_db`.`tbl_meters`
 (`id`, `name`, `uuid`, `description`)
 VALUES
 (1, 'Meter1', '5ca47bc5-22c2-47fc-b906-33222191ea40', 'meter1'),
 (2, 'Meter2', '5ca47bc5-22c2-47fc-b906-33222191ea40', 'meter2'),
 (3, 'Meter3', '6db58cd6-33d3-58ed-a095-22333202fb51', null);

 COMMIT;
