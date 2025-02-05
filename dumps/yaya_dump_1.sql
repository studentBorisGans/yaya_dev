-- MySQL dump 10.13  Distrib 9.0.1, for macos14.4 (arm64)
--
-- Host: localhost    Database: yaya_dev
-- ------------------------------------------------------
-- Server version	8.4.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dj`
--

DROP TABLE IF EXISTS `dj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dj` (
  `dj_id` int NOT NULL AUTO_INCREMENT,
  `dj_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `bio` text,
  `location` varchar(100) DEFAULT NULL,
  `interested_count` int DEFAULT '0',
  `socials` tinyint(1) DEFAULT '0',
  `notifications` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`dj_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dj`
--

LOCK TABLES `dj` WRITE;
/*!40000 ALTER TABLE `dj` DISABLE KEYS */;
/*!40000 ALTER TABLE `dj` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dj_org_chats`
--

DROP TABLE IF EXISTS `dj_org_chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dj_org_chats` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `organizer_id` int NOT NULL,
  `dj_id` int NOT NULL,
  `datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`chat_id`),
  KEY `organizer_id` (`organizer_id`),
  KEY `dj_id` (`dj_id`),
  CONSTRAINT `dj_org_chats_ibfk_1` FOREIGN KEY (`organizer_id`) REFERENCES `organizer` (`organizer_id`) ON DELETE RESTRICT,
  CONSTRAINT `dj_org_chats_ibfk_2` FOREIGN KEY (`dj_id`) REFERENCES `dj` (`dj_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dj_org_chats`
--

LOCK TABLES `dj_org_chats` WRITE;
/*!40000 ALTER TABLE `dj_org_chats` DISABLE KEYS */;
/*!40000 ALTER TABLE `dj_org_chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dj_org_messages`
--

DROP TABLE IF EXISTS `dj_org_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dj_org_messages` (
  `msg_id` int NOT NULL AUTO_INCREMENT,
  `chat_id` int NOT NULL,
  `event_id` int NOT NULL,
  `sender` enum('dj','organizer') NOT NULL,
  `datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `message` text NOT NULL,
  `status` enum('sent','delivered','read') NOT NULL DEFAULT 'sent',
  PRIMARY KEY (`msg_id`),
  KEY `chat_id` (`chat_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `dj_org_messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `dj_org_chats` (`chat_id`) ON DELETE CASCADE,
  CONSTRAINT `dj_org_messages_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dj_org_messages`
--

LOCK TABLES `dj_org_messages` WRITE;
/*!40000 ALTER TABLE `dj_org_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `dj_org_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dj_socials`
--

DROP TABLE IF EXISTS `dj_socials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dj_socials` (
  `dj_id` int NOT NULL,
  `website` varchar(2083) DEFAULT NULL,
  `soundcloud` varchar(2083) DEFAULT NULL,
  `spotify` varchar(2083) DEFAULT NULL,
  `facebook` varchar(2083) DEFAULT NULL,
  `instagram` varchar(2083) DEFAULT NULL,
  `snapchat` varchar(2083) DEFAULT NULL,
  `x` varchar(2083) DEFAULT NULL,
  KEY `dj_id` (`dj_id`),
  CONSTRAINT `dj_socials_ibfk_1` FOREIGN KEY (`dj_id`) REFERENCES `dj` (`dj_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dj_socials`
--

LOCK TABLES `dj_socials` WRITE;
/*!40000 ALTER TABLE `dj_socials` DISABLE KEYS */;
/*!40000 ALTER TABLE `dj_socials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dj_tags`
--

DROP TABLE IF EXISTS `dj_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dj_tags` (
  `tag_id` int NOT NULL,
  `dj_id` int NOT NULL,
  PRIMARY KEY (`tag_id`,`dj_id`),
  KEY `dj_id` (`dj_id`),
  CONSTRAINT `dj_tags_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON DELETE RESTRICT,
  CONSTRAINT `dj_tags_ibfk_2` FOREIGN KEY (`dj_id`) REFERENCES `dj` (`dj_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dj_tags`
--

LOCK TABLES `dj_tags` WRITE;
/*!40000 ALTER TABLE `dj_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `dj_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_attendance`
--

DROP TABLE IF EXISTS `event_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_attendance` (
  `event_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`event_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `event_attendance_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE CASCADE,
  CONSTRAINT `event_attendance_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_attendance`
--

LOCK TABLES `event_attendance` WRITE;
/*!40000 ALTER TABLE `event_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_data`
--

DROP TABLE IF EXISTS `event_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_data` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `organizer_id` int NOT NULL,
  `venue_id` int NOT NULL,
  `published` tinyint(1) DEFAULT '0',
  `tagged` tinyint(1) DEFAULT '0',
  `event_name` varchar(255) NOT NULL,
  `date` datetime NOT NULL,
  `budget` float DEFAULT NULL,
  `pre_event_poster` varchar(2083) DEFAULT NULL,
  `pre_bio` text,
  PRIMARY KEY (`event_id`),
  KEY `organizer_id` (`organizer_id`),
  KEY `venue_id` (`venue_id`),
  CONSTRAINT `event_data_ibfk_1` FOREIGN KEY (`organizer_id`) REFERENCES `organizer` (`organizer_id`) ON DELETE RESTRICT,
  CONSTRAINT `event_data_ibfk_2` FOREIGN KEY (`venue_id`) REFERENCES `venues` (`venue_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_data`
--

LOCK TABLES `event_data` WRITE;
/*!40000 ALTER TABLE `event_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_tags`
--

DROP TABLE IF EXISTS `event_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_tags` (
  `tag_id` int NOT NULL,
  `event_id` int NOT NULL,
  PRIMARY KEY (`tag_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `event_tags_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON DELETE RESTRICT,
  CONSTRAINT `event_tags_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_tags`
--

LOCK TABLES `event_tags` WRITE;
/*!40000 ALTER TABLE `event_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_tickets`
--

DROP TABLE IF EXISTS `event_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_tickets` (
  `event_id` int NOT NULL,
  `class_id` int NOT NULL,
  `sold_out` tinyint(1) DEFAULT '0',
  KEY `event_id` (`event_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `event_tickets_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE CASCADE,
  CONSTRAINT `event_tickets_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `ticket_classes` (`class_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_tickets`
--

LOCK TABLES `event_tickets` WRITE;
/*!40000 ALTER TABLE `event_tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friendships`
--

DROP TABLE IF EXISTS `friendships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friendships` (
  `friendship_id` int NOT NULL AUTO_INCREMENT,
  `user_a_id` int NOT NULL,
  `user_b_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`friendship_id`),
  UNIQUE KEY `user_a_id` (`user_a_id`,`user_b_id`),
  KEY `user_b_id` (`user_b_id`),
  CONSTRAINT `friendships_ibfk_1` FOREIGN KEY (`user_a_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `friendships_ibfk_2` FOREIGN KEY (`user_b_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friendships`
--

LOCK TABLES `friendships` WRITE;
/*!40000 ALTER TABLE `friendships` DISABLE KEYS */;
/*!40000 ALTER TABLE `friendships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_service`
--

DROP TABLE IF EXISTS `music_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_service` (
  `user_id` int NOT NULL,
  `apple` tinyint(1) DEFAULT '0',
  `spotify` tinyint(1) DEFAULT '0',
  `sc` tinyint(1) DEFAULT '0',
  `access_token` varchar(255) DEFAULT NULL,
  `refresh_token` varchar(255) DEFAULT NULL,
  `expiration` datetime DEFAULT NULL,
  KEY `user_id` (`user_id`),
  CONSTRAINT `music_service_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_service`
--

LOCK TABLES `music_service` WRITE;
/*!40000 ALTER TABLE `music_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `music_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizer`
--

DROP TABLE IF EXISTS `organizer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizer` (
  `organizer_id` int NOT NULL AUTO_INCREMENT,
  `org_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `notifications` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`organizer_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizer`
--

LOCK TABLES `organizer` WRITE;
/*!40000 ALTER TABLE `organizer` DISABLE KEYS */;
INSERT INTO `organizer` VALUES (1,'elrow','Michael','Bowman','matthew21@example.org','001-296-744-6807x120','Belarus','https://white.com/',1),(2,'LWE','Amy','Davis','david55@example.org','001-231-716-7151x937','Belgium','https://durham.net/',1),(3,'Alternative Projects','Monique','Ali','kevin92@example.org','515.382.0035','Cote d\'Ivoire','http://www.stevens.com/',0),(4,'Azulu','Matthew','Taylor','christopherschmidt@example.com','367.227.0052','Cape Verde','http://www.hughes.info/',1);
/*!40000 ALTER TABLE `organizer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `published_events`
--

DROP TABLE IF EXISTS `published_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `published_events` (
  `event_id` int NOT NULL,
  `dj_id` int NOT NULL,
  `completed` tinyint(1) DEFAULT '0',
  `sold_out` tinyint(1) DEFAULT '0',
  `event_poster` varchar(2083) NOT NULL,
  `bio` text NOT NULL,
  KEY `event_id` (`event_id`),
  KEY `dj_id` (`dj_id`),
  CONSTRAINT `published_events_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE RESTRICT,
  CONSTRAINT `published_events_ibfk_2` FOREIGN KEY (`dj_id`) REFERENCES `dj` (`dj_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `published_events`
--

LOCK TABLES `published_events` WRITE;
/*!40000 ALTER TABLE `published_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `published_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_details`
--

DROP TABLE IF EXISTS `purchase_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_details` (
  `purchase_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `event_id` int NOT NULL,
  `num_tickets` int NOT NULL,
  `price` float NOT NULL,
  `table_booking` tinyint(1) DEFAULT '0',
  `shared` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`purchase_id`),
  KEY `user_id` (`user_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `purchase_details_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `purchase_details_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_details`
--

LOCK TABLES `purchase_details` WRITE;
/*!40000 ALTER TABLE `purchase_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchased_tickets`
--

DROP TABLE IF EXISTS `purchased_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchased_tickets` (
  `purchase_id` int NOT NULL,
  `class_id` int NOT NULL,
  `num_tickets` int NOT NULL,
  PRIMARY KEY (`purchase_id`,`class_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `purchased_tickets_ibfk_1` FOREIGN KEY (`purchase_id`) REFERENCES `purchase_details` (`purchase_id`) ON DELETE CASCADE,
  CONSTRAINT `purchased_tickets_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `ticket_classes` (`class_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchased_tickets`
--

LOCK TABLES `purchased_tickets` WRITE;
/*!40000 ALTER TABLE `purchased_tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchased_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shared_ticket`
--

DROP TABLE IF EXISTS `shared_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shared_ticket` (
  `share_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `resolved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`share_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shared_ticket`
--

LOCK TABLES `shared_ticket` WRITE;
/*!40000 ALTER TABLE `shared_ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `shared_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `tag_id` int NOT NULL AUTO_INCREMENT,
  `tag_type` varchar(50) DEFAULT NULL,
  `tag_value` varchar(100) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_classes`
--

DROP TABLE IF EXISTS `ticket_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_classes` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(50) DEFAULT NULL,
  `num_left` int DEFAULT '0',
  `price` float NOT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_classes`
--

LOCK TABLES `ticket_classes` WRITE;
/*!40000 ALTER TABLE `ticket_classes` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_sharing`
--

DROP TABLE IF EXISTS `ticket_sharing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_sharing` (
  `purchase_id` int NOT NULL,
  `share_id` int NOT NULL,
  PRIMARY KEY (`purchase_id`,`share_id`),
  KEY `share_id` (`share_id`),
  CONSTRAINT `ticket_sharing_ibfk_1` FOREIGN KEY (`purchase_id`) REFERENCES `purchase_details` (`purchase_id`) ON DELETE CASCADE,
  CONSTRAINT `ticket_sharing_ibfk_2` FOREIGN KEY (`share_id`) REFERENCES `shared_ticket` (`share_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_sharing`
--

LOCK TABLES `ticket_sharing` WRITE;
/*!40000 ALTER TABLE `ticket_sharing` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket_sharing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_chats`
--

DROP TABLE IF EXISTS `user_chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_chats` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `friendship_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`chat_id`),
  KEY `friendship_id` (`friendship_id`),
  CONSTRAINT `user_chats_ibfk_1` FOREIGN KEY (`friendship_id`) REFERENCES `friendships` (`friendship_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_chats`
--

LOCK TABLES `user_chats` WRITE;
/*!40000 ALTER TABLE `user_chats` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_data`
--

DROP TABLE IF EXISTS `user_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_data` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `age` tinyint DEFAULT NULL,
  `spend_class` enum('A','B','C','D','E') DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `notifications` tinyint(1) DEFAULT '0',
  `music_service` tinyint(1) DEFAULT '0',
  `established` tinyint(1) DEFAULT '0',
  `pw` varchar(255) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=916 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_data`
--

LOCK TABLES `user_data` WRITE;
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` VALUES (3,'root','dev','dev@test.com','Madrid','Dutch','Male',0,'A','2025-02-05 17:03:07',0,0,0,'pw','test'),(816,'emilyCHAMBERS647','Emily','emilyCHAMBERS647@hotmail.com','Comoros','Spanish','Female',18,'E','2025-02-05 17:35:19',1,1,1,'default','Chambers'),(817,'daveSANDOVAL407','Dave','daveSANDOVAL407@yahoo.com','Gambia','Spanish','Female',28,'E','2025-02-05 17:35:19',1,1,1,'default','Sandoval'),(818,'christianROBINSON208','Christian','christianROBINSON208@hotmail.com','Saint Helena','Spanish','Male',20,'E','2025-02-05 17:35:19',0,1,1,'default','Robinson'),(819,'christinaHOWARD276','Christina','christinaHOWARD276@yahoo.com','Jordan','Dutch','Female',20,'B','2025-02-05 17:35:19',1,0,1,'default','Howard'),(820,'dannyJOHNSON987','Danny','dannyJOHNSON987@hotmail.com','Niger','Dutch','Other',18,'E','2025-02-05 17:35:19',0,1,1,'default','Johnson'),(821,'julieROBINSON563','Julie','julieROBINSON563@hotmail.com','Jersey','English','Male',24,'D','2025-02-05 17:35:19',0,0,1,'default','Robinson'),(822,'patriciaCOHEN103','Patricia','patriciaCOHEN103@hotmail.com','Argentina','Spanish','Other',28,'C','2025-02-05 17:35:19',0,0,1,'default','Cohen'),(823,'danielBROWN190','Daniel','danielBROWN190@yahoo.com','Ethiopia','English','Male',18,'D','2025-02-05 17:35:19',1,0,0,'default','Brown'),(824,'kariLEACH662','Kari','kariLEACH662@gmail.com','Eritrea','Spanish','Other',18,'E','2025-02-05 17:35:19',0,1,0,'default','Leach'),(825,'adrienneANDERSON90','Adrienne','adrienneANDERSON90@gmail.com','Chad','Dutch','Female',20,'E','2025-02-05 17:35:19',0,1,1,'default','Anderson'),(826,'carolBRANDT611','Carol','carolBRANDT611@hotmail.com','Bouvet Island (Bouvetoya)','Spanish','Other',25,'E','2025-02-05 17:35:19',0,1,1,'default','Brandt'),(827,'jessicaNELSON414','Jessica','jessicaNELSON414@gmail.com','Equatorial Guinea','Spanish','Female',25,'C','2025-02-05 17:35:19',0,1,0,'default','Nelson'),(828,'kimberlyKANE314','Kimberly','kimberlyKANE314@gmail.com','Tuvalu','English','Male',30,'E','2025-02-05 17:35:19',0,0,1,'default','Kane'),(829,'dannyHAMILTON71','Danny','dannyHAMILTON71@hotmail.com','Tokelau','Dutch','Other',24,'C','2025-02-05 17:35:19',0,1,1,'default','Hamilton'),(830,'andrewWU905','Andrew','andrewWU905@gmail.com','Cuba','English','Male',19,'A','2025-02-05 17:35:19',1,1,1,'default','Wu'),(831,'henryPADILLA871','Henry','henryPADILLA871@yahoo.com','Dominica','Dutch','Other',29,'D','2025-02-05 17:35:19',0,0,1,'default','Padilla'),(832,'matthewHILL649','Matthew','matthewHILL649@hotmail.com','Mayotte','English','Other',18,'B','2025-02-05 17:35:19',1,1,1,'default','Hill'),(833,'joannePACE954','Joanne','joannePACE954@hotmail.com','Venezuela','Dutch','Other',25,'E','2025-02-05 17:35:19',1,1,1,'default','Pace'),(834,'joshuaCOSTA612','Joshua','joshuaCOSTA612@yahoo.com','Serbia','Spanish','Other',30,'E','2025-02-05 17:35:19',1,1,0,'default','Costa'),(835,'alexanderJONES443','Alexander','alexanderJONES443@gmail.com','Congo','English','Other',19,'B','2025-02-05 17:35:19',1,1,1,'default','Jones'),(836,'pamelaBROWN290','Pamela','pamelaBROWN290@yahoo.com','Hungary','Dutch','Female',24,'E','2025-02-05 17:35:19',1,0,0,'default','Brown'),(837,'danielSMITH841','Daniel','danielSMITH841@gmail.com','Belgium','Dutch','Male',25,'C','2025-02-05 17:35:19',0,0,0,'default','Smith'),(838,'jessicaHILL95','Jessica','jessicaHILL95@hotmail.com','Kazakhstan','Spanish','Other',19,'D','2025-02-05 17:35:19',0,1,1,'default','Hill'),(839,'kevinRUSSELL305','Kevin','kevinRUSSELL305@hotmail.com','Nauru','English','Male',18,'E','2025-02-05 17:35:19',1,1,0,'default','Russell'),(840,'joanneJAMES864','Joanne','joanneJAMES864@yahoo.com','Turkmenistan','Dutch','Other',30,'B','2025-02-05 17:35:19',1,1,1,'default','James'),(841,'mariaSANCHEZ583','Maria','mariaSANCHEZ583@gmail.com','Barbados','Spanish','Male',24,'C','2025-02-05 17:35:19',1,0,0,'default','Sanchez'),(842,'edwardHO277','Edward','edwardHO277@gmail.com','Mexico','English','Female',19,'B','2025-02-05 17:35:19',1,0,0,'default','Ho'),(843,'erinWALKER442','Erin','erinWALKER442@hotmail.com','American Samoa','English','Other',24,'D','2025-02-05 17:35:19',0,0,1,'default','Walker'),(844,'monicaGILBERT962','Monica','monicaGILBERT962@gmail.com','Kyrgyz Republic','English','Female',22,'E','2025-02-05 17:35:19',1,1,0,'default','Gilbert'),(845,'margaretGILL895','Margaret','margaretGILL895@hotmail.com','Chad','English','Other',18,'A','2025-02-05 17:35:19',0,0,1,'default','Gill'),(846,'jessicaBOYD686','Jessica','jessicaBOYD686@gmail.com','Christmas Island','Dutch','Female',18,'E','2025-02-05 17:35:19',1,0,1,'default','Boyd'),(847,'jeffreyMURRAY716','Jeffrey','jeffreyMURRAY716@yahoo.com','Kenya','English','Female',22,'E','2025-02-05 17:35:19',0,0,0,'default','Murray'),(848,'adamROBERTS392','Adam','adamROBERTS392@yahoo.com','Tonga','Spanish','Female',26,'E','2025-02-05 17:35:19',0,0,1,'default','Roberts'),(849,'melanieMARTINEZ260','Melanie','melanieMARTINEZ260@gmail.com','Canada','English','Male',19,'E','2025-02-05 17:35:19',0,0,0,'default','Martinez'),(850,'justinLYNN166','Justin','justinLYNN166@gmail.com','Germany','Dutch','Female',24,'E','2025-02-05 17:35:19',1,0,0,'default','Lynn'),(851,'melissaSCOTT334','Melissa','melissaSCOTT334@gmail.com','Iceland','English','Male',23,'E','2025-02-05 17:35:19',1,1,0,'default','Scott'),(852,'michaelKIDD793','Michael','michaelKIDD793@yahoo.com','American Samoa','Dutch','Male',18,'D','2025-02-05 17:35:19',0,0,0,'default','Kidd'),(853,'kendraCOX516','Kendra','kendraCOX516@yahoo.com','Armenia','Spanish','Male',25,'E','2025-02-05 17:35:19',0,1,0,'default','Cox'),(854,'williamBRADSHAW52','William','williamBRADSHAW52@gmail.com','Mongolia','Spanish','Female',18,'C','2025-02-05 17:35:19',1,0,1,'default','Bradshaw'),(855,'brendanAGUILAR710','Brendan','brendanAGUILAR710@yahoo.com','Spain','English','Female',26,'E','2025-02-05 17:35:19',1,1,1,'default','Aguilar'),(856,'margaretRYAN407','Margaret','margaretRYAN407@hotmail.com','Myanmar','Dutch','Other',18,'E','2025-02-05 17:35:19',1,1,1,'default','Ryan'),(857,'teresaGALLOWAY545','Teresa','teresaGALLOWAY545@yahoo.com','British Virgin Islands','Dutch','Other',18,'E','2025-02-05 17:35:19',0,0,0,'default','Galloway'),(858,'tracyELLIS148','Tracy','tracyELLIS148@hotmail.com','Tunisia','Spanish','Male',19,'B','2025-02-05 17:35:19',1,0,0,'default','Ellis'),(859,'seanRICHARDS807','Sean','seanRICHARDS807@hotmail.com','Cocos (Keeling) Islands','Spanish','Other',24,'D','2025-02-05 17:35:19',0,0,1,'default','Richards'),(860,'seanRAY611','Sean','seanRAY611@yahoo.com','Greece','Spanish','Other',30,'E','2025-02-05 17:35:19',0,0,0,'default','Ray'),(861,'donnaBOWMAN28','Donna','donnaBOWMAN28@gmail.com','Central African Republic','English','Male',29,'C','2025-02-05 17:35:19',0,1,0,'default','Bowman'),(862,'wayneNIELSEN854','Wayne','wayneNIELSEN854@gmail.com','Cambodia','Spanish','Other',23,'D','2025-02-05 17:35:19',0,1,0,'default','Nielsen'),(863,'alanHORNE329','Alan','alanHORNE329@hotmail.com','North Macedonia','Dutch','Male',22,'C','2025-02-05 17:35:19',1,0,0,'default','Horne'),(864,'johnBROWN462','John','johnBROWN462@hotmail.com','Turks and Caicos Islands','Spanish','Other',25,'C','2025-02-05 17:35:19',0,1,1,'default','Brown'),(865,'ashleyKNIGHT603','Ashley','ashleyKNIGHT603@gmail.com','Papua New Guinea','Dutch','Other',22,'D','2025-02-05 17:35:19',1,0,0,'default','Knight'),(866,'timothyMCCONNELL273','Timothy','timothyMCCONNELL273@yahoo.com','Palau','English','Male',25,'B','2025-02-05 17:35:19',0,1,0,'default','Mcconnell'),(867,'justinPEREZ141','Justin','justinPEREZ141@yahoo.com','Switzerland','English','Male',28,'D','2025-02-05 17:35:19',0,0,1,'default','Perez'),(868,'jerryDAVIS917','Jerry','jerryDAVIS917@hotmail.com','Heard Island and McDonald Islands','English','Male',28,'D','2025-02-05 17:35:19',1,1,0,'default','Davis'),(869,'royWALKER903','Roy','royWALKER903@gmail.com','Yemen','English','Other',24,'E','2025-02-05 17:35:19',0,1,0,'default','Walker'),(870,'nancyMITCHELL622','Nancy','nancyMITCHELL622@hotmail.com','Mayotte','English','Other',28,'C','2025-02-05 17:35:19',1,1,1,'default','Mitchell'),(871,'jessicaWALTON219','Jessica','jessicaWALTON219@gmail.com','Bahamas','Dutch','Female',26,'D','2025-02-05 17:35:19',0,1,0,'default','Walton'),(872,'jamesMATTHEWS375','James','jamesMATTHEWS375@hotmail.com','Saint Martin','English','Other',31,'E','2025-02-05 17:35:19',1,1,1,'default','Matthews'),(873,'joshuaHARRISON846','Joshua','joshuaHARRISON846@yahoo.com','Trinidad and Tobago','Dutch','Female',18,'E','2025-02-05 17:35:19',0,1,1,'default','Harrison'),(874,'nancyMENDOZA927','Nancy','nancyMENDOZA927@hotmail.com','Turkey','Dutch','Male',22,'E','2025-02-05 17:35:19',0,1,1,'default','Mendoza'),(875,'johnBUTLER91','John','johnBUTLER91@yahoo.com','Panama','Dutch','Other',22,'D','2025-02-05 17:35:19',1,0,0,'default','Butler'),(876,'aaronSOLIS130','Aaron','aaronSOLIS130@yahoo.com','Bulgaria','Spanish','Other',26,'E','2025-02-05 17:35:19',1,0,0,'default','Solis'),(877,'ginaGONZALEZ522','Gina','ginaGONZALEZ522@yahoo.com','Namibia','Dutch','Male',31,'E','2025-02-05 17:35:19',1,0,0,'default','Gonzalez'),(878,'kennethDAVIDSON960','Kenneth','kennethDAVIDSON960@yahoo.com','Honduras','English','Other',21,'D','2025-02-05 17:35:19',1,0,1,'default','Davidson'),(879,'laurenCOX139','Lauren','laurenCOX139@yahoo.com','Burkina Faso','Dutch','Other',23,'B','2025-02-05 17:35:19',0,1,1,'default','Cox'),(880,'dannyMCCORMICK63','Danny','dannyMCCORMICK63@yahoo.com','Ukraine','Dutch','Female',31,'B','2025-02-05 17:35:19',0,0,0,'default','Mccormick'),(881,'johnBENJAMIN470','John','johnBENJAMIN470@hotmail.com','Romania','English','Other',28,'E','2025-02-05 17:35:19',0,1,1,'default','Benjamin'),(882,'christopherRICHARD620','Christopher','christopherRICHARD620@hotmail.com','Cyprus','Spanish','Other',25,'E','2025-02-05 17:35:19',1,1,1,'default','Richard'),(883,'carolWALTERS508','Carol','carolWALTERS508@yahoo.com','Ethiopia','Spanish','Other',19,'E','2025-02-05 17:35:19',0,1,1,'default','Walters'),(884,'connorWILSON212','Connor','connorWILSON212@hotmail.com','Canada','Dutch','Other',27,'E','2025-02-05 17:35:19',1,0,0,'default','Wilson'),(885,'christineHOLLOWAY221','Christine','christineHOLLOWAY221@hotmail.com','Bouvet Island (Bouvetoya)','English','Female',24,'E','2025-02-05 17:35:19',1,1,0,'default','Holloway'),(886,'maxROSS901','Max','maxROSS901@hotmail.com','Botswana','Spanish','Female',22,'E','2025-02-05 17:35:19',0,1,1,'default','Ross'),(887,'michaelJOHNSON185','Michael','michaelJOHNSON185@hotmail.com','Jordan','Spanish','Male',27,'C','2025-02-05 17:35:19',0,0,1,'default','Johnson'),(888,'nathanielJOHNSON471','Nathaniel','nathanielJOHNSON471@hotmail.com','Guernsey','Spanish','Other',19,'D','2025-02-05 17:35:19',0,0,0,'default','Johnson'),(889,'kimberlyGARCIA540','Kimberly','kimberlyGARCIA540@yahoo.com','Pitcairn Islands','English','Other',19,'B','2025-02-05 17:35:19',0,0,1,'default','Garcia'),(890,'jacobRANDOLPH614','Jacob','jacobRANDOLPH614@hotmail.com','Brazil','Dutch','Other',18,'D','2025-02-05 17:35:19',0,1,1,'default','Randolph'),(891,'williamDAVIS479','William','williamDAVIS479@yahoo.com','Gibraltar','Dutch','Female',31,'E','2025-02-05 17:35:19',1,1,0,'default','Davis'),(892,'taraOWENS378','Tara','taraOWENS378@hotmail.com','Bangladesh','Spanish','Other',18,'D','2025-02-05 17:35:19',0,1,1,'default','Owens'),(893,'margaretPRESTON147','Margaret','margaretPRESTON147@yahoo.com','Congo','Spanish','Other',23,'B','2025-02-05 17:35:19',0,0,1,'default','Preston'),(894,'calebBARNES259','Caleb','calebBARNES259@gmail.com','Tokelau','English','Female',26,'E','2025-02-05 17:35:19',0,1,1,'default','Barnes'),(895,'michelleLEE527','Michelle','michelleLEE527@yahoo.com','Tokelau','Dutch','Other',23,'E','2025-02-05 17:35:19',0,0,0,'default','Lee'),(896,'heatherMELTON223','Heather','heatherMELTON223@yahoo.com','Wallis and Futuna','Spanish','Female',18,'B','2025-02-05 17:35:19',1,0,1,'default','Melton'),(897,'codySTEWART504','Cody','codySTEWART504@gmail.com','Albania','Spanish','Female',26,'D','2025-02-05 17:35:19',1,1,1,'default','Stewart'),(898,'lisaMACK69','Lisa','lisaMACK69@yahoo.com','Ecuador','Spanish','Other',25,'E','2025-02-05 17:35:19',0,0,1,'default','Mack'),(899,'maryJACKSON653','Mary','maryJACKSON653@yahoo.com','Myanmar','Dutch','Male',25,'E','2025-02-05 17:35:19',0,1,1,'default','Jackson'),(900,'robertFLETCHER642','Robert','robertFLETCHER642@gmail.com','Libyan Arab Jamahiriya','Dutch','Female',25,'D','2025-02-05 17:35:19',1,1,0,'default','Fletcher'),(901,'bridgetROBERTS637','Bridget','bridgetROBERTS637@yahoo.com','Zambia','English','Male',23,'B','2025-02-05 17:35:19',0,1,1,'default','Roberts'),(902,'davidDOUGHERTY384','David','davidDOUGHERTY384@yahoo.com','Georgia','Dutch','Male',18,'C','2025-02-05 17:35:19',1,1,0,'default','Dougherty'),(903,'rodneyNGUYEN619','Rodney','rodneyNGUYEN619@gmail.com','United States Virgin Islands','Spanish','Male',18,'E','2025-02-05 17:35:19',0,1,1,'default','Nguyen'),(904,'jeremyJOHNSON840','Jeremy','jeremyJOHNSON840@yahoo.com','Burkina Faso','Spanish','Female',27,'E','2025-02-05 17:35:19',0,0,0,'default','Johnson'),(905,'katherinePETERSON971','Katherine','katherinePETERSON971@hotmail.com','Belize','Spanish','Female',27,'E','2025-02-05 17:35:19',1,0,0,'default','Peterson'),(906,'christineCUNNINGHAM195','Christine','christineCUNNINGHAM195@gmail.com','Japan','Spanish','Female',18,'D','2025-02-05 17:35:19',0,1,0,'default','Cunningham'),(907,'michaelWATTS35','Michael','michaelWATTS35@hotmail.com','Greece','Spanish','Other',18,'D','2025-02-05 17:35:19',0,0,1,'default','Watts'),(908,'judyTAYLOR393','Judy','judyTAYLOR393@yahoo.com','Maldives','Spanish','Other',18,'E','2025-02-05 17:35:19',0,1,1,'default','Taylor'),(909,'joanneFIGUEROA924','Joanne','joanneFIGUEROA924@yahoo.com','Oman','Spanish','Male',18,'E','2025-02-05 17:35:19',0,1,1,'default','Figueroa'),(910,'brianCHUNG43','Brian','brianCHUNG43@yahoo.com','Sao Tome and Principe','Spanish','Other',22,'E','2025-02-05 17:35:19',1,0,1,'default','Chung'),(911,'dillonBRANCH40','Dillon','dillonBRANCH40@gmail.com','Austria','Dutch','Other',28,'E','2025-02-05 17:35:19',1,0,0,'default','Branch'),(912,'danielWHITE891','Daniel','danielWHITE891@hotmail.com','Tuvalu','Spanish','Female',18,'E','2025-02-05 17:35:19',1,0,0,'default','White'),(913,'lisaWOOD604','Lisa','lisaWOOD604@gmail.com','French Guiana','Spanish','Male',22,'C','2025-02-05 17:35:19',1,1,1,'default','Wood'),(914,'kevinLEWIS799','Kevin','kevinLEWIS799@hotmail.com','Austria','Dutch','Other',20,'A','2025-02-05 17:35:19',0,1,1,'default','Lewis'),(915,'rachelMCCLAIN221','Rachel','rachelMCCLAIN221@hotmail.com','Sweden','Spanish','Female',21,'C','2025-02-05 17:35:19',1,1,1,'default','Mcclain');
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_messages`
--

DROP TABLE IF EXISTS `user_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_messages` (
  `msg_id` int NOT NULL AUTO_INCREMENT,
  `chat_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `event_id` int DEFAULT NULL,
  `sent_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('sent','delivered','read') NOT NULL DEFAULT 'sent',
  PRIMARY KEY (`msg_id`),
  KEY `chat_id` (`chat_id`),
  KEY `sender_id` (`sender_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `user_messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `user_chats` (`chat_id`) ON DELETE CASCADE,
  CONSTRAINT `user_messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `user_messages_ibfk_3` FOREIGN KEY (`event_id`) REFERENCES `event_data` (`event_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_messages`
--

LOCK TABLES `user_messages` WRITE;
/*!40000 ALTER TABLE `user_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tags`
--

DROP TABLE IF EXISTS `user_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tags` (
  `tag_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`tag_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_tags_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON DELETE RESTRICT,
  CONSTRAINT `user_tags_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tags`
--

LOCK TABLES `user_tags` WRITE;
/*!40000 ALTER TABLE `user_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venues`
--

DROP TABLE IF EXISTS `venues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venues` (
  `venue_id` int NOT NULL AUTO_INCREMENT,
  `venue_name` varchar(255) DEFAULT NULL,
  `venue_capacity` mediumint DEFAULT NULL,
  `venue_address` varchar(255) DEFAULT NULL,
  `venue_city` varchar(100) DEFAULT NULL,
  `venue_state` varchar(100) DEFAULT NULL,
  `venue_zip` varchar(20) DEFAULT NULL,
  `venue_country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`venue_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venues`
--

LOCK TABLES `venues` WRITE;
/*!40000 ALTER TABLE `venues` DISABLE KEYS */;
INSERT INTO `venues` VALUES (1,'Pacha',1200,'C. de Atocha, 14','Barcelona','Catalonia','06878','Spain'),(2,'Opium',800,'C. de Atocha, 14','Ibiza','Balearic Islands','06878','Spain'),(3,'Hanger48',200,'C. de Atocha, 14','Madrid','Madrid','06878','Spain'),(4,'Icon',300,'C. de Atocha, 14','Madrid','Madrid','06878','Spain'),(5,'Istar',700,'C. de Atocha, 14','Madrid','Madrid','06878','Spain'),(6,'Goya Social Club',150,'C. de Atocha, 14','Madrid','Madrid','06878','Spain');
/*!40000 ALTER TABLE `venues` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-05 18:58:56
