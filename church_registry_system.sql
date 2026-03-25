-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2026 at 06:17 AM
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
-- Database: `church_registry_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `baptism_details`
--

CREATE TABLE `baptism_details` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) DEFAULT NULL,
  `father_name` varchar(150) DEFAULT NULL,
  `mother_name` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `communion_details`
--

CREATE TABLE `communion_details` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `confirmation_details`
--

CREATE TABLE `confirmation_details` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) DEFAULT NULL,
  `confirmation_name` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `last_rites_details`
--

CREATE TABLE `last_rites_details` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) DEFAULT NULL,
  `condition_notes` text DEFAULT NULL,
  `family_contact` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `marriage_details`
--

CREATE TABLE `marriage_details` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) DEFAULT NULL,
  `spouse_name` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `suffix` varchar(20) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `gender` enum('male','female') DEFAULT NULL,
  `civil_status` enum('single','married','widowed','separated') DEFAULT NULL,
  `address` text DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `pledge_id` int(11) NOT NULL,
  `amount_paid` decimal(10,2) NOT NULL,
  `payment_date` date NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pledges`
--

CREATE TABLE `pledges` (
  `id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `amount_promised` decimal(10,2) NOT NULL,
  `due_date` date DEFAULT NULL,
  `status` enum('unpaid','partial','paid') DEFAULT 'unpaid',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `pledge_summary`
-- (See below for the actual view)
--
CREATE TABLE `pledge_summary` (
`id` int(11)
,`member_id` int(11)
,`amount_promised` decimal(10,2)
,`total_paid` decimal(32,2)
,`balance` decimal(33,2)
);

-- --------------------------------------------------------

--
-- Table structure for table `print_logs`
--

CREATE TABLE `print_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `record_type` enum('member','sacrament','pledge') DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `printed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sacraments`
--

CREATE TABLE `sacraments` (
  `id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `sacrament_type` enum('baptism','confirmation','communion','marriage','last_rites') NOT NULL,
  `date_received` date NOT NULL,
  `officiant_name` varchar(150) DEFAULT NULL,
  `place` varchar(150) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sacrament_participants`
--

CREATE TABLE `sacrament_participants` (
  `id` int(11) NOT NULL,
  `sacrament_id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `role` enum('godfather','godmother','sponsor','witness') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `role` enum('admin','staff') DEFAULT 'staff',
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure for view `pledge_summary`
--
DROP TABLE IF EXISTS `pledge_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `pledge_summary`  AS SELECT `p`.`id` AS `id`, `p`.`member_id` AS `member_id`, `p`.`amount_promised` AS `amount_promised`, ifnull(sum(`pm`.`amount_paid`),0) AS `total_paid`, `p`.`amount_promised`- ifnull(sum(`pm`.`amount_paid`),0) AS `balance` FROM (`pledges` `p` left join `payments` `pm` on(`p`.`id` = `pm`.`pledge_id`)) GROUP BY `p`.`id` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `baptism_details`
--
ALTER TABLE `baptism_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sacrament_id` (`sacrament_id`);

--
-- Indexes for table `communion_details`
--
ALTER TABLE `communion_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sacrament_id` (`sacrament_id`);

--
-- Indexes for table `confirmation_details`
--
ALTER TABLE `confirmation_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sacrament_id` (`sacrament_id`);

--
-- Indexes for table `last_rites_details`
--
ALTER TABLE `last_rites_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sacrament_id` (`sacrament_id`);

--
-- Indexes for table `marriage_details`
--
ALTER TABLE `marriage_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sacrament_id` (`sacrament_id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_member_name` (`last_name`,`first_name`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_payment_pledge` (`pledge_id`);

--
-- Indexes for table `pledges`
--
ALTER TABLE `pledges`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_pledge_member` (`member_id`);

--
-- Indexes for table `print_logs`
--
ALTER TABLE `print_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_print_user` (`user_id`);

--
-- Indexes for table `sacraments`
--
ALTER TABLE `sacraments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_sacrament_member` (`member_id`);

--
-- Indexes for table `sacrament_participants`
--
ALTER TABLE `sacrament_participants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_participant_sacrament` (`sacrament_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `baptism_details`
--
ALTER TABLE `baptism_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `communion_details`
--
ALTER TABLE `communion_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `confirmation_details`
--
ALTER TABLE `confirmation_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `last_rites_details`
--
ALTER TABLE `last_rites_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `marriage_details`
--
ALTER TABLE `marriage_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pledges`
--
ALTER TABLE `pledges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `print_logs`
--
ALTER TABLE `print_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sacraments`
--
ALTER TABLE `sacraments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sacrament_participants`
--
ALTER TABLE `sacrament_participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `baptism_details`
--
ALTER TABLE `baptism_details`
  ADD CONSTRAINT `fk_baptism_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `communion_details`
--
ALTER TABLE `communion_details`
  ADD CONSTRAINT `fk_communion_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `confirmation_details`
--
ALTER TABLE `confirmation_details`
  ADD CONSTRAINT `fk_confirmation_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `last_rites_details`
--
ALTER TABLE `last_rites_details`
  ADD CONSTRAINT `fk_lastrites_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `marriage_details`
--
ALTER TABLE `marriage_details`
  ADD CONSTRAINT `fk_marriage_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `fk_payment_pledge` FOREIGN KEY (`pledge_id`) REFERENCES `pledges` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pledges`
--
ALTER TABLE `pledges`
  ADD CONSTRAINT `fk_pledge_member` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `print_logs`
--
ALTER TABLE `print_logs`
  ADD CONSTRAINT `fk_print_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `sacraments`
--
ALTER TABLE `sacraments`
  ADD CONSTRAINT `fk_sacrament_member` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sacrament_participants`
--
ALTER TABLE `sacrament_participants`
  ADD CONSTRAINT `fk_participant_sacrament` FOREIGN KEY (`sacrament_id`) REFERENCES `sacraments` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
