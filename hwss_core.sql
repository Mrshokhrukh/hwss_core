-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 02, 2024 at 06:00 AM
-- Server version: 8.0.28
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hwss_core`
--

-- --------------------------------------------------------

--
-- Table structure for table `access_agency`
--

CREATE TABLE `access_agency` (
  `id` int NOT NULL,
  `agency_code` varchar(100) NOT NULL,
  `agency_name` varchar(100) NOT NULL,
  `agency_parent` varchar(100) DEFAULT NULL,
  `present_dzongkhag` varchar(100) DEFAULT NULL,
  `present_gewog` varchar(100) DEFAULT NULL,
  `present_village` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `access_agency`
--

INSERT INTO `access_agency` (`id`, `agency_code`, `agency_name`, `agency_parent`, `present_dzongkhag`, `present_gewog`, `present_village`) VALUES
(1, '123123', 'Motithang higher Secondary School', NULL, NULL, NULL, NULL),
(2, '028.201.00434', 'Tsirangtoe Middle Secondary School', NULL, NULL, NULL, NULL),
(3, '14433', 'The Pema Secretariat', NULL, NULL, NULL, NULL),
(4, 'lmss-01', 'LMSS', NULL, NULL, NULL, NULL),
(5, '028.201.00300', 'Changangkha Middle Secondary School', NULL, NULL, NULL, NULL),
(17, '11001', 'Case Base Clients', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `access_customuser`
--

CREATE TABLE `access_customuser` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` int NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `identity_number` varchar(50) NOT NULL,
  `nationality` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `mob_number` varchar(15) DEFAULT NULL,
  `father_name` varchar(100) DEFAULT NULL,
  `mother_name` varchar(100) DEFAULT NULL,
  `perm_add_village` varchar(100) NOT NULL,
  `perm_add_gewog` varchar(100) NOT NULL,
  `perm_add_dzongkhag` varchar(100) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `ps_add_village` varchar(100) DEFAULT NULL,
  `ps_add_gewog` varchar(100) DEFAULT NULL,
  `ps_add_dzongkhag` varchar(100) DEFAULT NULL,
  `is_gyalsung` tinyint(1) NOT NULL,
  `academy_code` varchar(100) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `access_level` int NOT NULL,
  `active_agency_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `access_customuser`
--

INSERT INTO `access_customuser` (`password`, `last_login`, `is_superuser`, `id`, `username`, `is_staff`, `is_active`, `identity_number`, `nationality`, `first_name`, `middle_name`, `last_name`, `date_of_birth`, `gender`, `email`, `mob_number`, `father_name`, `mother_name`, `perm_add_village`, `perm_add_gewog`, `perm_add_dzongkhag`, `profile_picture`, `ps_add_village`, `ps_add_gewog`, `ps_add_dzongkhag`, `is_gyalsung`, `academy_code`, `date_joined`, `role`, `access_level`, `active_agency_id`) VALUES
('pbkdf2_sha256$720000$VAO1DBtA1dOrAE2QZNTpbk$JPaiEcwJnDitGg72YsZnl8+LJS3qktqZestZF9zAIgQ=', '2024-03-30 07:43:40.889034', 1, 1, 'uhollica666', 1, 1, '11203005289', 'Bhutanese', 'Ujwal', NULL, 'Pradhan', '1988-08-27', 'Male', 'ujwalpradhan@druksmart.com', '17795088', 'Niren Mani Pradhan', 'Reeta Pradhan', 'Samtse', 'Samtse', 'Samtse', '', NULL, NULL, NULL, 0, NULL, '2024-02-05 10:46:18.895000', 'mh_admin', 1, 3),
('pbkdf2_sha256$720000$ojGmxgwpOxLqgZPEJExSDO$23UBlpB7QWdyKjO7LOv9iexXr3kYV+6hTYR+s7koclk=', NULL, 0, 2, 'reijell123', 0, 1, '11203005686', 'Bhutanese', 'Reijell', 'Wangyal', 'Pradhan', '2022-10-24', 'Male', 'reijell@gmail.com', '17795088', 'Ujwal Pradhan', 'Rashme Gurung', 'samtse', 'samtse', 'samtse', 'profile_pictures/d.png', NULL, NULL, NULL, 0, NULL, '2024-02-05 16:23:32.000000', 'student', 1, 1),
('pbkdf2_sha256$720000$NkAnfq0CrCFOOTxne5fPpU$PPXqqZqpO3PGtbI8QIEYDlZTfGoYxByas5PKczBMBII=', NULL, 0, 3, 'counselor123', 0, 1, '21203000121', 'Bhutanese', 'Rashme', NULL, 'Gurung', '1984-05-14', 'Female', 'rashmegurung@druksmart.com', '17648107', 'Sahabir  Gurung', 'Sumitara  Gurung', 'Dugphey(Dubey)', 'Norgaygang/Bara', 'Samtse', '', NULL, NULL, NULL, 0, NULL, '2024-02-08 11:21:00.150000', 'school_counselor', 1, 2),
('pbkdf2_sha256$720000$UFvAzxakgR7MVN5LBaTJAH$mhipihmZZPlqX9IV93L39q7mdnxDb3jMOCpLXDMHg+s=', NULL, 0, 4, 'kinzang123', 0, 1, '11506005090', 'Bhutanese', 'Kinzang', NULL, 'Dema', '1994-03-03', 'Female', 'kinza@gmail.com', '17570776', 'Late Tandin  Wangdi', 'Tshewang  Choden', 'Lhamoi Lum /Gopini', 'Dunglagang', 'Tsirang', '', NULL, NULL, NULL, 0, NULL, '2024-02-09 06:57:18.361000', 'student', 1, 3),
('pbkdf2_sha256$720000$3jJivKIrSBsX0VWkzEccZe$JuwbTG8U/u86PgEehUxhYjdYdgidaI8q4guXmas02kw=', NULL, 1, 5, 'kinzang2024', 1, 1, '123', 'Bhutanese', 'Kizang', NULL, 'Dema', '1994-03-03', 'Female', 'kinzangdema@tech.gov.bt', '1234', NULL, NULL, 'Thimphu', 'Thimphu', 'Thimphu', '', NULL, NULL, NULL, 0, NULL, '2024-02-13 11:51:28.522000', 'student', 1, 1),
('pbkdf2_sha256$720000$4Zr9loWW9Mfdw0GXM7Uiq7$yGu8g9Ta6EehyWL+wRsvOBR4LYqlXWZe682+YlmCLaA=', NULL, 0, 6, 'sezylub', 0, 1, '12203000121', 'Bhutanese', 'Rashme', NULL, 'Gurung', '1984-05-14', 'Female', 'rashmegurung123@druksmart.com', '17648107', NULL, NULL, 'Dugphey(Dubey)', 'Norgaygang/Bara', 'Samtse', '', NULL, NULL, NULL, 0, NULL, '2024-02-17 06:37:23.854000', 'student', 1, NULL),
('pbkdf2_sha256$720000$fKfVoIFuFqNunSZa99A1oU$1I2UZ9qo4aGPiNGj8+aKUOwHY8u+Pa7XhVxiUTu/BrM=', NULL, 0, 7, 'roshan123', 0, 1, '11201003758', '', 'Roshan', NULL, 'Chhetri', '1996-08-31', 'Male', 'roshan@email.com', '14789526', NULL, NULL, 'Tphu', 'Thimphu', 'Thimphu', '', NULL, NULL, NULL, 0, NULL, '2024-02-17 06:43:42.110000', 'student', 1, NULL),
('pbkdf2_sha256$720000$WjQXZw6KaTMMBRSi5MLVge$GBv3ENDJjVv65rOTmsQISgOffdZvpDAFy5GPeXHusQA=', NULL, 0, 9, 'rabsel123', 0, 1, '11204005796', 'Bhutanese', 'Rabsel', 'Zhoenu', 'Dorji', '1988-12-15', 'Male', 'rabsel@gmail.com', '17853809', 'Tashi  Dorji', 'Sonam  Yangchen', 'Tshongduekha(Hatkhola)', 'Norbugang/Chengmari', 'Samtse', '', 'Tshongduekha(Hatkhola)', 'Norbugang/Chengmari', 'Samtse', 0, NULL, '2024-02-26 11:03:48.334000', 'school_counselor', 1, 1),
('pbkdf2_sha256$720000$vMjOurqkgLhhFcF2W3jDdU$Tsc+LN4v6OKVb55LDvtmTeqHQVh8dEmeAPW8Sb4C7dY=', NULL, 0, 10, 'rashmelilo', 0, 1, '11201005411', 'Bhutanese', 'Rashme', '', 'Gurung', '1984-05-14', 'Female', 'rashme.gurung666@gmail.com', '17648107', 'Sahabir  Gurung', 'Sumitara  Gurung', 'Dugphey(Dubey)', 'Norgaygang/Bara', 'Samtse', '', 'Dugphey(Dubey)', 'Norgaygang/Bara', 'Samtse', 0, NULL, '2024-02-28 04:36:34.489000', 'student', 1, NULL),
('pbkdf2_sha256$720000$8HF6QvCRGdUlVhp1zy0elg$SGxdrj790XUmrI7UBL2QJC/8CWnw2LdeUjtITelADHA=', NULL, 0, 11, 'caelen123', 0, 1, '11203005696', 'Bhutanese', 'Caelen', 'Nyima', 'Pradhan', '2015-12-03', 'Male', 'caelen@gmail.com', NULL, 'Ujwal  Pradhan', 'Rashme  Gurung', 'Saduzhima Kha(Chargharay B)', 'Sangacholing/Chargharey', 'Samtse', '', 'Saduzhima Kha(Chargharay B)', 'Sangacholing/Chargharey', 'Samtse', 0, NULL, '2024-02-28 05:34:03.801000', 'student', 1, NULL),
('!NRCaOkiXlgaIixehyHgFvesutbqkqmHRof1GDoaw', NULL, 0, 56, 'beatricemann20140224', 0, 1, '57', 'Bhutanese', 'Beatrice', '', 'Mann', '2014-02-24', 'Male', 'kika@mailinator.com', '74185296', NULL, NULL, 'Et voluptatum sint ', 'Et voluptatum sint ', 'Chhukha', '', 'Et voluptatum sint ', 'Et voluptatum sint ', 'Chhukha', 0, NULL, '2024-03-31 12:52:45.782185', 'student', 1, NULL),
('!g8J6rTS8vxsPS5q6XOmpi8S3vNQ1Slt9qugRs89x', NULL, 0, 57, 'sheilahancock20220105', 0, 1, '24', 'Bhutanese', 'Sheila', '', 'Hancock', '2022-01-05', 'Female', 'taginydoga@mailinator.com', '12313213', NULL, NULL, 'Laudantium animi a', 'Laudantium animi a', 'Bumthang', '', 'Laudantium animi a', 'Laudantium animi a', 'Bumthang', 0, NULL, '2024-03-31 13:00:56.495594', 'student', 1, NULL),
('!z0YY7cFoddZOOEhycozjSYXGr8dNPWojupMe630D', NULL, 0, 58, 'annenorris20091118', 0, 1, '21', 'Bhutanese', 'Anne', '', 'Norris', '2009-11-18', 'Other', 'wyhidowo@mailinator.com', '78978978', NULL, NULL, 'Ut enim ad non ut su', 'Ut enim ad non ut su', 'Trashigang', '', 'Ut enim ad non ut su', 'Ut enim ad non ut su', 'Trashigang', 0, NULL, '2024-04-01 03:31:00.462919', 'student', 1, NULL),
('!Bvgv4niXGnj9Vi1KjlIbqxKr6DQ4sSnl5NULuqPQ', NULL, 0, 59, 'mckenzieburris19740220', 0, 1, '52', 'Bhutanese', 'McKenzie', '', 'Burris', '1974-02-20', 'Female', 'zufodyv@mailinator.com', '75446575', NULL, NULL, 'Cupidatat voluptate ', 'Cupidatat voluptate ', 'Gasa', '', 'Cupidatat voluptate ', 'Cupidatat voluptate ', 'Gasa', 0, NULL, '2024-04-01 03:44:50.772198', 'student', 1, NULL),
('pbkdf2_sha256$720000$B0OVQ8FFFQQcrmph0ZGpxJ$GB8SeZoTo/C0vA8dM9RveBUvwY2sWlhy10eM/sJ2Bd8=', NULL, 0, 67, 'kinzang456', 0, 1, '11605008090', 'Bhutanese', 'Kinzang', '', 'Dema', '1994-03-03', 'Female', 'mynewemail@gmail.com', '17570776', 'Late Tandin  Wangdi', 'Tshewang  Choden', 'Lhamoi Lum /Gopini', 'Dunglagang', 'Tsirang', '', 'Lhamoi Lum /Gopini', 'Dunglagang', 'Tsirang', 0, NULL, '2024-04-02 03:51:00.711704', 'mh_admin', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `access_customuser_groups`
--

CREATE TABLE `access_customuser_groups` (
  `id` bigint NOT NULL,
  `customuser_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `access_customuser_user_permissions`
--

CREATE TABLE `access_customuser_user_permissions` (
  `id` bigint NOT NULL,
  `customuser_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `access_prerecordeduser`
--

CREATE TABLE `access_prerecordeduser` (
  `id` int NOT NULL,
  `username` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `identity_number` varchar(50) NOT NULL,
  `nationality` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mob_number` varchar(15) NOT NULL,
  `father_name` varchar(50) DEFAULT NULL,
  `mother_name` varchar(50) DEFAULT NULL,
  `perm_add_village` varchar(100) NOT NULL,
  `perm_add_gewog` varchar(100) NOT NULL,
  `perm_add_dzongkhag` varchar(100) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `is_gyalsung` tinyint(1) NOT NULL,
  `academy_code` varchar(100) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(100) DEFAULT NULL,
  `access_level` varchar(100) DEFAULT NULL,
  `is_registered` tinyint(1) NOT NULL,
  `agency_name` varchar(100) DEFAULT NULL,
  `agency_code` varchar(100) DEFAULT NULL,
  `user_code` varchar(100) DEFAULT NULL,
  `ps_add_village` varchar(100) DEFAULT NULL,
  `ps_add_gewog` varchar(100) DEFAULT NULL,
  `ps_add_dzongkhag` varchar(100) DEFAULT NULL,
  `parent_occupation` varchar(100) DEFAULT NULL,
  `guardian_name` varchar(100) DEFAULT NULL,
  `guardian_occupation` varchar(100) DEFAULT NULL,
  `parent_status` varchar(100) DEFAULT NULL,
  `current_living_with` varchar(100) DEFAULT NULL,
  `user_role_agency` varchar(100) DEFAULT NULL,
  `user_class` varchar(100) DEFAULT NULL,
  `user_sub_class` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `access_prerecordeduser`
--

INSERT INTO `access_prerecordeduser` (`id`, `username`, `is_staff`, `is_active`, `identity_number`, `nationality`, `first_name`, `middle_name`, `last_name`, `date_of_birth`, `gender`, `email`, `mob_number`, `father_name`, `mother_name`, `perm_add_village`, `perm_add_gewog`, `perm_add_dzongkhag`, `profile_picture`, `is_gyalsung`, `academy_code`, `date_joined`, `role`, `access_level`, `is_registered`, `agency_name`, `agency_code`, `user_code`, `ps_add_village`, `ps_add_gewog`, `ps_add_dzongkhag`, `parent_occupation`, `guardian_name`, `guardian_occupation`, `parent_status`, `current_living_with`, `user_role_agency`, `user_class`, `user_sub_class`) VALUES
(1, 'reijell123', 0, 1, '11203005686', 'Bhutanese', 'Reijell', 'Wangyal', 'Pradhan', '2022-10-24', 'Male', 'reijell@gmail.com', '17795088', 'Ujwal Pradhan', 'Rashme Gurung', 'samtse', 'samtse', 'samtse', '', 0, NULL, '2024-02-05 16:23:32.000000', 'student', NULL, 1, 'Motithang higher Secondary School', '123123', '0123', 'Thimphu', 'Thimphu', 'Thumphu', 'Civil Worker', NULL, NULL, 'Married', 'Parents', 'student', '10', 'B'),
(2, 'a', 0, 1, '11201003758', 'Bhutanese', 'Roshan', NULL, 'Chhetri', '1996-08-31', 'Male', 'roshan@email.com', '14789526', NULL, NULL, 'Tphu', 'Thimphu', 'Thimphu', '', 0, NULL, '2024-02-16 10:11:08.000000', 'student', NULL, 1, 'LMSS', 'lmss-01', '123', 'tphu', 'tphu', 'tphu', 'Teacher', NULL, NULL, 'Married', 'Parents', 'student', '12', 'B');

-- --------------------------------------------------------

--
-- Table structure for table `access_useragency`
--

CREATE TABLE `access_useragency` (
  `id` bigint NOT NULL,
  `user_code` varchar(100) NOT NULL,
  `parent_occupation` varchar(100) DEFAULT NULL,
  `guardian_name` varchar(100) DEFAULT NULL,
  `guardian_occupation` varchar(100) DEFAULT NULL,
  `parent_status` varchar(100) DEFAULT NULL,
  `current_living_with` varchar(100) DEFAULT NULL,
  `user_role_agency` varchar(100) NOT NULL,
  `user_class` varchar(100) DEFAULT NULL,
  `user_stream` varchar(100) DEFAULT NULL,
  `user_sub_class` varchar(100) DEFAULT NULL,
  `agency_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `access_useragency`
--

INSERT INTO `access_useragency` (`id`, `user_code`, `parent_occupation`, `guardian_name`, `guardian_occupation`, `parent_status`, `current_living_with`, `user_role_agency`, `user_class`, `user_stream`, `user_sub_class`, `agency_id`, `user_id`) VALUES
(12, '', NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, 17, 56),
(13, '', NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, 17, 57),
(14, '', NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, 17, 58),
(15, '', NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, 17, 59),
(16, '321321', NULL, NULL, NULL, NULL, NULL, 'student', NULL, NULL, NULL, 1, 5),
(17, '20170107941', '', '', '', '', '', 'mh_admin', '', NULL, '', 3, 67);

-- --------------------------------------------------------

--
-- Table structure for table `admin_interface_theme`
--

CREATE TABLE `admin_interface_theme` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `title_visible` tinyint(1) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `logo_visible` tinyint(1) NOT NULL,
  `css_header_background_color` varchar(10) NOT NULL,
  `title_color` varchar(10) NOT NULL,
  `css_header_text_color` varchar(10) NOT NULL,
  `css_header_link_color` varchar(10) NOT NULL,
  `css_header_link_hover_color` varchar(10) NOT NULL,
  `css_module_background_color` varchar(10) NOT NULL,
  `css_module_text_color` varchar(10) NOT NULL,
  `css_module_link_color` varchar(10) NOT NULL,
  `css_module_link_hover_color` varchar(10) NOT NULL,
  `css_module_rounded_corners` tinyint(1) NOT NULL,
  `css_generic_link_color` varchar(10) NOT NULL,
  `css_generic_link_hover_color` varchar(10) NOT NULL,
  `css_save_button_background_color` varchar(10) NOT NULL,
  `css_save_button_background_hover_color` varchar(10) NOT NULL,
  `css_save_button_text_color` varchar(10) NOT NULL,
  `css_delete_button_background_color` varchar(10) NOT NULL,
  `css_delete_button_background_hover_color` varchar(10) NOT NULL,
  `css_delete_button_text_color` varchar(10) NOT NULL,
  `list_filter_dropdown` tinyint(1) NOT NULL,
  `related_modal_active` tinyint(1) NOT NULL,
  `related_modal_background_color` varchar(10) NOT NULL,
  `related_modal_rounded_corners` tinyint(1) NOT NULL,
  `logo_color` varchar(10) NOT NULL,
  `recent_actions_visible` tinyint(1) NOT NULL,
  `favicon` varchar(100) NOT NULL,
  `related_modal_background_opacity` varchar(5) NOT NULL,
  `env_name` varchar(50) NOT NULL,
  `env_visible_in_header` tinyint(1) NOT NULL,
  `env_color` varchar(10) NOT NULL,
  `env_visible_in_favicon` tinyint(1) NOT NULL,
  `related_modal_close_button_visible` tinyint(1) NOT NULL,
  `language_chooser_active` tinyint(1) NOT NULL,
  `language_chooser_display` varchar(10) NOT NULL,
  `list_filter_sticky` tinyint(1) NOT NULL,
  `form_pagination_sticky` tinyint(1) NOT NULL,
  `form_submit_sticky` tinyint(1) NOT NULL,
  `css_module_background_selected_color` varchar(10) NOT NULL,
  `css_module_link_selected_color` varchar(10) NOT NULL,
  `logo_max_height` smallint UNSIGNED NOT NULL,
  `logo_max_width` smallint UNSIGNED NOT NULL,
  `foldable_apps` tinyint(1) NOT NULL,
  `language_chooser_control` varchar(20) NOT NULL,
  `list_filter_highlight` tinyint(1) NOT NULL,
  `list_filter_removal_links` tinyint(1) NOT NULL,
  `show_fieldsets_as_tabs` tinyint(1) NOT NULL,
  `show_inlines_as_tabs` tinyint(1) NOT NULL,
  `css_generic_link_active_color` varchar(10) NOT NULL,
  `collapsible_stacked_inlines` tinyint(1) NOT NULL,
  `collapsible_stacked_inlines_collapsed` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines_collapsed` tinyint(1) NOT NULL
) ;

--
-- Dumping data for table `admin_interface_theme`
--

INSERT INTO `admin_interface_theme` (`id`, `name`, `active`, `title`, `title_visible`, `logo`, `logo_visible`, `css_header_background_color`, `title_color`, `css_header_text_color`, `css_header_link_color`, `css_header_link_hover_color`, `css_module_background_color`, `css_module_text_color`, `css_module_link_color`, `css_module_link_hover_color`, `css_module_rounded_corners`, `css_generic_link_color`, `css_generic_link_hover_color`, `css_save_button_background_color`, `css_save_button_background_hover_color`, `css_save_button_text_color`, `css_delete_button_background_color`, `css_delete_button_background_hover_color`, `css_delete_button_text_color`, `list_filter_dropdown`, `related_modal_active`, `related_modal_background_color`, `related_modal_rounded_corners`, `logo_color`, `recent_actions_visible`, `favicon`, `related_modal_background_opacity`, `env_name`, `env_visible_in_header`, `env_color`, `env_visible_in_favicon`, `related_modal_close_button_visible`, `language_chooser_active`, `language_chooser_display`, `list_filter_sticky`, `form_pagination_sticky`, `form_submit_sticky`, `css_module_background_selected_color`, `css_module_link_selected_color`, `logo_max_height`, `logo_max_width`, `foldable_apps`, `language_chooser_control`, `list_filter_highlight`, `list_filter_removal_links`, `show_fieldsets_as_tabs`, `show_inlines_as_tabs`, `css_generic_link_active_color`, `collapsible_stacked_inlines`, `collapsible_stacked_inlines_collapsed`, `collapsible_tabular_inlines`, `collapsible_tabular_inlines_collapsed`) VALUES
(1, 'HWSS Theme', 1, 'HWSS Admin', 1, 'admin-interface/logo/Logo_4eJ5IEu.png', 1, '#FFFFFF', '#2C6975', '#2C6975', '#8AC2AE', '#8AC2AE', '#2C6975', '#FFFFFF', '#8AC2AE', '#FFFFFF', 1, '#2C6975', '#8AC2AE', '#5CB85C', '#449D44', '#FFFFFF', '#D9534F', '#C9302C', '#FFFFFF', 1, 1, '#2C6975', 1, '#2C6975', 1, 'admin-interface/favicon/logoDashbopard_RrnBVwp.png', '0.2', 'Dev', 1, '#2C6975', 1, 1, 0, 'code', 1, 0, 0, '#CDE0C9', '#FFFFFF', 100, 150, 1, 'default-select', 1, 0, 0, 1, '#29B864', 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `authtoken_token`
--

INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES
('0bafab86a9704d762c806ce3aa6da32fdce2370f', '2024-03-29 09:13:46.867560', 9),
('18521625209b4b0a333add46c81b16741337b131', '2024-04-01 10:41:32.322382', 1),
('4e7a7bee6ac6b9a844a0df9c9c096d7207334cfc', '2024-03-29 08:32:31.757594', 2),
('7f08e42e7d3bd612be96160979b050f7b9e699b4', '2024-03-29 08:43:55.730109', 4),
('9824d9156a0bcf7fa1d168bc63e2fa58a8561806', '2024-04-01 07:09:56.342480', 6),
('cacff84a601f76f0b33120d4446f64314fcab6c1', '2024-04-01 07:25:47.994860', 10);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'admin'),
(3, 'counselor'),
(1, 'student');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add Theme', 1, 'add_theme'),
(2, 'Can change Theme', 1, 'change_theme'),
(3, 'Can delete Theme', 1, 'delete_theme'),
(4, 'Can view Theme', 1, 'view_theme'),
(5, 'Can add log entry', 2, 'add_logentry'),
(6, 'Can change log entry', 2, 'change_logentry'),
(7, 'Can delete log entry', 2, 'delete_logentry'),
(8, 'Can view log entry', 2, 'view_logentry'),
(9, 'Can add permission', 3, 'add_permission'),
(10, 'Can change permission', 3, 'change_permission'),
(11, 'Can delete permission', 3, 'delete_permission'),
(12, 'Can view permission', 3, 'view_permission'),
(13, 'Can add group', 4, 'add_group'),
(14, 'Can change group', 4, 'change_group'),
(15, 'Can delete group', 4, 'delete_group'),
(16, 'Can view group', 4, 'view_group'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add agency', 7, 'add_agency'),
(26, 'Can change agency', 7, 'change_agency'),
(27, 'Can delete agency', 7, 'delete_agency'),
(28, 'Can view agency', 7, 'view_agency'),
(29, 'Can add Pre-recorded user', 8, 'add_prerecordeduser'),
(30, 'Can change Pre-recorded user', 8, 'change_prerecordeduser'),
(31, 'Can delete Pre-recorded user', 8, 'delete_prerecordeduser'),
(32, 'Can view Pre-recorded user', 8, 'view_prerecordeduser'),
(33, 'Can add user', 9, 'add_customuser'),
(34, 'Can change user', 9, 'change_customuser'),
(35, 'Can delete user', 9, 'delete_customuser'),
(36, 'Can view user', 9, 'view_customuser'),
(37, 'Can add user agency', 10, 'add_useragency'),
(38, 'Can change user agency', 10, 'change_useragency'),
(39, 'Can delete user agency', 10, 'delete_useragency'),
(40, 'Can view user agency', 10, 'view_useragency'),
(41, 'Can add measurement substance', 11, 'add_measurementsubstance'),
(42, 'Can change measurement substance', 11, 'change_measurementsubstance'),
(43, 'Can delete measurement substance', 11, 'delete_measurementsubstance'),
(44, 'Can view measurement substance', 11, 'view_measurementsubstance'),
(45, 'Can add test type', 12, 'add_testtype'),
(46, 'Can change test type', 12, 'change_testtype'),
(47, 'Can delete test type', 12, 'delete_testtype'),
(48, 'Can view test type', 12, 'view_testtype'),
(49, 'Can add question set', 13, 'add_questionset'),
(50, 'Can change question set', 13, 'change_questionset'),
(51, 'Can delete question set', 13, 'delete_questionset'),
(52, 'Can view question set', 13, 'view_questionset'),
(53, 'Can add user submission', 14, 'add_usersubmission'),
(54, 'Can change user submission', 14, 'change_usersubmission'),
(55, 'Can delete user submission', 14, 'delete_usersubmission'),
(56, 'Can view user submission', 14, 'view_usersubmission'),
(57, 'Can add submission', 15, 'add_submission'),
(58, 'Can change submission', 15, 'change_submission'),
(59, 'Can delete submission', 15, 'delete_submission'),
(60, 'Can view submission', 15, 'view_submission'),
(61, 'Can add measurement assist', 16, 'add_measurementassist'),
(62, 'Can change measurement assist', 16, 'change_measurementassist'),
(63, 'Can delete measurement assist', 16, 'delete_measurementassist'),
(64, 'Can view measurement assist', 16, 'view_measurementassist'),
(65, 'Can add measurement', 17, 'add_measurement'),
(66, 'Can change measurement', 17, 'change_measurement'),
(67, 'Can delete measurement', 17, 'delete_measurement'),
(68, 'Can view measurement', 17, 'view_measurement'),
(69, 'Can add referral', 18, 'add_referral'),
(70, 'Can change referral', 18, 'change_referral'),
(71, 'Can delete referral', 18, 'delete_referral'),
(72, 'Can view referral', 18, 'view_referral'),
(73, 'Can add rescreening', 19, 'add_rescreening'),
(74, 'Can change rescreening', 19, 'change_rescreening'),
(75, 'Can delete rescreening', 19, 'delete_rescreening'),
(76, 'Can view rescreening', 19, 'view_rescreening'),
(77, 'Can add service and treatment', 20, 'add_serviceandtreatment'),
(78, 'Can change service and treatment', 20, 'change_serviceandtreatment'),
(79, 'Can delete service and treatment', 20, 'delete_serviceandtreatment'),
(80, 'Can view service and treatment', 20, 'view_serviceandtreatment'),
(81, 'Can add app config', 21, 'add_appconfig'),
(82, 'Can change app config', 21, 'change_appconfig'),
(83, 'Can delete app config', 21, 'delete_appconfig'),
(84, 'Can view app config', 21, 'view_appconfig'),
(85, 'Can add menu item', 22, 'add_menuitem'),
(86, 'Can change menu item', 22, 'change_menuitem'),
(87, 'Can delete menu item', 22, 'delete_menuitem'),
(88, 'Can view menu item', 22, 'view_menuitem'),
(89, 'Can add Token', 23, 'add_token'),
(90, 'Can change Token', 23, 'change_token'),
(91, 'Can delete Token', 23, 'delete_token'),
(92, 'Can view Token', 23, 'view_token'),
(93, 'Can add token', 24, 'add_tokenproxy'),
(94, 'Can change token', 24, 'change_tokenproxy'),
(95, 'Can delete token', 24, 'delete_tokenproxy'),
(96, 'Can view token', 24, 'view_tokenproxy'),
(97, 'Can add reporting', 25, 'add_reporting'),
(98, 'Can change reporting', 25, 'change_reporting'),
(99, 'Can delete reporting', 25, 'delete_reporting'),
(100, 'Can view reporting', 25, 'view_reporting'),
(101, 'Can add event screening', 26, 'add_eventscreening'),
(102, 'Can change event screening', 26, 'change_eventscreening'),
(103, 'Can delete event screening', 26, 'delete_eventscreening'),
(104, 'Can view event screening', 26, 'view_eventscreening'),
(105, 'Can add case screening', 27, 'add_casescreening'),
(106, 'Can change case screening', 27, 'change_casescreening'),
(107, 'Can delete case screening', 27, 'delete_casescreening'),
(108, 'Can view case screening', 27, 'view_casescreening'),
(109, 'Can add screened user', 28, 'add_screeneduser'),
(110, 'Can change screened user', 28, 'change_screeneduser'),
(111, 'Can delete screened user', 28, 'delete_screeneduser'),
(112, 'Can view screened user', 28, 'view_screeneduser'),
(113, 'Can add video', 29, 'add_video'),
(114, 'Can change video', 29, 'change_video'),
(115, 'Can delete video', 29, 'delete_video'),
(116, 'Can view video', 29, 'view_video'),
(117, 'Can add lifetime user', 30, 'add_lifetimeuser'),
(118, 'Can change lifetime user', 30, 'change_lifetimeuser'),
(119, 'Can delete lifetime user', 30, 'delete_lifetimeuser'),
(120, 'Can view lifetime user', 30, 'view_lifetimeuser'),
(121, 'Can add active user', 31, 'add_activeuser'),
(122, 'Can change active user', 31, 'change_activeuser'),
(123, 'Can delete active user', 31, 'delete_activeuser'),
(124, 'Can view active user', 31, 'view_activeuser'),
(125, 'Can add notification', 32, 'add_notification'),
(126, 'Can change notification', 32, 'change_notification'),
(127, 'Can delete notification', 32, 'delete_notification'),
(128, 'Can view notification', 32, 'view_notification');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-03-29 08:29:48.904025', '1', 'HWSS Theme', 2, '[]', 1, 1),
(2, '2024-03-29 09:09:20.781953', '4', 'kinzang123', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 9, 1),
(3, '2024-03-29 09:12:08.019885', '4', 'kinzang123', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 9, 1),
(4, '2024-03-30 17:16:04.918727', '6', 'Reporting for kinzang123', 3, '', 25, 1),
(5, '2024-03-30 17:16:04.921725', '5', 'Reporting for reijell123', 3, '', 25, 1),
(6, '2024-03-30 17:16:04.923051', '4', 'Reporting for kinzang123', 3, '', 25, 1),
(7, '2024-03-30 17:16:04.925092', '3', 'Reporting for reijell123', 3, '', 25, 1),
(8, '2024-03-30 17:16:04.927808', '2', 'Reporting for reijell123', 3, '', 25, 1),
(9, '2024-03-30 17:16:04.927808', '1', 'Reporting for uhollica666', 3, '', 25, 1),
(10, '2024-03-30 17:20:19.875017', '7', 'Reporting for reijell123', 3, '', 25, 1),
(11, '2024-03-30 17:44:58.506008', '9', 'Reporting for reijell123', 3, '', 25, 1),
(12, '2024-03-30 17:44:58.509007', '8', 'Reporting for kinzang123', 3, '', 25, 1),
(13, '2024-03-31 07:22:57.527814', '11', 'Reporting for kinzang123', 3, '', 25, 1),
(14, '2024-03-31 07:22:57.527814', '10', 'Reporting for reijell123', 3, '', 25, 1),
(15, '2024-03-31 07:24:34.702370', '14', 'Reporting for kinzang123', 3, '', 25, 1),
(16, '2024-03-31 07:24:34.704875', '13', 'Reporting for kinzang123', 3, '', 25, 1),
(17, '2024-03-31 07:24:34.706882', '12', 'Reporting for reijell123', 3, '', 25, 1),
(18, '2024-03-31 07:26:32.831304', '16', 'Reporting for kinzang123', 3, '', 25, 1),
(19, '2024-03-31 07:26:32.831304', '15', 'Reporting for reijell123', 3, '', 25, 1),
(20, '2024-03-31 07:31:15.390350', '19', 'Reporting for kinzang123', 3, '', 25, 1),
(21, '2024-03-31 07:31:15.392348', '18', 'Reporting for kinzang123', 3, '', 25, 1),
(22, '2024-03-31 07:31:15.393348', '17', 'Reporting for reijell123', 3, '', 25, 1),
(23, '2024-03-31 08:01:53.572157', '23', 'Reporting for kinzang123', 3, '', 25, 1),
(24, '2024-03-31 08:01:53.572157', '22', 'Reporting for kinzang123', 3, '', 25, 1),
(25, '2024-03-31 08:01:53.572157', '21', 'Reporting for reijell123', 3, '', 25, 1),
(26, '2024-03-31 08:01:53.589040', '20', 'Reporting for reijell123', 3, '', 25, 1),
(27, '2024-03-31 08:08:01.484229', '27', 'Reporting for kinzang123', 3, '', 25, 1),
(28, '2024-03-31 08:08:01.486193', '26', 'Reporting for kinzang123', 3, '', 25, 1),
(29, '2024-03-31 08:08:01.488197', '25', 'Reporting for reijell123', 3, '', 25, 1),
(30, '2024-03-31 08:08:01.489197', '24', 'Reporting for reijell123', 3, '', 25, 1),
(31, '2024-03-31 08:15:35.169305', '30', 'Reporting for kinzang123', 3, '', 25, 1),
(32, '2024-03-31 08:15:35.171307', '29', 'Reporting for reijell123', 3, '', 25, 1),
(33, '2024-03-31 08:15:35.173303', '28', 'Reporting for reijell123', 3, '', 25, 1),
(34, '2024-03-31 08:21:03.805062', '32', 'Reporting for kinzang123', 3, '', 25, 1),
(35, '2024-03-31 08:21:03.809063', '31', 'Reporting for reijell123', 3, '', 25, 1),
(36, '2024-03-31 08:23:13.831957', '33', 'Reporting for reijell123', 3, '', 25, 1),
(37, '2024-03-31 08:26:35.428954', '35', 'Reporting for reijell123', 3, '', 25, 1),
(38, '2024-03-31 08:36:53.160512', '36', 'Reporting for reijell123', 3, '', 25, 1),
(39, '2024-03-31 08:44:37.017671', '37', 'Reporting for reijell123', 3, '', 25, 1),
(40, '2024-03-31 08:47:55.306793', '38', 'Reporting for reijell123', 3, '', 25, 1),
(41, '2024-03-31 15:49:20.694280', '91', 'EventScreening object (91)', 3, '', 26, 1),
(42, '2024-03-31 15:49:20.698283', '90', 'EventScreening object (90)', 3, '', 26, 1),
(43, '2024-03-31 15:49:20.700300', '89', 'EventScreening object (89)', 3, '', 26, 1),
(44, '2024-03-31 15:49:20.702301', '88', 'EventScreening object (88)', 3, '', 26, 1),
(45, '2024-03-31 15:49:20.704868', '87', 'EventScreening object (87)', 3, '', 26, 1),
(46, '2024-03-31 15:49:20.706893', '86', 'EventScreening object (86)', 3, '', 26, 1),
(47, '2024-03-31 15:49:20.709907', '85', 'EventScreening object (85)', 3, '', 26, 1),
(48, '2024-03-31 15:49:20.711862', '84', 'EventScreening object (84)', 3, '', 26, 1),
(49, '2024-03-31 15:49:20.712863', '83', 'EventScreening object (83)', 3, '', 26, 1),
(50, '2024-03-31 15:49:20.713863', '82', 'EventScreening object (82)', 3, '', 26, 1),
(51, '2024-03-31 15:49:20.715863', '81', 'EventScreening object (81)', 3, '', 26, 1),
(52, '2024-03-31 15:49:20.716863', '80', 'EventScreening object (80)', 3, '', 26, 1),
(53, '2024-03-31 15:49:20.718866', '79', 'EventScreening object (79)', 3, '', 26, 1),
(54, '2024-03-31 15:49:20.720864', '78', 'EventScreening object (78)', 3, '', 26, 1),
(55, '2024-03-31 15:49:20.722868', '77', 'EventScreening object (77)', 3, '', 26, 1),
(56, '2024-03-31 15:49:20.723863', '76', 'EventScreening object (76)', 3, '', 26, 1),
(57, '2024-03-31 15:49:20.725864', '75', 'EventScreening object (75)', 3, '', 26, 1),
(58, '2024-03-31 15:49:20.726863', '74', 'EventScreening object (74)', 3, '', 26, 1),
(59, '2024-03-31 15:49:20.728866', '73', 'EventScreening object (73)', 3, '', 26, 1),
(60, '2024-03-31 15:49:20.729864', '72', 'EventScreening object (72)', 3, '', 26, 1),
(61, '2024-03-31 15:49:20.730863', '71', 'EventScreening object (71)', 3, '', 26, 1),
(62, '2024-03-31 15:49:20.732865', '70', 'EventScreening object (70)', 3, '', 26, 1),
(63, '2024-03-31 15:49:20.733864', '69', 'EventScreening object (69)', 3, '', 26, 1),
(64, '2024-03-31 15:49:20.735865', '68', 'EventScreening object (68)', 3, '', 26, 1),
(65, '2024-03-31 15:49:20.737867', '67', 'EventScreening object (67)', 3, '', 26, 1),
(66, '2024-03-31 15:49:20.739866', '66', 'EventScreening object (66)', 3, '', 26, 1),
(67, '2024-03-31 15:49:20.740866', '65', 'EventScreening object (65)', 3, '', 26, 1),
(68, '2024-03-31 15:49:20.742865', '64', 'EventScreening object (64)', 3, '', 26, 1),
(69, '2024-03-31 15:49:20.743866', '63', 'EventScreening object (63)', 3, '', 26, 1),
(70, '2024-03-31 15:49:20.745865', '62', 'EventScreening object (62)', 3, '', 26, 1),
(71, '2024-03-31 15:49:20.746865', '61', 'EventScreening object (61)', 3, '', 26, 1),
(72, '2024-03-31 15:49:20.748866', '60', 'EventScreening object (60)', 3, '', 26, 1),
(73, '2024-03-31 15:49:20.750865', '59', 'EventScreening object (59)', 3, '', 26, 1),
(74, '2024-03-31 15:49:20.752865', '58', 'EventScreening object (58)', 3, '', 26, 1),
(75, '2024-03-31 15:49:20.754864', '57', 'EventScreening object (57)', 3, '', 26, 1),
(76, '2024-03-31 15:49:20.758136', '56', 'EventScreening object (56)', 3, '', 26, 1),
(77, '2024-03-31 15:49:20.760139', '55', 'EventScreening object (55)', 3, '', 26, 1),
(78, '2024-03-31 15:49:20.762139', '54', 'EventScreening object (54)', 3, '', 26, 1),
(79, '2024-03-31 15:49:20.763146', '53', 'EventScreening object (53)', 3, '', 26, 1),
(80, '2024-03-31 15:49:20.765137', '52', 'EventScreening object (52)', 3, '', 26, 1),
(81, '2024-03-31 15:49:20.766137', '51', 'EventScreening object (51)', 3, '', 26, 1),
(82, '2024-03-31 15:49:20.768150', '50', 'EventScreening object (50)', 3, '', 26, 1),
(83, '2024-03-31 15:49:20.772138', '49', 'EventScreening object (49)', 3, '', 26, 1),
(84, '2024-03-31 15:49:20.773139', '48', 'EventScreening object (48)', 3, '', 26, 1),
(85, '2024-03-31 15:49:20.775136', '47', 'EventScreening object (47)', 3, '', 26, 1),
(86, '2024-03-31 15:49:20.777150', '46', 'EventScreening object (46)', 3, '', 26, 1),
(87, '2024-03-31 15:49:20.778137', '45', 'EventScreening object (45)', 3, '', 26, 1),
(88, '2024-03-31 15:49:20.780138', '44', 'EventScreening object (44)', 3, '', 26, 1),
(89, '2024-03-31 15:49:20.781136', '43', 'EventScreening object (43)', 3, '', 26, 1),
(90, '2024-03-31 15:49:20.783139', '42', 'EventScreening object (42)', 3, '', 26, 1),
(91, '2024-03-31 15:49:20.786299', '41', 'EventScreening object (41)', 3, '', 26, 1),
(92, '2024-03-31 15:49:20.788317', '40', 'EventScreening object (40)', 3, '', 26, 1),
(93, '2024-03-31 15:49:20.790317', '39', 'EventScreening object (39)', 3, '', 26, 1),
(94, '2024-03-31 15:49:20.791317', '38', 'EventScreening object (38)', 3, '', 26, 1),
(95, '2024-03-31 15:49:20.792317', '37', 'EventScreening object (37)', 3, '', 26, 1),
(96, '2024-03-31 15:49:20.794317', '36', 'EventScreening object (36)', 3, '', 26, 1),
(97, '2024-03-31 15:49:20.795317', '35', 'EventScreening object (35)', 3, '', 26, 1),
(98, '2024-03-31 15:49:20.797317', '34', 'EventScreening object (34)', 3, '', 26, 1),
(99, '2024-03-31 15:49:20.799316', '33', 'EventScreening object (33)', 3, '', 26, 1),
(100, '2024-03-31 15:49:20.800314', '32', 'EventScreening object (32)', 3, '', 26, 1),
(101, '2024-03-31 15:49:20.802823', '31', 'EventScreening object (31)', 3, '', 26, 1),
(102, '2024-03-31 15:49:20.804830', '30', 'EventScreening object (30)', 3, '', 26, 1),
(103, '2024-03-31 15:49:20.805829', '29', 'EventScreening object (29)', 3, '', 26, 1),
(104, '2024-03-31 15:49:20.806829', '28', 'EventScreening object (28)', 3, '', 26, 1),
(105, '2024-03-31 15:49:20.808830', '27', 'EventScreening object (27)', 3, '', 26, 1),
(106, '2024-03-31 15:49:20.809829', '26', 'EventScreening object (26)', 3, '', 26, 1),
(107, '2024-03-31 15:49:20.811829', '25', 'EventScreening object (25)', 3, '', 26, 1),
(108, '2024-03-31 15:49:20.813462', '24', 'EventScreening object (24)', 3, '', 26, 1),
(109, '2024-03-31 15:49:20.814989', '23', 'EventScreening object (23)', 3, '', 26, 1),
(110, '2024-03-31 15:49:20.816021', '22', 'EventScreening object (22)', 3, '', 26, 1),
(111, '2024-03-31 15:49:20.817989', '21', 'EventScreening object (21)', 3, '', 26, 1),
(112, '2024-03-31 15:49:20.819990', '20', 'EventScreening object (20)', 3, '', 26, 1),
(113, '2024-03-31 15:49:20.820988', '19', 'EventScreening object (19)', 3, '', 26, 1),
(114, '2024-03-31 15:49:20.822988', '18', 'EventScreening object (18)', 3, '', 26, 1),
(115, '2024-03-31 15:49:20.824988', '17', 'EventScreening object (17)', 3, '', 26, 1),
(116, '2024-03-31 15:49:20.825988', '16', 'EventScreening object (16)', 3, '', 26, 1),
(117, '2024-03-31 15:49:20.827988', '15', 'EventScreening object (15)', 3, '', 26, 1),
(118, '2024-03-31 15:49:20.829988', '14', 'EventScreening object (14)', 3, '', 26, 1),
(119, '2024-03-31 15:49:20.830988', '13', 'EventScreening object (13)', 3, '', 26, 1),
(120, '2024-03-31 15:49:20.832989', '12', 'EventScreening object (12)', 3, '', 26, 1),
(121, '2024-03-31 15:49:20.833989', '11', 'EventScreening object (11)', 3, '', 26, 1),
(122, '2024-03-31 15:49:20.836993', '10', 'EventScreening object (10)', 3, '', 26, 1),
(123, '2024-03-31 15:49:20.838988', '9', 'EventScreening object (9)', 3, '', 26, 1),
(124, '2024-03-31 15:49:20.840990', '8', 'EventScreening object (8)', 3, '', 26, 1),
(125, '2024-03-31 15:49:20.841988', '7', 'EventScreening object (7)', 3, '', 26, 1),
(126, '2024-03-31 15:49:20.843992', '6', 'EventScreening object (6)', 3, '', 26, 1),
(127, '2024-03-31 15:49:20.845990', '5', 'EventScreening object (5)', 3, '', 26, 1),
(128, '2024-03-31 15:49:20.847989', '4', 'EventScreening object (4)', 3, '', 26, 1),
(129, '2024-03-31 15:49:20.849988', '3', 'EventScreening object (3)', 3, '', 26, 1),
(130, '2024-03-31 15:49:20.851991', '2', 'EventScreening object (2)', 3, '', 26, 1),
(131, '2024-03-31 15:49:20.853989', '1', 'EventScreening object (1)', 3, '', 26, 1),
(132, '2024-03-31 17:06:41.883972', '92', 'EventScreening object (92)', 2, '[{\"changed\": {\"fields\": [\"Location\", \"Approval status\"]}}, {\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (1)\"}}]', 26, 1),
(133, '2024-03-31 19:12:09.471828', '92', 'EventScreening object (92)', 2, '[{\"changed\": {\"fields\": [\"Approval status\"]}}, {\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (2)\"}}]', 26, 1),
(134, '2024-03-31 19:13:19.693944', '92', 'EventScreening object (92)', 2, '[{\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (3)\"}}]', 26, 1),
(135, '2024-03-31 19:13:38.316470', '92', 'EventScreening object (92)', 2, '[{\"changed\": {\"fields\": [\"Approval status\"]}}, {\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (4)\"}}]', 26, 1),
(136, '2024-04-01 02:53:44.246135', '92', 'EventScreening object (92)', 2, '[{\"changed\": {\"fields\": [\"Approval status\"]}}, {\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (5)\"}}]', 26, 1),
(137, '2024-04-01 02:54:03.945162', '92', 'EventScreening object (92)', 2, '[{\"changed\": {\"fields\": [\"Approval status\"]}}, {\"added\": {\"name\": \"screened user\", \"object\": \"ScreenedUser object (6)\"}}]', 26, 1),
(138, '2024-04-01 04:50:56.569489', '1', 'My Video', 1, '[{\"added\": {}}]', 29, 1),
(139, '2024-04-01 07:10:18.843247', '6', 'sezylub', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 9, 1),
(140, '2024-04-01 07:23:39.009451', '5', 'kinzang2024', 2, '[{\"changed\": {\"fields\": [\"Role\", \"Nationality\"]}}]', 9, 1),
(141, '2024-04-01 07:24:16.373294', '5', 'kinzang2024', 2, '[{\"added\": {\"name\": \"user agency\", \"object\": \"kinzangdema@tech.gov.bt - Motithang higher Secondary School\"}}]', 9, 1),
(142, '2024-04-01 07:24:28.238881', '5', 'kinzang2024', 2, '[{\"changed\": {\"fields\": [\"Active agency\"]}}]', 9, 1),
(143, '2024-04-01 10:42:05.047819', '1', 'uhollica666', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 9, 1),
(144, '2024-04-01 10:53:52.310198', '3', 'Yes Menu', 3, '', 22, 1),
(145, '2024-04-01 10:54:08.321333', '2', 'Settings', 2, '[{\"changed\": {\"fields\": [\"Route\"]}}]', 22, 1),
(146, '2024-04-01 11:08:49.873429', '10', 'Approval', 1, '[{\"added\": {}}]', 22, 1),
(147, '2024-04-01 11:10:11.889474', '11', 'Reports', 1, '[{\"added\": {}}]', 22, 1),
(148, '2024-04-01 11:10:19.981532', '10', 'Approval', 2, '[{\"changed\": {\"fields\": [\"Route\"]}}]', 22, 1),
(149, '2024-04-01 11:11:29.062117', '12', 'Help', 1, '[{\"added\": {}}]', 22, 1),
(150, '2024-04-01 11:12:18.615218', '13', 'Settings', 1, '[{\"added\": {}}]', 22, 1),
(151, '2024-04-01 11:13:37.676160', '2', 'Settings', 3, '', 22, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'access', 'agency'),
(9, 'access', 'customuser'),
(8, 'access', 'prerecordeduser'),
(10, 'access', 'useragency'),
(2, 'admin', 'logentry'),
(1, 'admin_interface', 'theme'),
(4, 'auth', 'group'),
(3, 'auth', 'permission'),
(23, 'authtoken', 'token'),
(24, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(31, 'measurement', 'activeuser'),
(30, 'measurement', 'lifetimeuser'),
(17, 'measurement', 'measurement'),
(16, 'measurement', 'measurementassist'),
(11, 'measurement', 'measurementsubstance'),
(13, 'measurement', 'questionset'),
(15, 'measurement', 'submission'),
(12, 'measurement', 'testtype'),
(14, 'measurement', 'usersubmission'),
(18, 'monitoring', 'referral'),
(19, 'monitoring', 'rescreening'),
(20, 'monitoring', 'serviceandtreatment'),
(25, 'reporting', 'reporting'),
(27, 'screening', 'casescreening'),
(26, 'screening', 'eventscreening'),
(28, 'screening', 'screeneduser'),
(6, 'sessions', 'session'),
(21, 'settings_module', 'appconfig'),
(22, 'settings_module', 'menuitem'),
(32, 'settings_module', 'notification'),
(29, 'settings_module', 'video');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-03-29 08:10:37.588469'),
(2, 'contenttypes', '0002_remove_content_type_name', '2024-03-29 08:10:37.783847'),
(3, 'auth', '0001_initial', '2024-03-29 08:10:38.286839'),
(4, 'auth', '0002_alter_permission_name_max_length', '2024-03-29 08:10:38.390501'),
(5, 'auth', '0003_alter_user_email_max_length', '2024-03-29 08:10:38.399856'),
(6, 'auth', '0004_alter_user_username_opts', '2024-03-29 08:10:38.408844'),
(7, 'auth', '0005_alter_user_last_login_null', '2024-03-29 08:10:38.417259'),
(8, 'auth', '0006_require_contenttypes_0002', '2024-03-29 08:10:38.420642'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2024-03-29 08:10:38.427141'),
(10, 'auth', '0008_alter_user_username_max_length', '2024-03-29 08:10:38.435660'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2024-03-29 08:10:38.441848'),
(12, 'auth', '0010_alter_group_name_max_length', '2024-03-29 08:10:38.465187'),
(13, 'auth', '0011_update_proxy_permissions', '2024-03-29 08:10:38.476182'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2024-03-29 08:10:38.485677'),
(15, 'access', '0001_initial', '2024-03-29 08:10:39.550428'),
(16, 'admin', '0001_initial', '2024-03-29 08:10:39.779004'),
(17, 'admin', '0002_logentry_remove_auto_add', '2024-03-29 08:10:39.793043'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-03-29 08:10:39.804042'),
(19, 'admin_interface', '0001_initial', '2024-03-29 08:10:39.843846'),
(20, 'admin_interface', '0002_add_related_modal', '2024-03-29 08:10:39.995811'),
(21, 'admin_interface', '0003_add_logo_color', '2024-03-29 08:10:40.043772'),
(22, 'admin_interface', '0004_rename_title_color', '2024-03-29 08:10:40.068416'),
(23, 'admin_interface', '0005_add_recent_actions_visible', '2024-03-29 08:10:40.109711'),
(24, 'admin_interface', '0006_bytes_to_str', '2024-03-29 08:10:40.180791'),
(25, 'admin_interface', '0007_add_favicon', '2024-03-29 08:10:40.221139'),
(26, 'admin_interface', '0008_change_related_modal_background_opacity_type', '2024-03-29 08:10:40.335881'),
(27, 'admin_interface', '0009_add_enviroment', '2024-03-29 08:10:40.421883'),
(28, 'admin_interface', '0010_add_localization', '2024-03-29 08:10:40.444540'),
(29, 'admin_interface', '0011_add_environment_options', '2024-03-29 08:10:40.591806'),
(30, 'admin_interface', '0012_update_verbose_names', '2024-03-29 08:10:40.600840'),
(31, 'admin_interface', '0013_add_related_modal_close_button', '2024-03-29 08:10:40.654103'),
(32, 'admin_interface', '0014_name_unique', '2024-03-29 08:10:40.687624'),
(33, 'admin_interface', '0015_add_language_chooser_active', '2024-03-29 08:10:40.738106'),
(34, 'admin_interface', '0016_add_language_chooser_display', '2024-03-29 08:10:40.788251'),
(35, 'admin_interface', '0017_change_list_filter_dropdown', '2024-03-29 08:10:40.795254'),
(36, 'admin_interface', '0018_theme_list_filter_sticky', '2024-03-29 08:10:40.847858'),
(37, 'admin_interface', '0019_add_form_sticky', '2024-03-29 08:10:40.955165'),
(38, 'admin_interface', '0020_module_selected_colors', '2024-03-29 08:10:41.065533'),
(39, 'admin_interface', '0021_file_extension_validator', '2024-03-29 08:10:41.076503'),
(40, 'admin_interface', '0022_add_logo_max_width_and_height', '2024-03-29 08:10:41.330491'),
(41, 'admin_interface', '0023_theme_foldable_apps', '2024-03-29 08:10:41.379923'),
(42, 'admin_interface', '0024_remove_theme_css', '2024-03-29 08:10:41.483653'),
(43, 'admin_interface', '0025_theme_language_chooser_control', '2024-03-29 08:10:41.535388'),
(44, 'admin_interface', '0026_theme_list_filter_highlight', '2024-03-29 08:10:41.582539'),
(45, 'admin_interface', '0027_theme_list_filter_removal_links', '2024-03-29 08:10:41.635372'),
(46, 'admin_interface', '0028_theme_show_fieldsets_as_tabs_and_more', '2024-03-29 08:10:41.738921'),
(47, 'admin_interface', '0029_theme_css_generic_link_active_color', '2024-03-29 08:10:41.786854'),
(48, 'admin_interface', '0030_theme_collapsible_stacked_inlines_and_more', '2024-03-29 08:10:41.978222'),
(49, 'authtoken', '0001_initial', '2024-03-29 08:10:42.160125'),
(50, 'authtoken', '0002_auto_20160226_1747', '2024-03-29 08:10:42.211008'),
(51, 'authtoken', '0003_tokenproxy', '2024-03-29 08:10:42.214973'),
(52, 'measurement', '0001_initial', '2024-03-29 08:10:43.597162'),
(53, 'monitoring', '0001_initial', '2024-03-29 08:10:44.347169'),
(54, 'sessions', '0001_initial', '2024-03-29 08:10:44.410025'),
(55, 'settings_module', '0001_initial', '2024-03-29 08:10:44.744309'),
(56, 'access', '0002_alter_customuser_role', '2024-03-29 08:47:49.154635'),
(57, 'access', '0003_alter_customuser_role', '2024-03-29 09:07:31.840762'),
(58, 'access', '0004_alter_customuser_role', '2024-03-29 09:11:56.364533'),
(59, 'monitoring', '0002_alter_referral_referred_to', '2024-03-29 09:37:08.986547'),
(60, 'monitoring', '0003_alter_referral_referred_to_name', '2024-03-29 09:41:17.260277'),
(61, 'monitoring', '0004_referral_service_and_treatment_and_more', '2024-03-29 12:22:16.742886'),
(62, 'monitoring', '0005_rescreening_rescreening_count', '2024-03-30 08:01:25.578765'),
(63, 'reporting', '0001_initial', '2024-03-30 09:49:24.729131'),
(64, 'reporting', '0002_reporting_alcoholic_flag_and_more', '2024-03-30 09:58:24.854523'),
(65, 'measurement', '0002_alter_measurement_user_submission_and_more', '2024-03-30 15:15:22.659517'),
(66, 'measurement', '0003_alter_usersubmission_test_type', '2024-03-31 07:21:11.419683'),
(67, 'reporting', '0003_reporting_past_diagnosis', '2024-03-31 07:21:11.471365'),
(68, 'screening', '0001_initial', '2024-03-31 11:54:08.904606'),
(69, 'screening', '0002_remove_eventscreening_user_screeneduser', '2024-03-31 11:59:30.637361'),
(70, 'screening', '0003_alter_eventscreening_approval_status', '2024-03-31 16:12:30.544935'),
(71, 'screening', '0004_alter_eventscreening_approval_status', '2024-03-31 16:26:37.879427'),
(72, 'screening', '0005_alter_screeneduser_user', '2024-03-31 17:06:35.997861'),
(73, 'settings_module', '0002_video', '2024-04-01 04:38:21.109294'),
(74, 'measurement', '0004_activeuser_lifetimeuser', '2024-04-01 06:50:48.742031'),
(75, 'settings_module', '0003_notification', '2024-04-01 06:50:48.934406'),
(76, 'measurement', '0005_alter_activeuser_substances_used_and_more', '2024-04-01 09:53:56.559715');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('93fkwlev5hz1iqsat8y6qe0krwm6n8d6', '.eJxVjMsOwiAQRf-FtSEC5TEu3fsNZGAGqRqalHZl_HfbpAvd3nPOfYuI61Lj2nmOI4mLUOL0uyXMT247oAe2-yTz1JZ5THJX5EG7vE3Er-vh_h1U7HWrkYuHlL09k4MMDFgwDMoaU5IHT4aDDo5NwcEbVhqstpSZeUtc1iA-X_zTOF0:1rqTNM:f_kOsJ2dQMAK3FthT2J7wn7fccPMVh3bPtZNqUL6ouw', '2024-04-13 07:43:40.893137'),
('9lcpiwbsi6m9dzzv2b25mzk7obtypvbt', '.eJxVjMsOwiAQRf-FtSEC5TEu3fsNZGAGqRqalHZl_HfbpAvd3nPOfYuI61Lj2nmOI4mLUOL0uyXMT247oAe2-yTz1JZ5THJX5EG7vE3Er-vh_h1U7HWrkYuHlL09k4MMDFgwDMoaU5IHT4aDDo5NwcEbVhqstpSZeUtc1iA-X_zTOF0:1rq7Qi:S8qdQdDm-EqWIid5Xg6JBsRVXrUGCEGO6WXqQWcCoT8', '2024-04-12 08:17:40.757526'),
('9m5jthy7yow89w16dkvrno3ida2vc8qn', '.eJyNUcFOwzAM_ZUoZxCdYKu2I0NwYMdJHCO3yVKLxJmSlGmb9u84LbCeJqQckvde7Ge_s-yTiUpDBrk6S9SGMuajot43JsqVnM3m1aKq5tWykndyhzFlReANU-9IJyDLsEetnfnFGXBwlb0YDwxxC6PCTjUYc1cKL5dP99UjHyatIT20e2WxM6VkaCYm6nld1fWC8b2JXoHW6gudA1sabDrwAcWm9-LhLeyRcKqz5hBssdGT5Q-j4T9WnwLZzw6KYpswjjRBxkDgeBOMP3d9BjKp2NpB7nhfP6NteCaxBdJIQnzwX42D9almmzpzYEqIdRd4vaV7-tcE6Yb_dMP9kGgMHAhXp_Y4RjKgLQeTJu_UN1MMWtDGH1XLRq-qa6x7Vh5C1OOLo0JXrpfLNyc9wV0:1rrV6L:qC0ONQI09cwAfzQvDLLtiu7Pl62HiQB9wUVRFx99TPw', '2024-04-16 03:46:21.735637'),
('onoliolfcvrjgx84lp3k5ijdzn6rcft8', '.eJyNUcFOwzAM_ZUoZxCdYKu2I0NwYMdJHCO3yVKLxJmSlGmb9u84LbCeJqQckvde7Ge_s-yTiUpDBrk6S9SGMuajot43JsqVnM3m1aKq5tWykndyhzFlReANU-9IJyDLsEetnfnFGXBwlb0YDwxxC6PCTjUYc1cKL5dP99UjHyatIT20e2WxM6VkaCYm6nld1fWC8b2JXoHW6gudA1sabDrwAcWm9-LhLeyRcKqz5hBssdGT5Q-j4T9WnwLZzw6KYpswjjRBxkDgeBOMP3d9BjKp2NpB7nhfP6NteCaxBdJIQnzwX42D9almmzpzYEqIdRd4vaV7-tcE6Yb_dMP9kGgMHAhXp_Y4RjKgLQeTJu_UN1MMWtDGH1XLRq-qa6x7Vh5C1OOLo0JXrpfLNyc9wV0:1rrUtK:fTJrgjSX9Nh8twJkpQ06lAYzUwHAusFlrCZbNankfkA', '2024-04-16 03:32:54.674892');

-- --------------------------------------------------------

--
-- Table structure for table `measurement_activeuser`
--

CREATE TABLE `measurement_activeuser` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_activeuser`
--

INSERT INTO `measurement_activeuser` (`id`, `user_id`, `user_submission_id`) VALUES
(1, 2, 29),
(3, 6, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_activeuser_substances_used`
--

CREATE TABLE `measurement_activeuser_substances_used` (
  `id` bigint NOT NULL,
  `activeuser_id` bigint NOT NULL,
  `measurementsubstance_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `measurement_lifetimeuser`
--

CREATE TABLE `measurement_lifetimeuser` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_lifetimeuser`
--

INSERT INTO `measurement_lifetimeuser` (`id`, `user_id`, `user_submission_id`) VALUES
(1, 6, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_lifetimeuser_substances_used`
--

CREATE TABLE `measurement_lifetimeuser_substances_used` (
  `id` bigint NOT NULL,
  `lifetimeuser_id` bigint NOT NULL,
  `measurementsubstance_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_lifetimeuser_substances_used`
--

INSERT INTO `measurement_lifetimeuser_substances_used` (`id`, `lifetimeuser_id`, `measurementsubstance_id`) VALUES
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_measurement`
--

CREATE TABLE `measurement_measurement` (
  `id` bigint NOT NULL,
  `gad_measurement` varchar(50) DEFAULT NULL,
  `gad_flag` varchar(10) DEFAULT NULL,
  `phq_measurement` varchar(50) DEFAULT NULL,
  `phq_flag` varchar(10) DEFAULT NULL,
  `suicidal_measurement` varchar(50) DEFAULT NULL,
  `suicidal_flag` varchar(10) DEFAULT NULL,
  `ace_measurement` varchar(50) DEFAULT NULL,
  `ace_flag` varchar(10) DEFAULT NULL,
  `overall_flag` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `assist_id` bigint DEFAULT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_measurement`
--

INSERT INTO `measurement_measurement` (`id`, `gad_measurement`, `gad_flag`, `phq_measurement`, `phq_flag`, `suicidal_measurement`, `suicidal_flag`, `ace_measurement`, `ace_flag`, `overall_flag`, `created_at`, `user_id`, `assist_id`, `user_submission_id`) VALUES
(2, 'moderate', 'yellow', 'moderately severe', 'orange', 'more than half the days', 'orange', NULL, NULL, NULL, '2024-03-29 09:13:21.219687', 4, NULL, 28),
(25, 'minimal', 'green', 'minimal', 'green', NULL, NULL, NULL, NULL, NULL, '2024-04-01 07:08:27.435016', 2, NULL, 29),
(27, 'minimal', 'green', 'minimal', 'green', NULL, NULL, NULL, NULL, NULL, '2024-04-01 09:14:58.752114', 6, NULL, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_measurementassist`
--

CREATE TABLE `measurement_measurementassist` (
  `id` bigint NOT NULL,
  `alcoholic_measurement` varchar(50) DEFAULT NULL,
  `alcoholic_flag` varchar(50) DEFAULT NULL,
  `tobacco_measurement` varchar(50) DEFAULT NULL,
  `tobacco_flag` varchar(50) DEFAULT NULL,
  `cannabis_measurement` varchar(50) DEFAULT NULL,
  `cannabis_flag` varchar(50) DEFAULT NULL,
  `cocaine_measurement` varchar(50) DEFAULT NULL,
  `cocaine_flag` varchar(50) DEFAULT NULL,
  `amphetamine_measurement` varchar(50) DEFAULT NULL,
  `amphetamine_flag` varchar(50) DEFAULT NULL,
  `inhalants_measurement` varchar(50) DEFAULT NULL,
  `inhalants_flag` varchar(50) DEFAULT NULL,
  `sedatives_measurement` varchar(50) DEFAULT NULL,
  `sedatives_flag` varchar(50) DEFAULT NULL,
  `hallucinogens_measurement` varchar(50) DEFAULT NULL,
  `hallucinogens_flag` varchar(50) DEFAULT NULL,
  `opioids_measurement` varchar(50) DEFAULT NULL,
  `opioids_flag` varchar(50) DEFAULT NULL,
  `injection_measurement` varchar(50) DEFAULT NULL,
  `injection_flag` varchar(50) DEFAULT NULL,
  `other_measurement` varchar(50) DEFAULT NULL,
  `other_flag` varchar(50) DEFAULT NULL,
  `other_name` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_measurementassist`
--

INSERT INTO `measurement_measurementassist` (`id`, `alcoholic_measurement`, `alcoholic_flag`, `tobacco_measurement`, `tobacco_flag`, `cannabis_measurement`, `cannabis_flag`, `cocaine_measurement`, `cocaine_flag`, `amphetamine_measurement`, `amphetamine_flag`, `inhalants_measurement`, `inhalants_flag`, `sedatives_measurement`, `sedatives_flag`, `hallucinogens_measurement`, `hallucinogens_flag`, `opioids_measurement`, `opioids_flag`, `injection_measurement`, `injection_flag`, `other_measurement`, `other_flag`, `other_name`, `created_at`, `user_id`, `user_submission_id`) VALUES
(2, 'high risk', 'red', 'moderate risk', 'yellow', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'no risk', 'green', 'low risk', 'blue', NULL, '2024-03-29 09:13:21.343341', 4, 28),
(3, 'moderate risk', 'yellow', 'moderate risk', 'yellow', 'moderate risk', 'yellow', 'no risk', '', 'no risk', '', 'no risk', '', 'no risk', '', 'no risk', '', 'no risk', '', 'no risk', 'green', 'no risk', '', NULL, '2024-04-01 07:08:27.475935', 2, 29),
(5, 'low risk', 'blue', 'moderate risk', 'yellow', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'low risk', 'blue', 'no risk', 'green', 'low risk', 'blue', NULL, '2024-04-01 09:14:58.782361', 6, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_measurementsubstance`
--

CREATE TABLE `measurement_measurementsubstance` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_measurementsubstance`
--

INSERT INTO `measurement_measurementsubstance` (`id`, `name`) VALUES
(1, 'Tobacco products (cigarettes'),
(2, 'chewing tobacco etc)');

-- --------------------------------------------------------

--
-- Table structure for table `measurement_questionset`
--

CREATE TABLE `measurement_questionset` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `test_type_id` bigint NOT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_questionset`
--

INSERT INTO `measurement_questionset` (`id`, `name`, `test_type_id`, `user_submission_id`) VALUES
(8, 'PRE-CLUSTER', 2, 28),
(9, 'PHQ2', 2, 28),
(10, 'PHQ9', 2, 28),
(11, 'GAD2', 2, 28),
(12, 'GAD7', 2, 28),
(13, 'ASSIST', 2, 28),
(14, 'SCHOOL ENV', 2, 28),
(15, 'PRE-CLUSTER', 2, 29),
(16, 'PHQ2', 2, 29),
(17, 'GAD2', 2, 29),
(18, 'ASSIST', 2, 29),
(19, 'GAD7', 2, 29),
(20, 'SCHOOL ENV', 2, 29),
(26, 'PRE-CLUSTER', 2, 31),
(27, 'PHQ2', 2, 31),
(28, 'GAD2', 2, 31),
(29, 'ASSIST', 2, 31),
(30, 'SCHOOL ENV', 2, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_submission`
--

CREATE TABLE `measurement_submission` (
  `id` bigint NOT NULL,
  `question` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `score` int DEFAULT NULL,
  `substance` varchar(100) NOT NULL,
  `specify` varchar(100) NOT NULL,
  `diagnosis` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `question_set_id` bigint NOT NULL,
  `user_submission_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_submission`
--

INSERT INTO `measurement_submission` (`id`, `question`, `answer`, `score`, `substance`, `specify`, `diagnosis`, `created_at`, `question_set_id`, `user_submission_id`) VALUES
(65, 'Have you been diagnosed with any mental illness in the past before?', 'No', 0, '', '', '', '2024-03-29 09:13:21.077229', 8, 28),
(66, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nLittle interest or pleasure in doing things', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.085933', 9, 28),
(67, 'Feeling down, depressed or hopeless', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.087667', 9, 28),
(68, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nTrouble falling or staying asleep, or sleeping too much', 'Nearly everyday', 3, '', '', '', '2024-03-29 09:13:21.094637', 10, 28),
(69, 'Feeling tired or having little energy', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.096372', 10, 28),
(70, 'Poor appetite, weight loss or overeating', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.098111', 10, 28),
(71, 'Feeling bad about yourself -or feeling that you are a failure or have let yourself or your family down', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.101591', 10, 28),
(72, 'Trouble concentrating on things, such as school work, reading or watching television', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.103390', 10, 28),
(73, 'Moving or speaking so slowly that other people could have noticed. Or the opposite being so fidgety or restless that you have been moving around a lot more than usual', 'Nearly everyday', 3, '', '', '', '2024-03-29 09:13:21.103390', 10, 28),
(74, 'Thoughts that you would be better off dead, or of hurting yourself', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.105771', 10, 28),
(75, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nFeeling nervous, anxious, or on edge', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.114042', 11, 28),
(76, 'Not being able to stop or control worrying', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.115443', 11, 28),
(77, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nWorrying too much about different things', 'Nearly everyday', 3, '', '', '', '2024-03-29 09:13:21.121819', 12, 28),
(78, 'Trouble relaxing', 'More than half the days', 2, '', '', '', '2024-03-29 09:13:21.122638', 12, 28),
(79, 'Being so restless that it is hard to sit still', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.124405', 12, 28),
(80, 'Becoming easily annoyed or irritable', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.126145', 12, 28),
(81, 'Feeling afraid, as if something awful might happen', 'Several days', 1, '', '', '', '2024-03-29 09:13:21.127891', 12, 28),
(82, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.134254', 13, 28),
(83, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.135572', 13, 28),
(84, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-03-29 09:13:21.135572', 13, 28),
(85, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Cocaine (Cocaine, Coke, Blow, Snow)', '', '', '2024-03-29 09:13:21.137327', 13, 28),
(86, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Amphetamine-type stimulants (speed, meth, ecstasy, ice, diet pills etc.)', '', '', '2024-03-29 09:13:21.140070', 13, 28),
(87, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Inhalants (dendrite, glue, petrol, paint thinner, etc.)', '', '', '2024-03-29 09:13:21.141209', 13, 28),
(88, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Sedatives or Sleeping Pills (Valium,Temazepam, Amitriptyline, N-10, diazepam etc.)', '', '', '2024-03-29 09:13:21.142695', 13, 28),
(89, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Hallucinogens (LSD, acid,, trips, Ketamine, etc.)', '', '', '2024-03-29 09:13:21.144319', 13, 28),
(90, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Opioids (heroin, morphine, fentanyl, codeine, SP+, tramadol, BS etc.)', '', '', '2024-03-29 09:13:21.145858', 13, 28),
(91, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Other - specify', '', '', '2024-03-29 09:13:21.146369', 13, 28),
(92, 'In the past three months, how often have you used?', 'Weekly, 1 to 4 times per week', 4, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.149370', 13, 28),
(93, 'In the past three months, how often have you used?', 'Weekly, 1 to 4 times per week', 4, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.151467', 13, 28),
(94, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Weekly, 1 to 4 times per week', 5, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.151467', 13, 28),
(95, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Weekly, 1 to 4 times per week', 5, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.154582', 13, 28),
(96, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Weekly, 1 to 4 times per week', 6, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.156104', 13, 28),
(97, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Weekly, 1 to 4 times per week', 6, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.157996', 13, 28),
(98, 'Has your use of the substance impacted on your usual activities? (eg. school attendance, involvement in recreational activities or sport, completion of chores, family expectations, family events, homework etc). If YES, how often has this happened in the last 3 months for each substance?', 'Daily or Almost Daily, 5 to 7 days per week', 8, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.158504', 13, 28),
(99, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'Yes, but not in the past 3 months', 3, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.160259', 13, 28),
(100, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'Yes, In the past 3 months', 6, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.161998', 13, 28),
(101, 'Have you ever tried and failed to control, cut down or stop using the substances?', 'Yes, In the past 3 months', 6, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-03-29 09:13:21.163739', 13, 28),
(102, 'Have you ever tried and failed to control, cut down or stop using the substances?', 'Yes, In the past 3 months', 6, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-03-29 09:13:21.165480', 13, 28),
(103, 'Have you ever used any drug by injection? (NON-MEDICAL USE ONLY)', 'Yes, In the past 3 months', 6, 'Any Drug', '', '', '2024-03-29 09:13:21.167219', 13, 28),
(104, 'I feel safe at school', 'Strongly Agree', NULL, '', '', '', '2024-03-29 09:13:21.174182', 14, 28),
(105, 'My school is free of corporal punishment', 'Agree', NULL, '', '', '', '2024-03-29 09:13:21.175918', 14, 28),
(106, 'I feel motivated to come to school', 'Neutral/Indifferent', NULL, '', '', '', '2024-03-29 09:13:21.177659', 14, 28),
(107, 'My teachers and other staff are helpful and supportive', 'Neutral/Indifferent', NULL, '', '', '', '2024-03-29 09:13:21.181139', 14, 28),
(108, 'My school is free of bullying', 'Neutral/Indifferent', NULL, '', '', '', '2024-03-29 09:13:21.182880', 14, 28),
(109, 'All the students receive fair treatment at school', 'Disagree', NULL, '', '', '', '2024-03-29 09:13:21.184621', 14, 28),
(110, 'My school engages all the students in all school activities', 'Disagree', NULL, '', '', '', '2024-03-29 09:13:21.186360', 14, 28),
(111, 'Students get along well with each other in our school', 'Neutral/Indifferent', NULL, '', '', '', '2024-03-29 09:13:21.188100', 14, 28),
(112, 'What do you like the most about your school? (Mention two things)', 'a', NULL, '', '', '', '2024-03-29 09:13:21.189839', 14, 28),
(113, 'What do you like the most about your school? (Mention two things)', 's', NULL, '', '', '', '2024-03-29 09:13:21.191582', 14, 28),
(114, 'What changes do you really wish to see in your school? (mention two things)', 'd', NULL, '', '', '', '2024-03-29 09:13:21.193320', 14, 28),
(115, 'What changes do you really wish to see in your school? (mention two things)', 'f', NULL, '', '', '', '2024-03-29 09:13:21.195705', 14, 28),
(116, 'Have you been diagnosed with any mental illness in the past before?', 'No', 0, '', '', '', '2024-04-01 07:08:27.370013', 15, 29),
(117, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nLittle interest or pleasure in doing things', 'Not at all', 0, '', '', '', '2024-04-01 07:08:27.374360', 16, 29),
(118, 'Feeling down, depressed or hopeless', 'Not at all', 0, '', '', '', '2024-04-01 07:08:27.375360', 16, 29),
(119, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nFeeling nervous, anxious, or on edge', 'Not at all', 0, '', '', '', '2024-04-01 07:08:27.378374', 17, 29),
(120, 'Not being able to stop or control worrying', 'Not at all', 0, '', '', '', '2024-04-01 07:08:27.379364', 17, 29),
(121, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 07:08:27.384161', 18, 29),
(122, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.385055', 18, 29),
(123, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.386575', 18, 29),
(124, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Cocaine (Cocaine, Coke, Blow, Snow)', '', '', '2024-04-01 07:08:27.387689', 18, 29),
(125, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Amphetamine-type stimulants (speed, meth, ecstasy, ice, diet pills etc.)', '', '', '2024-04-01 07:08:27.388703', 18, 29),
(126, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Inhalants (dendrite, glue, petrol, paint thinner, etc.)', '', '', '2024-04-01 07:08:27.388703', 18, 29),
(127, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Sedatives or Sleeping Pills (Valium,Temazepam, Amitriptyline, N-10, diazepam etc.)', '', '', '2024-04-01 07:08:27.389699', 18, 29),
(128, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Hallucinogens (LSD, acid,, trips, Ketamine, etc.)', '', '', '2024-04-01 07:08:27.390700', 18, 29),
(129, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Opioids (heroin, morphine, fentanyl, codeine, SP+, tramadol, BS etc.)', '', '', '2024-04-01 07:08:27.390700', 18, 29),
(130, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Other - specify', '', '', '2024-04-01 07:08:27.391702', 18, 29),
(131, 'In the past three months, how often have you used?', 'Once or Twice, in the last 3 months', 2, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 07:08:27.392699', 18, 29),
(132, 'In the past three months, how often have you used?', 'Monthly, 1 to 3 times in a month in the last 3 months', 3, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.393702', 18, 29),
(133, 'In the past three months, how often have you used?', 'Weekly, 1 to 4 times per week', 4, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.393702', 18, 29),
(134, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Once or Twice, in the last 3 months', 3, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 07:08:27.394714', 18, 29),
(135, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Monthly, 1 to 3 times in a month in the last 3 months', 4, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.395697', 18, 29),
(136, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Once or Twice, in the last 3 months', 3, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.396700', 18, 29),
(137, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Monthly, 1 to 3 times in a month in the last 3 months', 5, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.397703', 18, 29),
(138, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Weekly, 1 to 4 times per week', 6, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.400704', 18, 29),
(139, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Daily or Almost Daily, 5 to 7 days per week', 7, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 07:08:27.401698', 18, 29),
(140, 'Has your use of the substance impacted on your usual activities? (eg. school attendance, involvement in recreational activities or sport, completion of chores, family expectations, family events, homework etc). If YES, how often has this happened in the last 3 months for each substance?', 'Monthly, 1 to 3 times in a month in the last 3 months', 6, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.402968', 18, 29),
(141, 'Has your use of the substance impacted on your usual activities? (eg. school attendance, involvement in recreational activities or sport, completion of chores, family expectations, family events, homework etc). If YES, how often has this happened in the last 3 months for each substance?', 'Once or Twice, in the last 3 months', 5, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.403966', 18, 29),
(142, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'Yes, In the past 3 months', 6, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 07:08:27.404967', 18, 29),
(143, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'No, Never', 0, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 07:08:27.404967', 18, 29),
(144, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'No, Never', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 07:08:27.405969', 18, 29),
(145, 'Feeling afraid, as if something awful might happen', 'Not at all', 0, '', '', '', '2024-04-01 07:08:27.408969', 19, 29),
(146, 'I feel safe at school', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.412967', 20, 29),
(147, 'My school is free of corporal punishment', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.413966', 20, 29),
(148, 'I feel motivated to come to school', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.415364', 20, 29),
(149, 'My teachers and other staff are helpful and supportive', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.417081', 20, 29),
(150, 'My school is free of bullying', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.418088', 20, 29),
(151, 'All the students receive fair treatment at school', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.418088', 20, 29),
(152, 'My school engages all the students in all school activities', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.419085', 20, 29),
(153, 'Students get along well with each other in our school', 'Agree', NULL, '', '', '', '2024-04-01 07:08:27.420085', 20, 29),
(154, 'What do you like the most about your school? (Mention two things)', 'a', NULL, '', '', '', '2024-04-01 07:08:27.420085', 20, 29),
(155, 'What do you like the most about your school? (Mention two things)', 's', NULL, '', '', '', '2024-04-01 07:08:27.421085', 20, 29),
(156, 'What changes do you really wish to see in your school? (mention two things)', 'd', NULL, '', '', '', '2024-04-01 07:08:27.421085', 20, 29),
(157, 'What changes do you really wish to see in your school? (mention two things)', 'f', NULL, '', '', '', '2024-04-01 07:08:27.422083', 20, 29),
(197, 'Have you been diagnosed with any mental illness in the past before?', 'No', 0, '', '', '', '2024-04-01 09:14:58.700910', 26, 31),
(198, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nLittle interest or pleasure in doing things', 'Several days', 1, '', '', '', '2024-04-01 09:14:58.707904', 27, 31),
(199, 'Feeling down, depressed or hopeless', 'Not at all', 0, '', '', '', '2024-04-01 09:14:58.708910', 27, 31),
(200, 'Over the last 2 weeks, how often have you been bothered by any of the following problems? \r\nFeeling nervous, anxious, or on edge', 'Not at all', 0, '', '', '', '2024-04-01 09:14:58.713905', 28, 31),
(201, 'Not being able to stop or control worrying', 'Not at all', 0, '', '', '', '2024-04-01 09:14:58.714908', 28, 31),
(202, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'Yes', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.716904', 29, 31),
(203, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Alcoholic beverages (beer, wine, spirits, ara etc.)', '', '', '2024-04-01 09:14:58.716904', 29, 31),
(204, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Cannabis (marijuana, pot, grass, hash, black etc.)', '', '', '2024-04-01 09:14:58.717903', 29, 31),
(205, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Cocaine (Cocaine, Coke, Blow, Snow)', '', '', '2024-04-01 09:14:58.718902', 29, 31),
(206, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Amphetamine-type stimulants (speed, meth, ecstasy, ice, diet pills etc.)', '', '', '2024-04-01 09:14:58.718902', 29, 31),
(207, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Inhalants (dendrite, glue, petrol, paint thinner, etc.)', '', '', '2024-04-01 09:14:58.719905', 29, 31),
(208, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Sedatives or Sleeping Pills (Valium,Temazepam, Amitriptyline, N-10, diazepam etc.)', '', '', '2024-04-01 09:14:58.720905', 29, 31),
(209, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Hallucinogens (LSD, acid,, trips, Ketamine, etc.)', '', '', '2024-04-01 09:14:58.720905', 29, 31),
(210, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Opioids (heroin, morphine, fentanyl, codeine, SP+, tramadol, BS etc.)', '', '', '2024-04-01 09:14:58.721907', 29, 31),
(211, 'In your life, have you ever tried (NON-MEDICAL USE ONLY):', 'No', 0, 'Other - specify', '', '', '2024-04-01 09:14:58.722906', 29, 31),
(212, 'In the past three months, how often have you used?', 'Never, not used in the last 3 months', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.723906', 29, 31),
(213, 'Have you found yourself using the substance when you are away from your usual social situations or friends (eg. maybe when you are alone)? If YES, how often has that happened in the last 3 months for the following?', 'Never, not used in the last 3 months', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.723906', 29, 31),
(214, 'Has your use of substance led to problems with your health, relationships, finances, school, or with the police? If YES, how often has that happened in the last 3 months for (FIRST DRUG, SECOND DRUG, ETC)?', 'Never, not used in the last 3 months', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.724904', 29, 31),
(215, 'Has a friend or relative or anyone else ever expressed concern (or worry) about your use of the substances? If YES, was it within the last 3 months or before that for (FIRST DRUG, SECOND DRUG, ETC)?', 'No, Never', 0, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.724904', 29, 31),
(216, 'Have you ever tried and failed to control, cut down or stop using the substances?', 'Yes, In the past 3 months', 6, 'Tobacco products (cigarettes, chewing tobacco etc)', '', '', '2024-04-01 09:14:58.725904', 29, 31),
(217, 'Have you ever used any drug by injection? (NON-MEDICAL USE ONLY)', 'No, Never', 0, 'Any Drug', '', '', '2024-04-01 09:14:58.725904', 29, 31),
(218, 'I feel safe at school', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.729905', 30, 31),
(219, 'My school is free of corporal punishment', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.731908', 30, 31),
(220, 'I feel motivated to come to school', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.731908', 30, 31),
(221, 'My teachers and other staff are helpful and supportive', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.732903', 30, 31),
(222, 'My school is free of bullying', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.733904', 30, 31),
(223, 'All the students receive fair treatment at school', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.734909', 30, 31),
(224, 'My school engages all the students in all school activities', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.734909', 30, 31),
(225, 'Students get along well with each other in our school', 'Strongly Agree', NULL, '', '', '', '2024-04-01 09:14:58.736923', 30, 31),
(226, 'What do you like the most about your school? (Mention two things)', 'a', NULL, '', '', '', '2024-04-01 09:14:58.736923', 30, 31),
(227, 'What do you like the most about your school? (Mention two things)', 's', NULL, '', '', '', '2024-04-01 09:14:58.737919', 30, 31),
(228, 'What changes do you really wish to see in your school? (mention two things)', 'd', NULL, '', '', '', '2024-04-01 09:14:58.738918', 30, 31),
(229, 'What changes do you really wish to see in your school? (mention two things)', 'f', NULL, '', '', '', '2024-04-01 09:14:58.740921', 30, 31);

-- --------------------------------------------------------

--
-- Table structure for table `measurement_testtype`
--

CREATE TABLE `measurement_testtype` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_testtype`
--

INSERT INTO `measurement_testtype` (`id`, `name`) VALUES
(2, 'Cluster Screening');

-- --------------------------------------------------------

--
-- Table structure for table `measurement_usersubmission`
--

CREATE TABLE `measurement_usersubmission` (
  `id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `test_type_id` bigint NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `measurement_usersubmission`
--

INSERT INTO `measurement_usersubmission` (`id`, `created_at`, `test_type_id`, `user_id`) VALUES
(28, '2024-03-29 09:13:21.068533', 2, 4),
(29, '2024-04-01 07:08:27.362733', 2, 2),
(31, '2024-04-01 09:14:58.692903', 2, 6);

-- --------------------------------------------------------

--
-- Table structure for table `monitoring_referral`
--

CREATE TABLE `monitoring_referral` (
  `id` bigint NOT NULL,
  `date` date NOT NULL,
  `referred_to_name` varchar(100) DEFAULT NULL,
  `referral_status` varchar(20) NOT NULL,
  `referral_remarks` longtext,
  `referred_by_id` int DEFAULT NULL,
  `referred_to_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `service_and_treatment_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `monitoring_referral`
--

INSERT INTO `monitoring_referral` (`id`, `date`, `referred_to_name`, `referral_status`, `referral_remarks`, `referred_by_id`, `referred_to_id`, `user_id`, `service_and_treatment_id`) VALUES
(1, '2024-03-29', '', 'Awaiting', NULL, NULL, NULL, 2, NULL),
(2, '2024-03-29', '', 'Awaiting', NULL, NULL, NULL, 4, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `monitoring_rescreening`
--

CREATE TABLE `monitoring_rescreening` (
  `id` bigint NOT NULL,
  `date` date NOT NULL,
  `submission_diagnosis` varchar(255) NOT NULL,
  `measurement` json NOT NULL,
  `measurement_assist` json NOT NULL,
  `user_id` int NOT NULL,
  `service_and_treatment_id` bigint DEFAULT NULL,
  `rescreening_count` int UNSIGNED NOT NULL
) ;

--
-- Dumping data for table `monitoring_rescreening`
--

INSERT INTO `monitoring_rescreening` (`id`, `date`, `submission_diagnosis`, `measurement`, `measurement_assist`, `user_id`, `service_and_treatment_id`, `rescreening_count`) VALUES
(1, '2024-03-29', 'My Sickness', '{\"gad_flag\": \"yellow\", \"phq_flag\": \"orange\", \"gad_measurement\": \"moderate\", \"phq_measurement\": \"moderately severe\"}', '{\"other_flag\": \"red\", \"cocaine_flag\": \"red\", \"opioids_flag\": \"\", \"tobacco_flag\": \"yellow\", \"cannabis_flag\": \"\", \"alcoholic_flag\": \"yellow\", \"inhalants_flag\": \"\", \"injection_flag\": \"green\", \"sedatives_flag\": \"\", \"amphetamine_flag\": \"\", \"other_measurement\": \"high risk\", \"hallucinogens_flag\": \"red\", \"cocaine_measurement\": \"high risk\", \"opioids_measurement\": \"no risk\", \"tobacco_measurement\": \"moderate risk\", \"cannabis_measurement\": \"no risk\", \"alcoholic_measurement\": \"moderate risk\", \"inhalants_measurement\": \"no risk\", \"injection_measurement\": \"no risk\", \"sedatives_measurement\": \"no risk\", \"amphetamine_measurement\": \"no risk\", \"hallucinogens_measurement\": \"high risk\"}', 2, NULL, 0),
(2, '2024-03-29', '', '{\"gad_flag\": \"yellow\", \"phq_flag\": \"orange\", \"gad_measurement\": \"moderate\", \"phq_measurement\": \"moderately severe\"}', '{\"other_flag\": \"blue\", \"cocaine_flag\": \"blue\", \"opioids_flag\": \"blue\", \"tobacco_flag\": \"yellow\", \"cannabis_flag\": \"blue\", \"alcoholic_flag\": \"red\", \"inhalants_flag\": \"blue\", \"injection_flag\": \"green\", \"sedatives_flag\": \"blue\", \"amphetamine_flag\": \"blue\", \"other_measurement\": \"low risk\", \"hallucinogens_flag\": \"blue\", \"cocaine_measurement\": \"low risk\", \"opioids_measurement\": \"low risk\", \"tobacco_measurement\": \"moderate risk\", \"cannabis_measurement\": \"low risk\", \"alcoholic_measurement\": \"high risk\", \"inhalants_measurement\": \"low risk\", \"injection_measurement\": \"no risk\", \"sedatives_measurement\": \"low risk\", \"amphetamine_measurement\": \"low risk\", \"hallucinogens_measurement\": \"low risk\"}', 4, NULL, 0),
(3, '2024-04-01', '', '{\"gad_flag\": null, \"phq_flag\": null, \"gad_measurement\": null, \"phq_measurement\": null}', '{\"other_flag\": \"\", \"cocaine_flag\": \"\", \"opioids_flag\": \"\", \"tobacco_flag\": \"yellow\", \"cannabis_flag\": \"yellow\", \"alcoholic_flag\": \"yellow\", \"inhalants_flag\": \"\", \"injection_flag\": \"green\", \"sedatives_flag\": \"\", \"amphetamine_flag\": \"\", \"other_measurement\": \"no risk\", \"hallucinogens_flag\": \"\", \"cocaine_measurement\": \"no risk\", \"opioids_measurement\": \"no risk\", \"tobacco_measurement\": \"moderate risk\", \"cannabis_measurement\": \"moderate risk\", \"alcoholic_measurement\": \"moderate risk\", \"inhalants_measurement\": \"no risk\", \"injection_measurement\": \"no risk\", \"sedatives_measurement\": \"no risk\", \"amphetamine_measurement\": \"no risk\", \"hallucinogens_measurement\": \"no risk\"}', 2, NULL, 0),
(4, '2024-04-01', '', '{\"gad_flag\": null, \"phq_flag\": null, \"gad_measurement\": null, \"phq_measurement\": null}', '{\"other_flag\": \"blue\", \"cocaine_flag\": \"blue\", \"opioids_flag\": \"blue\", \"tobacco_flag\": \"yellow\", \"cannabis_flag\": \"blue\", \"alcoholic_flag\": \"yellow\", \"inhalants_flag\": \"blue\", \"injection_flag\": \"green\", \"sedatives_flag\": \"blue\", \"amphetamine_flag\": \"blue\", \"other_measurement\": \"low risk\", \"hallucinogens_flag\": \"blue\", \"cocaine_measurement\": \"low risk\", \"opioids_measurement\": \"low risk\", \"tobacco_measurement\": \"moderate risk\", \"cannabis_measurement\": \"low risk\", \"alcoholic_measurement\": \"moderate risk\", \"inhalants_measurement\": \"low risk\", \"injection_measurement\": \"no risk\", \"sedatives_measurement\": \"low risk\", \"amphetamine_measurement\": \"low risk\", \"hallucinogens_measurement\": \"low risk\"}', 6, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `monitoring_serviceandtreatment`
--

CREATE TABLE `monitoring_serviceandtreatment` (
  `id` bigint NOT NULL,
  `date` date NOT NULL,
  `assessment_status` varchar(20) NOT NULL,
  `case_status` varchar(20) NOT NULL,
  `counseling` varchar(20) NOT NULL,
  `follow_up` varchar(255) NOT NULL,
  `comments` longtext,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `monitoring_serviceandtreatment`
--

INSERT INTO `monitoring_serviceandtreatment` (`id`, `date`, `assessment_status`, `case_status`, `counseling`, `follow_up`, `comments`, `user_id`) VALUES
(1, '2024-03-29', 'Not Conducted', 'On Going', 'Waiting List', '', NULL, 2),
(2, '2024-03-29', 'Not Conducted', 'On Going', 'Waiting List', '', NULL, 4);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_reporting`
--

CREATE TABLE `reporting_reporting` (
  `id` bigint NOT NULL,
  `agency_code` varchar(100) DEFAULT NULL,
  `agency_name` varchar(100) DEFAULT NULL,
  `present_dzongkhag` varchar(100) DEFAULT NULL,
  `present_gewog` varchar(100) DEFAULT NULL,
  `present_village` varchar(100) DEFAULT NULL,
  `user_code` varchar(100) DEFAULT NULL,
  `parent_occupation` varchar(100) DEFAULT NULL,
  `guardian_name` varchar(100) DEFAULT NULL,
  `guardian_occupation` varchar(100) DEFAULT NULL,
  `parent_status` varchar(100) DEFAULT NULL,
  `current_living_with` varchar(100) DEFAULT NULL,
  `user_role_agency` varchar(100) DEFAULT NULL,
  `user_class` varchar(100) DEFAULT NULL,
  `user_stream` varchar(100) DEFAULT NULL,
  `user_sub_class` varchar(100) DEFAULT NULL,
  `gad_measurement` varchar(50) DEFAULT NULL,
  `phq_measurement` varchar(50) DEFAULT NULL,
  `suicidal_measurement` varchar(50) DEFAULT NULL,
  `ace_measurement` varchar(50) DEFAULT NULL,
  `overall_flag` varchar(10) DEFAULT NULL,
  `assessment_status` varchar(20) DEFAULT NULL,
  `case_status` varchar(20) DEFAULT NULL,
  `counseling` varchar(20) DEFAULT NULL,
  `follow_up` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `referral_status` varchar(20) DEFAULT NULL,
  `referral_remarks` longtext,
  `rescreening_count` int UNSIGNED NOT NULL,
  `user_id` int NOT NULL,
  `alcoholic_flag` varchar(50) DEFAULT NULL,
  `alcoholic_measurement` varchar(50) DEFAULT NULL,
  `amphetamine_flag` varchar(50) DEFAULT NULL,
  `amphetamine_measurement` varchar(50) DEFAULT NULL,
  `cannabis_flag` varchar(50) DEFAULT NULL,
  `cannabis_measurement` varchar(50) DEFAULT NULL,
  `cocaine_flag` varchar(50) DEFAULT NULL,
  `cocaine_measurement` varchar(50) DEFAULT NULL,
  `hallucinogens_flag` varchar(50) DEFAULT NULL,
  `hallucinogens_measurement` varchar(50) DEFAULT NULL,
  `inhalants_flag` varchar(50) DEFAULT NULL,
  `inhalants_measurement` varchar(50) DEFAULT NULL,
  `injection_flag` varchar(50) DEFAULT NULL,
  `injection_measurement` varchar(50) DEFAULT NULL,
  `opioids_flag` varchar(50) DEFAULT NULL,
  `opioids_measurement` varchar(50) DEFAULT NULL,
  `other_flag` varchar(50) DEFAULT NULL,
  `other_measurement` varchar(50) DEFAULT NULL,
  `other_name` varchar(100) DEFAULT NULL,
  `sedatives_flag` varchar(50) DEFAULT NULL,
  `sedatives_measurement` varchar(50) DEFAULT NULL,
  `tobacco_flag` varchar(50) DEFAULT NULL,
  `tobacco_measurement` varchar(50) DEFAULT NULL,
  `past_diagnosis` varchar(50) DEFAULT NULL
) ;

--
-- Dumping data for table `reporting_reporting`
--

INSERT INTO `reporting_reporting` (`id`, `agency_code`, `agency_name`, `present_dzongkhag`, `present_gewog`, `present_village`, `user_code`, `parent_occupation`, `guardian_name`, `guardian_occupation`, `parent_status`, `current_living_with`, `user_role_agency`, `user_class`, `user_stream`, `user_sub_class`, `gad_measurement`, `phq_measurement`, `suicidal_measurement`, `ace_measurement`, `overall_flag`, `assessment_status`, `case_status`, `counseling`, `follow_up`, `comments`, `referral_status`, `referral_remarks`, `rescreening_count`, `user_id`, `alcoholic_flag`, `alcoholic_measurement`, `amphetamine_flag`, `amphetamine_measurement`, `cannabis_flag`, `cannabis_measurement`, `cocaine_flag`, `cocaine_measurement`, `hallucinogens_flag`, `hallucinogens_measurement`, `inhalants_flag`, `inhalants_measurement`, `injection_flag`, `injection_measurement`, `opioids_flag`, `opioids_measurement`, `other_flag`, `other_measurement`, `other_name`, `sedatives_flag`, `sedatives_measurement`, `tobacco_flag`, `tobacco_measurement`, `past_diagnosis`) VALUES
(34, NULL, NULL, 'Tsirang', 'Dunglagang', 'Lhamoi Lum /Gopini', '4', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'moderate', 'moderately severe', 'more than half the days', NULL, NULL, 'Not Conducted', 'On Going', 'Waiting List', '', NULL, 'Awaiting', NULL, 0, 4, 'red', 'high risk', NULL, NULL, 'blue', 'low risk', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'yellow', 'moderate risk', ''),
(39, NULL, NULL, 'samtse', 'samtse', 'samtse', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'moderate', 'moderately severe', 'nearly everyday', NULL, NULL, 'Not Conducted', 'On Going', 'Waiting List', '', NULL, 'Awaiting', NULL, 0, 2, 'yellow', 'moderate risk', NULL, NULL, '', 'no risk', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'yellow', 'moderate risk', 'My Sickness'),
(40, NULL, NULL, 'Samtse', 'Norgaygang/Bara', 'Dugphey(Dubey)', '6', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'minimal', 'minimal', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 6, 'yellow', 'moderate risk', NULL, NULL, 'blue', 'low risk', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'yellow', 'moderate risk', '');

-- --------------------------------------------------------

--
-- Table structure for table `screening_casescreening`
--

CREATE TABLE `screening_casescreening` (
  `id` bigint NOT NULL,
  `case_name` varchar(255) NOT NULL,
  `purpose` varchar(20) NOT NULL,
  `dzongkhag` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `counselor` varchar(255) NOT NULL,
  `registration_lockout_end_time` datetime(6) DEFAULT NULL,
  `submission_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `screening_casescreening`
--

INSERT INTO `screening_casescreening` (`id`, `case_name`, `purpose`, `dzongkhag`, `date`, `counselor`, `registration_lockout_end_time`, `submission_id`, `user_id`) VALUES
(5, 'McKenzie Estes', 'Follow up', 'Chhukha', '2024-03-31', 'Rabsel Dorji', '2024-04-01 12:52:45.785694', NULL, 56),
(6, 'Angela Nash', 'Follow up', 'Bumthang', '2024-03-31', 'Rabsel Dorji', '2024-04-01 13:00:56.504611', NULL, 57),
(7, 'Maggie Foreman', 'Assessment', 'Trashigang', '2024-04-01', 'Rabsel Dorji', '2024-04-02 03:31:00.476138', NULL, 58),
(8, 'Kieran Kirby', 'Intervention', 'Gasa', '2024-04-01', 'Rabsel Dorji', '2024-04-02 03:44:50.779223', NULL, 59);

-- --------------------------------------------------------

--
-- Table structure for table `screening_eventscreening`
--

CREATE TABLE `screening_eventscreening` (
  `id` bigint NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `event_purpose` longtext,
  `location` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `duration` int NOT NULL,
  `counselor` varchar(255) NOT NULL,
  `approval_status` varchar(20) NOT NULL,
  `remarks` longtext,
  `registration_lockout_end_time` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `screening_eventscreening`
--

INSERT INTO `screening_eventscreening` (`id`, `event_name`, `event_purpose`, `location`, `start_date`, `end_date`, `duration`, `counselor`, `approval_status`, `remarks`, `registration_lockout_end_time`) VALUES
(92, 'Connor Rowe', 'Exercitation quia pr', 'Dolor aliquid ut ea', '2024-03-31', '2024-04-06', 6, 'Rabsel Dorji', 'approved', '', '2024-04-06 17:03:23.000000');

-- --------------------------------------------------------

--
-- Table structure for table `screening_screeneduser`
--

CREATE TABLE `screening_screeneduser` (
  `id` bigint NOT NULL,
  `screening_date` date NOT NULL,
  `event_screening_id` bigint NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `screening_screeneduser`
--

INSERT INTO `screening_screeneduser` (`id`, `screening_date`, `event_screening_id`, `user_id`) VALUES
(1, '2024-03-31', 92, NULL),
(2, '2024-03-31', 92, NULL),
(3, '2024-03-31', 92, NULL),
(4, '2024-03-31', 92, NULL),
(5, '2024-04-01', 92, NULL),
(6, '2024-04-01', 92, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `settings_module_appconfig`
--

CREATE TABLE `settings_module_appconfig` (
  `id` bigint NOT NULL,
  `login_logo` varchar(100) NOT NULL,
  `registration_logo` varchar(100) NOT NULL,
  `landing_page_logo` varchar(100) DEFAULT NULL,
  `landing_img_bg` varchar(100) DEFAULT NULL,
  `landing_tag_line` varchar(255) DEFAULT NULL,
  `dashboard_logo` varchar(100) NOT NULL,
  `carousel_image_1` varchar(100) DEFAULT NULL,
  `carousel_image_2` varchar(100) DEFAULT NULL,
  `carousel_image_3` varchar(100) DEFAULT NULL,
  `carousel_image_4` varchar(100) DEFAULT NULL,
  `app_name` varchar(100) NOT NULL,
  `tagline` varchar(255) NOT NULL,
  `helpline_number_1` varchar(50) NOT NULL,
  `helpline_number_2` varchar(50) NOT NULL,
  `response_service_logo` varchar(100) NOT NULL,
  `cluster_test_title` varchar(50) DEFAULT NULL,
  `cluster_test_content` longtext,
  `cluster_test_disclaimer` longtext,
  `cluster_test_icon` varchar(100) DEFAULT NULL,
  `copyright_message` varchar(255) DEFAULT NULL,
  `google_play_link` varchar(255) DEFAULT NULL,
  `apple_appstore_link` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `settings_module_appconfig`
--

INSERT INTO `settings_module_appconfig` (`id`, `login_logo`, `registration_logo`, `landing_page_logo`, `landing_img_bg`, `landing_tag_line`, `dashboard_logo`, `carousel_image_1`, `carousel_image_2`, `carousel_image_3`, `carousel_image_4`, `app_name`, `tagline`, `helpline_number_1`, `helpline_number_2`, `response_service_logo`, `cluster_test_title`, `cluster_test_content`, `cluster_test_disclaimer`, `cluster_test_icon`, `copyright_message`, `google_play_link`, `apple_appstore_link`) VALUES
(1, 'logos/pema_seal_out_bwF1Om2.png', 'logos/pema_seal_out_yeiQC9A.png', 'logos/landing_logo_2zLnDfq.png', 'logos/landing_bg_BKCPOkB.png', 'Touching People, Building Lives', 'logos/logoxs_1NBHc0P.png', 'carousel/poster1.jpg', 'carousel/poster2.jpg', 'carousel/poster3.jpg', 'carousel/poster4.jpg', 'The PEMA HWSS', 'Mental Health Matters', '1234', '5678', 'logos/logoDashbopard_DYVd4vz.png', 'Your Mental Health Matters', 'Your mental health is important for overall health and well-being. It affects how you feel, think, and behave. Good mental health allows you to cope with daily stressors and challenges and enjoy your life. Sometimes, life can get tough, and you may find yourself feeling stressed or sad. These are normal reactions, but sometimes it affects your day-to-day functioning. That is when you need professional support and it is okay to ask for help.', 'Please respond to all the questions. Your responses will help us determine the status of your mental health and safe interventions will be provided as per your need and convenience. Information will be handled with the highest level of integrity and confidentiality.', 'icons/book_1.png', 'Your Mental Health Matters', '#', '#');

-- --------------------------------------------------------

--
-- Table structure for table `settings_module_menuitem`
--

CREATE TABLE `settings_module_menuitem` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `route` varchar(100) NOT NULL,
  `icon_class` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `settings_module_menuitem`
--

INSERT INTO `settings_module_menuitem` (`id`, `name`, `route`, `icon_class`) VALUES
(1, 'Screening', '/student-dashboard/screening', 'fas fa-question-circle'),
(4, 'Screening', '/counselor-dashboard/counselor-screening', 'fa-solid fa-person-circle-question'),
(5, 'Monitor', '/counselor-dashboard/counselor-monitor', 'fa-solid fa-clipboard-list'),
(6, 'Reports', '/counselor-dashboard/counselor-reports', 'fa-solid fa-file-waveform'),
(7, 'Help', '/counselor-dashboard/counselor-help', 'fa-solid fa-circle-question'),
(8, 'Settings', '/counselor-dashboard/counselor-settings', 'fa-solid fa-gear'),
(9, 'Profile', '/student-dashboard/profile', 'fas fa-user'),
(10, 'Approval', '/admin-dashboard/admin-approval', 'fa-regular fa-thumbs-up'),
(11, 'Reports', '/admin-dashboard/admin-report', 'fa-regular fa-file-lines'),
(12, 'Help', '/admin-dashboard/admin-help', 'fa-regular fa-circle-question'),
(13, 'Settings', '/admin-dashboard/admin-settings', 'fa-solid fa-screwdriver-wrench');

-- --------------------------------------------------------

--
-- Table structure for table `settings_module_menuitem_roles`
--

CREATE TABLE `settings_module_menuitem_roles` (
  `id` bigint NOT NULL,
  `menuitem_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `settings_module_menuitem_roles`
--

INSERT INTO `settings_module_menuitem_roles` (`id`, `menuitem_id`, `group_id`) VALUES
(1, 1, 1),
(3, 4, 3),
(4, 5, 3),
(5, 6, 3),
(6, 7, 3),
(7, 8, 3),
(8, 9, 1),
(9, 10, 2),
(10, 11, 2),
(11, 12, 2),
(12, 13, 2);

-- --------------------------------------------------------

--
-- Table structure for table `settings_module_notification`
--

CREATE TABLE `settings_module_notification` (
  `id` bigint NOT NULL,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `recipient_id` int NOT NULL,
  `sender_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `settings_module_video`
--

CREATE TABLE `settings_module_video` (
  `id` bigint NOT NULL,
  `title` varchar(100) NOT NULL,
  `thumbnail` varchar(100) NOT NULL,
  `topic` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `video_link` varchar(200) NOT NULL,
  `video_file` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `settings_module_video`
--

INSERT INTO `settings_module_video` (`id`, `title`, `thumbnail`, `topic`, `description`, `video_link`, `video_file`) VALUES
(1, 'My Video', 'thumbnails/LandingPage1.png', 'Some Topic', 'some description', '', 'videos/How_Its_Made-_Fishing_Line.mp4');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `access_agency`
--
ALTER TABLE `access_agency`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `agency_code` (`agency_code`);

--
-- Indexes for table `access_customuser`
--
ALTER TABLE `access_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `identity_number` (`identity_number`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `access_customuser_active_agency_id_7ab9e26f_fk_access_agency_id` (`active_agency_id`);

--
-- Indexes for table `access_customuser_groups`
--
ALTER TABLE `access_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `access_customuser_groups_customuser_id_group_id_6bc54d74_uniq` (`customuser_id`,`group_id`),
  ADD KEY `access_customuser_groups_group_id_a0855f68_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `access_customuser_user_permissions`
--
ALTER TABLE `access_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `access_customuser_user_p_customuser_id_permission_c6f1c9ef_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `access_customuser_us_permission_id_2f58c254_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `access_prerecordeduser`
--
ALTER TABLE `access_prerecordeduser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `identity_number` (`identity_number`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `access_useragency`
--
ALTER TABLE `access_useragency`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `access_useragency_agency_id_5dfef3d4_fk_access_agency_id` (`agency_id`);

--
-- Indexes for table `admin_interface_theme`
--
ALTER TABLE `admin_interface_theme`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `admin_interface_theme_name_30bda70f_uniq` (`name`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_access_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `measurement_activeuser`
--
ALTER TABLE `measurement_activeuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `measurement_activeus_user_submission_id_a5cc855b_fk_measureme` (`user_submission_id`);

--
-- Indexes for table `measurement_activeuser_substances_used`
--
ALTER TABLE `measurement_activeuser_substances_used`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `measurement_activeuser_s_activeuser_id_measuremen_62e68a48_uniq` (`activeuser_id`,`measurementsubstance_id`),
  ADD KEY `measurement_activeus_measurementsubstance_c9997986_fk_measureme` (`measurementsubstance_id`);

--
-- Indexes for table `measurement_lifetimeuser`
--
ALTER TABLE `measurement_lifetimeuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `measurement_lifetime_user_submission_id_1e23fcc6_fk_measureme` (`user_submission_id`);

--
-- Indexes for table `measurement_lifetimeuser_substances_used`
--
ALTER TABLE `measurement_lifetimeuser_substances_used`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `measurement_lifetimeuser_lifetimeuser_id_measurem_3e2444e6_uniq` (`lifetimeuser_id`,`measurementsubstance_id`),
  ADD KEY `measurement_lifetime_measurementsubstance_cefe8119_fk_measureme` (`measurementsubstance_id`);

--
-- Indexes for table `measurement_measurement`
--
ALTER TABLE `measurement_measurement`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `assist_id` (`assist_id`),
  ADD KEY `measurement_measurem_user_submission_id_a1646c07_fk_measureme` (`user_submission_id`);

--
-- Indexes for table `measurement_measurementassist`
--
ALTER TABLE `measurement_measurementassist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `measurement_measurem_user_submission_id_ecb75274_fk_measureme` (`user_submission_id`);

--
-- Indexes for table `measurement_measurementsubstance`
--
ALTER TABLE `measurement_measurementsubstance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `measurement_questionset`
--
ALTER TABLE `measurement_questionset`
  ADD PRIMARY KEY (`id`),
  ADD KEY `measurement_question_user_submission_id_17622e3f_fk_measureme` (`user_submission_id`),
  ADD KEY `measurement_question_test_type_id_bcea9246_fk_measureme` (`test_type_id`);

--
-- Indexes for table `measurement_submission`
--
ALTER TABLE `measurement_submission`
  ADD PRIMARY KEY (`id`),
  ADD KEY `measurement_submissi_question_set_id_4084877e_fk_measureme` (`question_set_id`),
  ADD KEY `measurement_submissi_user_submission_id_7dde365b_fk_measureme` (`user_submission_id`);

--
-- Indexes for table `measurement_testtype`
--
ALTER TABLE `measurement_testtype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `measurement_usersubmission`
--
ALTER TABLE `measurement_usersubmission`
  ADD PRIMARY KEY (`id`),
  ADD KEY `measurement_usersubm_test_type_id_94dcf569_fk_measureme` (`test_type_id`),
  ADD KEY `measurement_usersubm_user_id_b0a3069e_fk_access_cu` (`user_id`);

--
-- Indexes for table `monitoring_referral`
--
ALTER TABLE `monitoring_referral`
  ADD PRIMARY KEY (`id`),
  ADD KEY `monitoring_referral_referred_by_id_5376166f_fk_access_cu` (`referred_by_id`),
  ADD KEY `monitoring_referral_user_id_e8015836_fk_access_customuser_id` (`user_id`),
  ADD KEY `monitoring_referral_referred_to_id_8133c710_fk_access_cu` (`referred_to_id`),
  ADD KEY `monitoring_referral_service_and_treatmen_d4aa1b4d_fk_monitorin` (`service_and_treatment_id`);

--
-- Indexes for table `monitoring_rescreening`
--
ALTER TABLE `monitoring_rescreening`
  ADD PRIMARY KEY (`id`),
  ADD KEY `monitoring_rescreening_user_id_851b5469_fk_access_customuser_id` (`user_id`),
  ADD KEY `monitoring_rescreeni_service_and_treatmen_7959f9a8_fk_monitorin` (`service_and_treatment_id`);

--
-- Indexes for table `monitoring_serviceandtreatment`
--
ALTER TABLE `monitoring_serviceandtreatment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `monitoring_servicean_user_id_28344ea9_fk_access_cu` (`user_id`);

--
-- Indexes for table `reporting_reporting`
--
ALTER TABLE `reporting_reporting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reporting_reporting_user_id_d4c4311b_fk_access_customuser_id` (`user_id`);

--
-- Indexes for table `screening_casescreening`
--
ALTER TABLE `screening_casescreening`
  ADD PRIMARY KEY (`id`),
  ADD KEY `screening_casescreen_submission_id_68c03606_fk_measureme` (`submission_id`),
  ADD KEY `screening_casescreening_user_id_112c4aa4_fk_access_customuser_id` (`user_id`);

--
-- Indexes for table `screening_eventscreening`
--
ALTER TABLE `screening_eventscreening`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `screening_screeneduser`
--
ALTER TABLE `screening_screeneduser`
  ADD PRIMARY KEY (`id`),
  ADD KEY `screening_screenedus_event_screening_id_c6456750_fk_screening` (`event_screening_id`),
  ADD KEY `screening_screeneduser_user_id_9303156e_fk_access_customuser_id` (`user_id`);

--
-- Indexes for table `settings_module_appconfig`
--
ALTER TABLE `settings_module_appconfig`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `settings_module_menuitem`
--
ALTER TABLE `settings_module_menuitem`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `settings_module_menuitem_roles`
--
ALTER TABLE `settings_module_menuitem_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `settings_module_menuitem_menuitem_id_group_id_983decd8_uniq` (`menuitem_id`,`group_id`),
  ADD KEY `settings_module_menu_group_id_f1cf0871_fk_auth_grou` (`group_id`);

--
-- Indexes for table `settings_module_notification`
--
ALTER TABLE `settings_module_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `settings_module_noti_recipient_id_e54dc951_fk_access_cu` (`recipient_id`),
  ADD KEY `settings_module_noti_sender_id_d7bb0cbd_fk_access_cu` (`sender_id`);

--
-- Indexes for table `settings_module_video`
--
ALTER TABLE `settings_module_video`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `access_agency`
--
ALTER TABLE `access_agency`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `access_customuser`
--
ALTER TABLE `access_customuser`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT for table `access_customuser_groups`
--
ALTER TABLE `access_customuser_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `access_customuser_user_permissions`
--
ALTER TABLE `access_customuser_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `access_prerecordeduser`
--
ALTER TABLE `access_prerecordeduser`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `access_useragency`
--
ALTER TABLE `access_useragency`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `admin_interface_theme`
--
ALTER TABLE `admin_interface_theme`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `measurement_activeuser`
--
ALTER TABLE `measurement_activeuser`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `measurement_activeuser_substances_used`
--
ALTER TABLE `measurement_activeuser_substances_used`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `measurement_lifetimeuser`
--
ALTER TABLE `measurement_lifetimeuser`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `measurement_lifetimeuser_substances_used`
--
ALTER TABLE `measurement_lifetimeuser_substances_used`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1543;

--
-- AUTO_INCREMENT for table `measurement_measurement`
--
ALTER TABLE `measurement_measurement`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `measurement_measurementassist`
--
ALTER TABLE `measurement_measurementassist`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `measurement_measurementsubstance`
--
ALTER TABLE `measurement_measurementsubstance`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `measurement_questionset`
--
ALTER TABLE `measurement_questionset`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `measurement_submission`
--
ALTER TABLE `measurement_submission`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=230;

--
-- AUTO_INCREMENT for table `measurement_testtype`
--
ALTER TABLE `measurement_testtype`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `measurement_usersubmission`
--
ALTER TABLE `measurement_usersubmission`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `monitoring_referral`
--
ALTER TABLE `monitoring_referral`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `monitoring_rescreening`
--
ALTER TABLE `monitoring_rescreening`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `monitoring_serviceandtreatment`
--
ALTER TABLE `monitoring_serviceandtreatment`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `reporting_reporting`
--
ALTER TABLE `reporting_reporting`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `screening_casescreening`
--
ALTER TABLE `screening_casescreening`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `screening_eventscreening`
--
ALTER TABLE `screening_eventscreening`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `screening_screeneduser`
--
ALTER TABLE `screening_screeneduser`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `settings_module_appconfig`
--
ALTER TABLE `settings_module_appconfig`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `settings_module_menuitem`
--
ALTER TABLE `settings_module_menuitem`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `settings_module_menuitem_roles`
--
ALTER TABLE `settings_module_menuitem_roles`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `settings_module_notification`
--
ALTER TABLE `settings_module_notification`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `settings_module_video`
--
ALTER TABLE `settings_module_video`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `access_customuser`
--
ALTER TABLE `access_customuser`
  ADD CONSTRAINT `access_customuser_active_agency_id_7ab9e26f_fk_access_agency_id` FOREIGN KEY (`active_agency_id`) REFERENCES `access_agency` (`id`);

--
-- Constraints for table `access_customuser_groups`
--
ALTER TABLE `access_customuser_groups`
  ADD CONSTRAINT `access_customuser_gr_customuser_id_f51a174b_fk_access_cu` FOREIGN KEY (`customuser_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `access_customuser_groups_group_id_a0855f68_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `access_customuser_user_permissions`
--
ALTER TABLE `access_customuser_user_permissions`
  ADD CONSTRAINT `access_customuser_us_customuser_id_7a2ca22b_fk_access_cu` FOREIGN KEY (`customuser_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `access_customuser_us_permission_id_2f58c254_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `access_useragency`
--
ALTER TABLE `access_useragency`
  ADD CONSTRAINT `access_useragency_agency_id_5dfef3d4_fk_access_agency_id` FOREIGN KEY (`agency_id`) REFERENCES `access_agency` (`id`),
  ADD CONSTRAINT `access_useragency_user_id_43932f93_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `measurement_activeuser`
--
ALTER TABLE `measurement_activeuser`
  ADD CONSTRAINT `measurement_activeus_user_submission_id_a5cc855b_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`),
  ADD CONSTRAINT `measurement_activeuser_user_id_a09b6d52_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `measurement_activeuser_substances_used`
--
ALTER TABLE `measurement_activeuser_substances_used`
  ADD CONSTRAINT `measurement_activeus_activeuser_id_af5fea96_fk_measureme` FOREIGN KEY (`activeuser_id`) REFERENCES `measurement_activeuser` (`id`),
  ADD CONSTRAINT `measurement_activeus_measurementsubstance_c9997986_fk_measureme` FOREIGN KEY (`measurementsubstance_id`) REFERENCES `measurement_measurementsubstance` (`id`);

--
-- Constraints for table `measurement_lifetimeuser`
--
ALTER TABLE `measurement_lifetimeuser`
  ADD CONSTRAINT `measurement_lifetime_user_id_17770d3a_fk_access_cu` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `measurement_lifetime_user_submission_id_1e23fcc6_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`);

--
-- Constraints for table `measurement_lifetimeuser_substances_used`
--
ALTER TABLE `measurement_lifetimeuser_substances_used`
  ADD CONSTRAINT `measurement_lifetime_lifetimeuser_id_e53ef858_fk_measureme` FOREIGN KEY (`lifetimeuser_id`) REFERENCES `measurement_lifetimeuser` (`id`),
  ADD CONSTRAINT `measurement_lifetime_measurementsubstance_cefe8119_fk_measureme` FOREIGN KEY (`measurementsubstance_id`) REFERENCES `measurement_measurementsubstance` (`id`);

--
-- Constraints for table `measurement_measurement`
--
ALTER TABLE `measurement_measurement`
  ADD CONSTRAINT `measurement_measurem_assist_id_85e9c793_fk_measureme` FOREIGN KEY (`assist_id`) REFERENCES `measurement_measurementassist` (`id`),
  ADD CONSTRAINT `measurement_measurem_user_submission_id_a1646c07_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`),
  ADD CONSTRAINT `measurement_measurement_user_id_df2a9b1d_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `measurement_measurementassist`
--
ALTER TABLE `measurement_measurementassist`
  ADD CONSTRAINT `measurement_measurem_user_id_fc444b52_fk_access_cu` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `measurement_measurem_user_submission_id_ecb75274_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`);

--
-- Constraints for table `measurement_questionset`
--
ALTER TABLE `measurement_questionset`
  ADD CONSTRAINT `measurement_question_test_type_id_bcea9246_fk_measureme` FOREIGN KEY (`test_type_id`) REFERENCES `measurement_testtype` (`id`),
  ADD CONSTRAINT `measurement_question_user_submission_id_17622e3f_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`);

--
-- Constraints for table `measurement_submission`
--
ALTER TABLE `measurement_submission`
  ADD CONSTRAINT `measurement_submissi_question_set_id_4084877e_fk_measureme` FOREIGN KEY (`question_set_id`) REFERENCES `measurement_questionset` (`id`),
  ADD CONSTRAINT `measurement_submissi_user_submission_id_7dde365b_fk_measureme` FOREIGN KEY (`user_submission_id`) REFERENCES `measurement_usersubmission` (`id`);

--
-- Constraints for table `measurement_usersubmission`
--
ALTER TABLE `measurement_usersubmission`
  ADD CONSTRAINT `measurement_usersubm_test_type_id_94dcf569_fk_measureme` FOREIGN KEY (`test_type_id`) REFERENCES `measurement_testtype` (`id`),
  ADD CONSTRAINT `measurement_usersubm_user_id_b0a3069e_fk_access_cu` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `monitoring_referral`
--
ALTER TABLE `monitoring_referral`
  ADD CONSTRAINT `monitoring_referral_referred_by_id_5376166f_fk_access_cu` FOREIGN KEY (`referred_by_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `monitoring_referral_referred_to_id_8133c710_fk_access_cu` FOREIGN KEY (`referred_to_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `monitoring_referral_user_id_e8015836_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `monitoring_rescreening`
--
ALTER TABLE `monitoring_rescreening`
  ADD CONSTRAINT `monitoring_rescreeni_service_and_treatmen_7959f9a8_fk_monitorin` FOREIGN KEY (`service_and_treatment_id`) REFERENCES `monitoring_serviceandtreatment` (`id`),
  ADD CONSTRAINT `monitoring_rescreening_user_id_851b5469_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `monitoring_serviceandtreatment`
--
ALTER TABLE `monitoring_serviceandtreatment`
  ADD CONSTRAINT `monitoring_servicean_user_id_28344ea9_fk_access_cu` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `reporting_reporting`
--
ALTER TABLE `reporting_reporting`
  ADD CONSTRAINT `reporting_reporting_user_id_d4c4311b_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `screening_casescreening`
--
ALTER TABLE `screening_casescreening`
  ADD CONSTRAINT `screening_casescreen_submission_id_68c03606_fk_measureme` FOREIGN KEY (`submission_id`) REFERENCES `measurement_usersubmission` (`id`),
  ADD CONSTRAINT `screening_casescreening_user_id_112c4aa4_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `screening_screeneduser`
--
ALTER TABLE `screening_screeneduser`
  ADD CONSTRAINT `screening_screenedus_event_screening_id_c6456750_fk_screening` FOREIGN KEY (`event_screening_id`) REFERENCES `screening_eventscreening` (`id`),
  ADD CONSTRAINT `screening_screeneduser_user_id_9303156e_fk_access_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `access_customuser` (`id`);

--
-- Constraints for table `settings_module_menuitem_roles`
--
ALTER TABLE `settings_module_menuitem_roles`
  ADD CONSTRAINT `settings_module_menu_group_id_f1cf0871_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `settings_module_menu_menuitem_id_5018c0c6_fk_settings_` FOREIGN KEY (`menuitem_id`) REFERENCES `settings_module_menuitem` (`id`);

--
-- Constraints for table `settings_module_notification`
--
ALTER TABLE `settings_module_notification`
  ADD CONSTRAINT `settings_module_noti_recipient_id_e54dc951_fk_access_cu` FOREIGN KEY (`recipient_id`) REFERENCES `access_customuser` (`id`),
  ADD CONSTRAINT `settings_module_noti_sender_id_d7bb0cbd_fk_access_cu` FOREIGN KEY (`sender_id`) REFERENCES `access_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
