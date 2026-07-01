-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2026 at 03:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `boat_booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `seats`
--

CREATE TABLE `seats` (
  `id` int(11) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `meal_preference` varchar(50) DEFAULT NULL,
  `meal_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `seats`
--

INSERT INTO `seats` (`id`, `type`, `price`, `status`, `user_name`, `meal_preference`, `meal_id`) VALUES
(1, 'Luxury', 24575, 'booked', 'Nishant', 'Veg Thali', NULL),
(2, 'Standard', 16749, 'booked', 'Sakshi', NULL, NULL),
(3, 'Standard', 19610, 'booked', 'Anushka', 'Veg Thali', NULL),
(4, 'Standard', 17798, 'booked', 'Soham', 'Non-Veg Thali', NULL),
(5, 'Luxury', 26808, 'available', NULL, NULL, NULL),
(6, 'Standard', 15164, 'available', NULL, NULL, NULL),
(7, 'Luxury', 22313, 'available', NULL, NULL, NULL),
(8, 'Luxury', 25142, 'available', NULL, NULL, NULL),
(9, 'Standard', 17425, 'available', NULL, NULL, NULL),
(10, 'Luxury', 28770, 'available', NULL, NULL, NULL),
(11, 'Economy', 5737, 'available', NULL, NULL, NULL),
(12, 'Economy', 5405, 'available', NULL, NULL, NULL),
(13, 'Economy', 9817, 'booked', 'Rutuja', 'Veg Thali', NULL),
(14, 'Upper', 13720, 'booked', 'Prathamesh', NULL, NULL),
(15, 'Economy', 7867, 'available', NULL, NULL, NULL),
(16, 'Economy', 9884, 'available', NULL, NULL, NULL),
(17, 'Upper', 12507, 'available', NULL, NULL, NULL),
(18, 'Upper', 11377, 'available', NULL, NULL, NULL),
(19, 'Upper', 14362, 'available', NULL, NULL, NULL),
(20, 'Upper', 12680, 'available', NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `seats`
--
ALTER TABLE `seats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_meal` (`meal_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `seats`
--
ALTER TABLE `seats`
  ADD CONSTRAINT `fk_meal` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
