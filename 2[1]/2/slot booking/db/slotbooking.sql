-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for slotbooking
CREATE DATABASE IF NOT EXISTS `slotbooking` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `slotbooking`;

-- Dumping structure for table slotbooking.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(50) NOT NULL default '0',
  `password` varchar(50) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table slotbooking.admin: ~1 rows (approximately)
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `email`, `password`) VALUES
	(1, 'admin@gmail.com', '123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table slotbooking.bookings
CREATE TABLE IF NOT EXISTS `bookings` (
  `id` int(11) NOT NULL auto_increment,
  `bdate` varchar(50) NOT NULL default '0',
  `gender` varchar(50) NOT NULL default '0',
  `comitee` varchar(50) NOT NULL default '0',
  `status` varchar(50) NOT NULL default '0',
  `uid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_bookings_user` (`uid`),
  CONSTRAINT `FK_bookings_user` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table slotbooking.bookings: ~2 rows (approximately)
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` (`id`, `bdate`, `gender`, `comitee`, `status`, `uid`) VALUES
	(1, '2025-04-03', 'Male', 'ba123', 'Accepted', 1),
	(2, '2025-04-03', 'Male', 'ba123', 'Rejected', 1);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;

-- Dumping structure for table slotbooking.subadmin
CREATE TABLE IF NOT EXISTS `subadmin` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) default NULL,
  `regno` varchar(150) default NULL,
  `class` varchar(150) default NULL,
  `section` varchar(150) default NULL,
  `phone` varchar(150) default NULL,
  `email` varchar(150) default NULL,
  `password` varchar(150) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table slotbooking.subadmin: ~1 rows (approximately)
/*!40000 ALTER TABLE `subadmin` DISABLE KEYS */;
INSERT INTO `subadmin` (`id`, `name`, `regno`, `class`, `section`, `phone`, `email`, `password`) VALUES
	(1, 'john', 'abc123', 'a', 'c', '9874563214', 'john@gmail.com', '456');
/*!40000 ALTER TABLE `subadmin` ENABLE KEYS */;

-- Dumping structure for table slotbooking.user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `regno` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `password` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table slotbooking.user: ~1 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `name`, `regno`, `phone`, `email`, `password`) VALUES
	(1, 'abc', '123', '9874563214', 'abc@gmail.com', '123');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
