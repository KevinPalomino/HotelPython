-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 21-09-2025 a las 20:17:55
-- Versión del servidor: 8.0.31
-- Versión de PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel-python`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `camas`
--

DROP TABLE IF EXISTS `camas`;
CREATE TABLE IF NOT EXISTS `camas` (
  `idcamas` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `capacidad` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`idcamas`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `camas`
--

INSERT INTO `camas` (`idcamas`, `nombre`, `capacidad`) VALUES
(1, 'Sencilla', 1),
(2, 'Doble', 2),
(3, 'Queen', 2),
(4, 'King', 2),
(5, 'Litera', 1),
(6, 'Sofá cama', 1),
(7, 'Cama nido', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `idcategorias` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `descripcion` varchar(125) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`idcategorias`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`idcategorias`, `nombre`, `descripcion`) VALUES
(6, 'Sencilla', 'Habitación para una persona'),
(7, 'Doble', 'Habitación para dos personas'),
(8, 'Familiar', 'Ideal para familias pequeñas'),
(9, 'Suite', 'Espaciosa con amenidades premium'),
(10, 'Lujo', 'Habitación de alta gama con servicios exclusivos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias_inventario`
--

DROP TABLE IF EXISTS `categorias_inventario`;
CREATE TABLE IF NOT EXISTS `categorias_inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `categorias_inventario`
--

INSERT INTO `categorias_inventario` (`id`, `nombre`) VALUES
(1, 'Bebida'),
(2, 'Alimento'),
(3, 'Aseo'),
(4, 'Lencería'),
(5, 'utileria'),
(6, 'PRUEBA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `idclientes` int NOT NULL AUTO_INCREMENT,
  `departamento` varchar(45) DEFAULT NULL,
  `ciudad` varchar(45) DEFAULT NULL,
  `personas_cedula` bigint NOT NULL,
  `estado` varchar(255) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `justificacion` text,
  PRIMARY KEY (`idclientes`),
  KEY `fk_clientes_personas_idx` (`personas_cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`idclientes`, `departamento`, `ciudad`, `personas_cedula`, `estado`, `fecha`, `justificacion`) VALUES
(9, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(10, 'Santander', 'Barrancabermeja', 28070697, '', NULL, NULL),
(11, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(12, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(13, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(14, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(15, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(16, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(17, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(18, 'Santander', 'Barrancabermeja', 100528012, '', NULL, NULL),
(19, 'Santander', 'Barrancabermeja', 13213123, '', NULL, NULL),
(20, 'Santander', 'Barrancabermeja', 1005180469, '', NULL, NULL),
(21, 'Santander', 'Barrancabermeja', 10023231, '', NULL, NULL),
(22, '', '', 1000000, '', NULL, NULL),
(23, '', '', 11111111, '', NULL, NULL),
(24, 'santander', 'barranca', 1097185085, '', NULL, NULL),
(25, '', '', 12456789, '', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios`
--

DROP TABLE IF EXISTS `comentarios`;
CREATE TABLE IF NOT EXISTS `comentarios` (
  `idcomentarios` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `puntuacion` tinyint(1) DEFAULT NULL,
  `comentario` text,
  `clientes_idclientes` int NOT NULL,
  PRIMARY KEY (`idcomentarios`),
  KEY `fk_comentarios_clientes1_idx` (`clientes_idclientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consumos`
--

DROP TABLE IF EXISTS `consumos`;
CREATE TABLE IF NOT EXISTS `consumos` (
  `idconsumos` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `total` int DEFAULT NULL,
  `inventario_idinventario` int NOT NULL,
  `detalle_reserva_iddetalle_reserva` int NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`idconsumos`),
  KEY `fk_consumos_inventario1_idx` (`inventario_idinventario`),
  KEY `fk_consumos_detalle_reserva1_idx` (`detalle_reserva_iddetalle_reserva`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_reserva`
--

DROP TABLE IF EXISTS `detalle_reserva`;
CREATE TABLE IF NOT EXISTS `detalle_reserva` (
  `iddetalle_reserva` int NOT NULL AUTO_INCREMENT,
  `reservas_idreservas` int NOT NULL,
  `habitaciones_idhabitaciones` int NOT NULL,
  PRIMARY KEY (`iddetalle_reserva`),
  KEY `fk_detalle_reserva_reservas1_idx` (`reservas_idreservas`),
  KEY `fk_detalle_reserva_habitaciones1_idx` (`habitaciones_idhabitaciones`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `detalle_reserva`
--

INSERT INTO `detalle_reserva` (`iddetalle_reserva`, `reservas_idreservas`, `habitaciones_idhabitaciones`) VALUES
(22, 24, 16),
(23, 25, 16),
(24, 26, 17),
(25, 27, 16),
(26, 28, 18);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos`
--

DROP TABLE IF EXISTS `fotos`;
CREATE TABLE IF NOT EXISTS `fotos` (
  `idfotos` int NOT NULL AUTO_INCREMENT,
  `fotos` longblob,
  `habitaciones_idhabitaciones` int DEFAULT NULL,
  PRIMARY KEY (`idfotos`),
  KEY `fk_fotos_habitaciones1` (`habitaciones_idhabitaciones`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitaciones`
--

DROP TABLE IF EXISTS `habitaciones`;
CREATE TABLE IF NOT EXISTS `habitaciones` (
  `idhabitaciones` int NOT NULL AUTO_INCREMENT,
  `capacidad` int DEFAULT NULL,
  `estado` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT 'disponible',
  `precio` bigint DEFAULT NULL,
  `ventilador` tinyint(1) DEFAULT NULL,
  `aire_acondicionado` tinyint(1) DEFAULT NULL,
  `TV` tinyint(1) DEFAULT NULL,
  `tina` tinyint(1) DEFAULT NULL,
  `wifi` tinyint(1) DEFAULT NULL,
  `bar` tinyint(1) DEFAULT NULL,
  `aseo` tinyint(1) DEFAULT NULL,
  `caja_fuerte` tinyint(1) DEFAULT NULL,
  `categorias_idcategorias` int NOT NULL,
  `tipos_idtipo` int DEFAULT NULL,
  PRIMARY KEY (`idhabitaciones`),
  KEY `fk_habitaciones_categorias1_idx` (`categorias_idcategorias`),
  KEY `fk_tipo_habitacion` (`tipos_idtipo`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `habitaciones`
--

INSERT INTO `habitaciones` (`idhabitaciones`, `capacidad`, `estado`, `precio`, `ventilador`, `aire_acondicionado`, `TV`, `tina`, `wifi`, `bar`, `aseo`, `caja_fuerte`, `categorias_idcategorias`, `tipos_idtipo`) VALUES
(16, 2, '0', 75000, 1, 0, 1, 0, 1, 0, 1, 0, 6, 7),
(17, 6, '0', 300000, 0, 1, 1, 1, 1, 1, 1, 1, 9, 2),
(18, 4, '0', 150000, 0, 1, 1, 0, 1, 0, 1, 1, 7, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

DROP TABLE IF EXISTS `inventario`;
CREATE TABLE IF NOT EXISTS `inventario` (
  `idinventario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `categoria` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `descripcion` text,
  `precio` bigint DEFAULT NULL,
  PRIMARY KEY (`idinventario`),
  KEY `fk_categoria_inventario` (`categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`idinventario`, `nombre`, `categoria`, `cantidad`, `descripcion`, `precio`) VALUES
(1, 'frijol enlatado', 1, 15, 'comida procesada', 3000),
(4, 'Gaseosa', 1, 80, 'Gaseosas surtidas de 350ml', 2000),
(5, 'Jugo de fruta', 1, 60, 'Jugos en caja o botella', 2500),
(6, 'Snack surtido', 2, 50, 'Galletas, papas y otros snacks', 3000),
(7, 'Desayuno continental', 2, 20, 'Desayuno básico para servicio a la habitación', 12000),
(8, 'Jabón de baño', 3, 200, 'Jabón pequeño individual para huéspedes', 800),
(9, 'Champú', 3, 180, 'Botellitas de champú de cortesía', 1000),
(10, 'Papel higiénico', 3, 300, 'Rollo de papel higiénico estándar', 1200),
(11, 'Cepillo dental', 3, 100, 'Cepillos individuales desechables', 1000),
(12, 'Toalla de baño', 4, 100, 'Toallas blancas de algodón', 20000),
(13, 'Sábanas', 4, 80, 'Juego de sábanas para cama sencilla o doble', 30000),
(14, 'Funda de almohada', 4, 100, 'Fundas blancas estándar', 10000),
(15, 'Control remoto', 5, 30, 'Controles de TV de reemplazo', 15000),
(16, 'Bombillo LED', 5, 50, 'Bombillos para reemplazo en habitaciones', 8000),
(19, 'Doritos', 2, 12, '180 gr', 4000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

DROP TABLE IF EXISTS `pagos`;
CREATE TABLE IF NOT EXISTS `pagos` (
  `idpagos` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `metodo_pago` tinyint(1) DEFAULT NULL,
  `id_transferencia` varchar(45) DEFAULT NULL,
  `valor` varchar(45) DEFAULT NULL,
  `reservas_idreservas` int NOT NULL,
  `recepcionistas_idrecepcionistas` int NOT NULL,
  `referencia_pago` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idpagos`),
  KEY `fk_pagos_reservas1_idx` (`reservas_idreservas`),
  KEY `fk_pagos_recepcionistas1_idx` (`recepcionistas_idrecepcionistas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

DROP TABLE IF EXISTS `personas`;
CREATE TABLE IF NOT EXISTS `personas` (
  `cedula` bigint NOT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `telefono` bigint DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `correo` varchar(60) DEFAULT NULL,
  `contrasena` varchar(200) DEFAULT NULL,
  `roles_idroles` int NOT NULL,
  PRIMARY KEY (`cedula`),
  KEY `fk_personas_roles1_idx` (`roles_idroles`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`cedula`, `nombre`, `telefono`, `direccion`, `correo`, `contrasena`, `roles_idroles`) VALUES
(1000000, 'juan esteban pedroza', 310000000, 'Bucaramanga', 'juan@prueba.com', NULL, 2),
(10023231, 'frijol enlatado', 3154687234, NULL, 'frijol@gmail.com', NULL, 2),
(11111111, 'cliente_nuevo', 1111111, 'Barrancabermeja', 'cliente_nuevo@prueba.com', NULL, 2),
(12456789, 'Maye', 3214726895, 'CLL 70 #15n', 'maye@gmail.com', NULL, 2),
(13213123, 'Breyshell', 23123123, NULL, 'breyshell@gmail.com', NULL, 2),
(28070697, 'Cliente Nuevo nuevo', 3154687234, NULL, 'cliente@nuevo.com', NULL, 2),
(100500000, 'Daniela Villalba', 315000000, 'Santander', 'dani@prueba.com', 'scrypt:32768:8:1$ci1GUalOAUTzxIim$ece491c1a022dde74468985b7de9e44794c631a2429e8e3f95e4126627a4c6886fdd1acb1b4ee870955675ddf0310bf073e032c3ce7a4bbd0e26d12a503a1d4a', 3),
(100528012, 'Juan Esteban', 3154687234, NULL, 'esteban@gmail.com', NULL, 2),
(123456789, 'Alberto', 3214024325, 'CLL 28', 'alberto@gmail.com', 'scrypt:32768:8:1$j9lwUdUr2HXKETfw$edb87836a7a58fbda98f966318d84e061d380c79e4d2d6a55be5f04b9fdfad60953cd9ec202acaefd35fa1fb25a395f2984f1888052cac80b675f9438688313c', 3),
(1005180469, 'Kevin Armando Palomino Jolianis', 3160534614, NULL, 'kevinpalomino.jolianis@gmail.com', NULL, 2),
(1097185085, 'Juan Esteban Ruiz Peinado ', 3151803878, 'Cll 5', 'juru2967@gmail.com', 'scrypt:32768:8:1$w0pi0ccpvduhJMBP$2470c05c7c401b5950ce330d6c6516b059f52d36c0c625fa211f0fcbaa0e2eaf8f5a5e66f9d16028de79bb6e3f82f62c73842d29de52fa9e57b7c16c9ebf21ca', 3),
(1111111111, 'Lucdo', 3151803878, 'Cll 5', 'lucdo@gmail.com', NULL, 2),
(1234567890, 'Admin Principal', 3001234567, 'Oficina Central', 'admin@hotel.com', 'scrypt:32768:8:1$w0pi0ccpvduhJMBP$2470c05c7c401b5950ce330d6c6516b059f52d36c0c625fa211f0fcbaa0e2eaf8f5a5e66f9d16028de79bb6e3f82f62c73842d29de52fa9e57b7c16c9ebf21ca', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pqr`
--

DROP TABLE IF EXISTS `pqr`;
CREATE TABLE IF NOT EXISTS `pqr` (
  `idPQR` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `correo` varchar(45) DEFAULT NULL,
  `telefono` bigint DEFAULT NULL,
  `mensaje` text,
  `observacion` text,
  `estado` tinyint(1) DEFAULT NULL,
  `personas_cedula` bigint NOT NULL,
  PRIMARY KEY (`idPQR`),
  KEY `fk_pqr_personas1_idx` (`personas_cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recepcionistas`
--

DROP TABLE IF EXISTS `recepcionistas`;
CREATE TABLE IF NOT EXISTS `recepcionistas` (
  `idrecepcionistas` int NOT NULL AUTO_INCREMENT,
  `estado` tinyint(1) DEFAULT NULL,
  `personas_cedula` bigint NOT NULL,
  PRIMARY KEY (`idrecepcionistas`),
  KEY `fk_recepcionistas_personas1_idx` (`personas_cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `relacion_cama`
--

DROP TABLE IF EXISTS `relacion_cama`;
CREATE TABLE IF NOT EXISTS `relacion_cama` (
  `idrelacion_cama` int NOT NULL AUTO_INCREMENT,
  `camas_idcamas` int NOT NULL,
  `habitaciones_idhabitaciones` int NOT NULL,
  PRIMARY KEY (`idrelacion_cama`),
  KEY `fk_relacion_cama_camas1_idx` (`camas_idcamas`),
  KEY `fk_relacion_cama_habitaciones1_idx` (`habitaciones_idhabitaciones`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `relacion_cama`
--

INSERT INTO `relacion_cama` (`idrelacion_cama`, `camas_idcamas`, `habitaciones_idhabitaciones`) VALUES
(48, 1, 16),
(49, 1, 16),
(50, 2, 17),
(51, 2, 17),
(52, 2, 17),
(53, 2, 18),
(54, 2, 18);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

DROP TABLE IF EXISTS `reservas`;
CREATE TABLE IF NOT EXISTS `reservas` (
  `idreservas` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `checkin` datetime DEFAULT NULL,
  `checkout` datetime DEFAULT NULL,
  `comentario` text,
  `estado` tinyint(1) DEFAULT NULL,
  `abono` bigint DEFAULT NULL,
  `clientes_idclientes` int NOT NULL,
  `fecha_cancelacion` datetime DEFAULT NULL,
  `observacion` text,
  `cedula_usuario` bigint DEFAULT NULL,
  PRIMARY KEY (`idreservas`),
  KEY `fk_reservas_clientes1_idx` (`clientes_idclientes`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`idreservas`, `fecha`, `checkin`, `checkout`, `comentario`, `estado`, `abono`, `clientes_idclientes`, `fecha_cancelacion`, `observacion`, `cedula_usuario`) VALUES
(9, NULL, '2025-07-03 00:00:00', '2025-06-29 00:00:00', NULL, 3, 323232, 17, NULL, NULL, NULL),
(10, NULL, '2025-07-03 00:00:00', '2025-07-05 00:00:00', NULL, 1, 25000, 18, NULL, NULL, NULL),
(13, NULL, '2025-07-02 00:00:00', '2025-07-03 00:00:00', NULL, 1, 2323, 19, NULL, NULL, NULL),
(14, NULL, '2025-07-02 00:00:00', '2025-07-05 00:00:00', NULL, 1, 10000, 20, NULL, NULL, NULL),
(15, NULL, '2025-07-05 00:00:00', '2025-07-05 00:00:00', NULL, 1, 0, 21, NULL, NULL, NULL),
(16, NULL, '2025-09-15 00:00:00', '2025-09-17 00:00:00', NULL, 3, 50000, 22, NULL, NULL, NULL),
(17, NULL, '2025-09-15 00:00:00', '2025-09-17 00:00:00', NULL, 3, 0, 23, NULL, NULL, NULL),
(18, NULL, '2025-09-18 00:00:00', '2025-09-20 00:00:00', NULL, 3, 0, 9, NULL, NULL, NULL),
(19, NULL, '2025-09-20 00:00:00', '2025-09-21 00:00:00', NULL, 2, 0, 22, NULL, NULL, NULL),
(20, NULL, '2025-09-24 00:00:00', '2025-09-26 00:00:00', NULL, 2, 0, 18, NULL, NULL, NULL),
(21, NULL, '2025-09-20 00:00:00', '2025-09-22 00:00:00', NULL, 3, 0, 9, NULL, NULL, NULL),
(22, NULL, '2025-09-22 00:00:00', '2025-09-24 00:00:00', NULL, 2, 0, 21, NULL, NULL, NULL),
(23, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 2, 0, 21, NULL, NULL, NULL),
(24, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 3, 0, 18, NULL, NULL, NULL),
(25, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 2, 0, 25, NULL, NULL, NULL),
(26, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 2, 0, 19, NULL, NULL, NULL),
(27, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 3, 0, 18, NULL, NULL, NULL),
(28, NULL, '2025-09-21 00:00:00', '2025-09-22 00:00:00', NULL, 2, 0, 25, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `idroles` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idroles`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idroles`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Cliente'),
(3, 'Recepcionista');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_habitacion`
--

DROP TABLE IF EXISTS `tipos_habitacion`;
CREATE TABLE IF NOT EXISTS `tipos_habitacion` (
  `idtipo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`idtipo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `tipos_habitacion`
--

INSERT INTO `tipos_habitacion` (`idtipo`, `nombre`, `descripcion`) VALUES
(1, 'Sin tipo asignado', 'Tipo por defecto para registros antiguos'),
(2, 'Suite Ejecutiva', 'Habitación amplia con escritorio y zona de estar'),
(3, 'Doble Clásica', 'Para dos personas con cama doble y baño privado'),
(4, 'Familiar Premium', 'Espaciosa, ideal para grupos o familias grandes'),
(5, 'Estándar con Balcón', 'Habitación sencilla con balcón y vista al jardín'),
(6, 'Vista al Mar', 'Con acceso a terraza y vista directa al océano'),
(7, 'Accesible', 'Adaptada para personas con movilidad reducida');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `fk_clientes_personas` FOREIGN KEY (`personas_cedula`) REFERENCES `personas` (`cedula`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD CONSTRAINT `fk_comentarios_clientes1` FOREIGN KEY (`clientes_idclientes`) REFERENCES `clientes` (`idclientes`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `consumos`
--
ALTER TABLE `consumos`
  ADD CONSTRAINT `fk_consumos_detalle_reserva1` FOREIGN KEY (`detalle_reserva_iddetalle_reserva`) REFERENCES `detalle_reserva` (`iddetalle_reserva`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_consumos_inventario1` FOREIGN KEY (`inventario_idinventario`) REFERENCES `inventario` (`idinventario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_reserva`
--
ALTER TABLE `detalle_reserva`
  ADD CONSTRAINT `fk_detalle_reserva_habitaciones1` FOREIGN KEY (`habitaciones_idhabitaciones`) REFERENCES `habitaciones` (`idhabitaciones`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detalle_reserva_reservas1` FOREIGN KEY (`reservas_idreservas`) REFERENCES `reservas` (`idreservas`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `fotos`
--
ALTER TABLE `fotos`
  ADD CONSTRAINT `fk_fotos_habitaciones1` FOREIGN KEY (`habitaciones_idhabitaciones`) REFERENCES `habitaciones` (`idhabitaciones`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `habitaciones`
--
ALTER TABLE `habitaciones`
  ADD CONSTRAINT `fk_habitaciones_categorias1` FOREIGN KEY (`categorias_idcategorias`) REFERENCES `categorias` (`idcategorias`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tipo_habitacion` FOREIGN KEY (`tipos_idtipo`) REFERENCES `tipos_habitacion` (`idtipo`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `fk_categoria_inventario` FOREIGN KEY (`categoria`) REFERENCES `categorias_inventario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `fk_pagos_recepcionistas1` FOREIGN KEY (`recepcionistas_idrecepcionistas`) REFERENCES `recepcionistas` (`idrecepcionistas`),
  ADD CONSTRAINT `fk_pagos_reservas1` FOREIGN KEY (`reservas_idreservas`) REFERENCES `reservas` (`idreservas`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `personas`
--
ALTER TABLE `personas`
  ADD CONSTRAINT `fk_personas_roles1` FOREIGN KEY (`roles_idroles`) REFERENCES `roles` (`idroles`);

--
-- Filtros para la tabla `pqr`
--
ALTER TABLE `pqr`
  ADD CONSTRAINT `fk_pqr_personas1` FOREIGN KEY (`personas_cedula`) REFERENCES `personas` (`cedula`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `recepcionistas`
--
ALTER TABLE `recepcionistas`
  ADD CONSTRAINT `fk_recepcionistas_personas1` FOREIGN KEY (`personas_cedula`) REFERENCES `personas` (`cedula`);

--
-- Filtros para la tabla `relacion_cama`
--
ALTER TABLE `relacion_cama`
  ADD CONSTRAINT `fk_relacion_cama_camas1` FOREIGN KEY (`camas_idcamas`) REFERENCES `camas` (`idcamas`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_relacion_cama_habitaciones1` FOREIGN KEY (`habitaciones_idhabitaciones`) REFERENCES `habitaciones` (`idhabitaciones`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reservas_clientes1` FOREIGN KEY (`clientes_idclientes`) REFERENCES `clientes` (`idclientes`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
