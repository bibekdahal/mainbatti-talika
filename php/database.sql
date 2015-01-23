-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 23, 2015 at 03:55 PM
-- Server version: 5.5.40-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mainbatti_talika`
--
CREATE DATABASE IF NOT EXISTS `mainbatti_talika` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `mainbatti_talika`;

-- --------------------------------------------------------

--
-- Table structure for table `routine`
--

DROP TABLE IF EXISTS `routine`;
CREATE TABLE IF NOT EXISTS `routine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table-id` int(11) NOT NULL,
  `group-id` int(11) NOT NULL,
  `day` char(11) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `routine`
--

INSERT INTO `routine` (`id`, `table-id`, `group-id`, `day`, `start`, `end`) VALUES
(1, 1, 1, 'Sunday', '02:00:00', '03:00:00'),
(2, 1, 1, 'Sunday', '03:00:00', '04:00:00'),
(3, 1, 1, 'Sunday', '03:00:00', '04:00:00');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
