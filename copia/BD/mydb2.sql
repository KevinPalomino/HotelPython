-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`camas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`camas` (
  `idcamas` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idcamas`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categorias` (
  `idcategorias` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `descripcion` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idcategorias`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`roles` (
  `idroles` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`idroles`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`personas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`personas` (
  `cedula` BIGINT NOT NULL,
  `nombre` VARCHAR(150) NULL DEFAULT NULL,
  `telefono` BIGINT NULL DEFAULT NULL,
  `direccion` VARCHAR(100) NULL DEFAULT NULL,
  `correo` VARCHAR(60) NULL DEFAULT NULL,
  `contrasena` VARCHAR(45) NULL DEFAULT NULL,
  `roles_idroles` INT NOT NULL,
  PRIMARY KEY (`cedula`),
  INDEX `fk_personas_roles1_idx` (`roles_idroles` ASC) VISIBLE,
  CONSTRAINT `fk_personas_roles1`
    FOREIGN KEY (`roles_idroles`)
    REFERENCES `mydb`.`roles` (`idroles`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`clientes` (
  `idclientes` INT NOT NULL AUTO_INCREMENT,
  `departamento` VARCHAR(45) NULL DEFAULT NULL,
  `ciudad` VARCHAR(45) NULL DEFAULT NULL,
  `personas_cedula` BIGINT NOT NULL,
  `reservas_idreservas` INT NOT NULL,
  PRIMARY KEY (`idclientes`),
  INDEX `fk_clientes_personas_idx` (`personas_cedula` ASC) VISIBLE,
  CONSTRAINT `fk_clientes_personas`
    FOREIGN KEY (`personas_cedula`)
    REFERENCES `mydb`.`personas` (`cedula`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`comentarios` (
  `idcomentarios` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NULL DEFAULT NULL,
  `puntuacion` TINYINT(1) NULL DEFAULT NULL,
  `comentario` TEXT NULL DEFAULT NULL,
  `clientes_idclientes` INT NOT NULL,
  PRIMARY KEY (`idcomentarios`),
  INDEX `fk_comentarios_clientes1_idx` (`clientes_idclientes` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_clientes1`
    FOREIGN KEY (`clientes_idclientes`)
    REFERENCES `mydb`.`clientes` (`idclientes`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`habitaciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`habitaciones` (
  `idhabitaciones` INT NOT NULL,
  `tipo` TINYINT(1) NULL DEFAULT NULL,
  `capacidad` INT NULL DEFAULT NULL,
  `estado` TINYINT(1) NULL DEFAULT NULL,
  `precio` BIGINT NULL DEFAULT NULL,
  `ventilador` TINYINT(1) NULL DEFAULT NULL,
  `aire_acondicionado` TINYINT(1) NULL DEFAULT NULL,
  `TV` TINYINT(1) NULL DEFAULT NULL,
  `tina` TINYINT(1) NULL DEFAULT NULL,
  `wifi` TINYINT(1) NULL DEFAULT NULL,
  `bar` TINYINT(1) NULL DEFAULT NULL,
  `aseo` TINYINT(1) NULL DEFAULT NULL,
  `caja_fuerte` TINYINT(1) NULL DEFAULT NULL,
  `categorias_idcategorias` INT NOT NULL,
  PRIMARY KEY (`idhabitaciones`),
  INDEX `fk_habitaciones_categorias1_idx` (`categorias_idcategorias` ASC) VISIBLE,
  CONSTRAINT `fk_habitaciones_categorias1`
    FOREIGN KEY (`categorias_idcategorias`)
    REFERENCES `mydb`.`categorias` (`idcategorias`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`reservas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`reservas` (
  `idreservas` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NULL DEFAULT NULL,
  `checkin` DATETIME NULL DEFAULT NULL,
  `checkout` DATETIME NULL DEFAULT NULL,
  `comentario` TEXT NULL DEFAULT NULL,
  `estado` TINYINT(1) NULL DEFAULT NULL,
  `abono` BIGINT NOT NULL,
  `clientes_idclientes` INT NOT NULL,
  PRIMARY KEY (`idreservas`),
  INDEX `fk_reservas_clientes1_idx` (`clientes_idclientes` ASC) VISIBLE,
  CONSTRAINT `fk_reservas_clientes1`
    FOREIGN KEY (`clientes_idclientes`)
    REFERENCES `mydb`.`clientes` (`idclientes`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`detalle_reserva`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`detalle_reserva` (
  `iddetalle_reserva` INT NOT NULL AUTO_INCREMENT,
  `reservas_idreservas` INT NOT NULL,
  `habitaciones_idhabitaciones` INT NOT NULL,
  PRIMARY KEY (`iddetalle_reserva`),
  INDEX `fk_detalle_reserva_reservas1_idx` (`reservas_idreservas` ASC) VISIBLE,
  INDEX `fk_detalle_reserva_habitaciones1_idx` (`habitaciones_idhabitaciones` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_reserva_habitaciones1`
    FOREIGN KEY (`habitaciones_idhabitaciones`)
    REFERENCES `mydb`.`habitaciones` (`idhabitaciones`)
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_reserva_reservas1`
    FOREIGN KEY (`reservas_idreservas`)
    REFERENCES `mydb`.`reservas` (`idreservas`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`inventario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`inventario` (
  `idinventario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `categoria` TINYINT(1) NULL DEFAULT NULL,
  `cantidad` INT NULL DEFAULT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `precio` BIGINT NULL DEFAULT NULL,
  PRIMARY KEY (`idinventario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`consumos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`consumos` (
  `idconsumos` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NULL DEFAULT NULL,
  `cantidad` INT NULL DEFAULT NULL,
  `total` INT NULL DEFAULT NULL,
  `inventario_idinventario` INT NOT NULL,
  `detalle_reserva_iddetalle_reserva` INT NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  PRIMARY KEY (`idconsumos`),
  INDEX `fk_consumos_inventario1_idx` (`inventario_idinventario` ASC) VISIBLE,
  INDEX `fk_consumos_detalle_reserva1_idx` (`detalle_reserva_iddetalle_reserva` ASC) VISIBLE,
  CONSTRAINT `fk_consumos_detalle_reserva1`
    FOREIGN KEY (`detalle_reserva_iddetalle_reserva`)
    REFERENCES `mydb`.`detalle_reserva` (`iddetalle_reserva`)
    ON UPDATE CASCADE,
  CONSTRAINT `fk_consumos_inventario1`
    FOREIGN KEY (`inventario_idinventario`)
    REFERENCES `mydb`.`inventario` (`idinventario`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`fotos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`fotos` (
  `idfotos` INT NOT NULL AUTO_INCREMENT,
  `fotos` LONGBLOB NULL DEFAULT NULL,
  `habitaciones_idhabitaciones` INT NOT NULL,
  PRIMARY KEY (`idfotos`),
  INDEX `fk_fotos_habitaciones1_idx` (`habitaciones_idhabitaciones` ASC) VISIBLE,
  CONSTRAINT `fk_fotos_habitaciones1`
    FOREIGN KEY (`habitaciones_idhabitaciones`)
    REFERENCES `mydb`.`habitaciones` (`idhabitaciones`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`recepcionistas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`recepcionistas` (
  `idrecepcionistas` INT NOT NULL AUTO_INCREMENT,
  `estado` TINYINT(1) NULL DEFAULT NULL,
  `personas_cedula` BIGINT NOT NULL,
  PRIMARY KEY (`idrecepcionistas`),
  INDEX `fk_recepcionistas_personas1_idx` (`personas_cedula` ASC) VISIBLE,
  CONSTRAINT `fk_recepcionistas_personas1`
    FOREIGN KEY (`personas_cedula`)
    REFERENCES `mydb`.`personas` (`cedula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`pagos` (
  `idpagos` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `metodo_pago` TINYINT(1) NULL DEFAULT NULL,
  `id_transferencia` VARCHAR(45) NULL DEFAULT NULL,
  `valor` VARCHAR(45) NULL DEFAULT NULL,
  `reservas_idreservas` INT NOT NULL,
  `recepcionistas_idrecepcionistas` INT NOT NULL,
  PRIMARY KEY (`idpagos`),
  INDEX `fk_pagos_reservas1_idx` (`reservas_idreservas` ASC) VISIBLE,
  INDEX `fk_pagos_recepcionistas1_idx` (`recepcionistas_idrecepcionistas` ASC) VISIBLE,
  CONSTRAINT `fk_pagos_reservas1`
    FOREIGN KEY (`reservas_idreservas`)
    REFERENCES `mydb`.`reservas` (`idreservas`)
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pagos_recepcionistas1`
    FOREIGN KEY (`recepcionistas_idrecepcionistas`)
    REFERENCES `mydb`.`recepcionistas` (`idrecepcionistas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`pqr`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`pqr` (
  `idPQR` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL DEFAULT NULL,
  `correo` VARCHAR(45) NULL DEFAULT NULL,
  `telefono` BIGINT NULL DEFAULT NULL,
  `mensaje` TEXT NULL DEFAULT NULL,
  `observacion` TEXT NULL,
  `estado` TINYINT(1) NULL,
  `personas_cedula` BIGINT NOT NULL,
  PRIMARY KEY (`idPQR`),
  INDEX `fk_pqr_personas1_idx` (`personas_cedula` ASC) VISIBLE,
  CONSTRAINT `fk_pqr_personas1`
    FOREIGN KEY (`personas_cedula`)
    REFERENCES `mydb`.`personas` (`cedula`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`relacion_cama`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`relacion_cama` (
  `idrelacion_cama` INT NOT NULL AUTO_INCREMENT,
  `camas_idcamas` INT NOT NULL,
  `habitaciones_idhabitaciones` INT NOT NULL,
  PRIMARY KEY (`idrelacion_cama`),
  INDEX `fk_relacion_cama_camas1_idx` (`camas_idcamas` ASC) VISIBLE,
  INDEX `fk_relacion_cama_habitaciones1_idx` (`habitaciones_idhabitaciones` ASC) VISIBLE,
  CONSTRAINT `fk_relacion_cama_camas1`
    FOREIGN KEY (`camas_idcamas`)
    REFERENCES `mydb`.`camas` (`idcamas`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_relacion_cama_habitaciones1`
    FOREIGN KEY (`habitaciones_idhabitaciones`)
    REFERENCES `mydb`.`habitaciones` (`idhabitaciones`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
