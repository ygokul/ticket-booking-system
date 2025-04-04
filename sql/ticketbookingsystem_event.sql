-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ticketbookingsystem
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_name` varchar(20) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_time` time DEFAULT NULL,
  `total_seats` int DEFAULT NULL,
  `available_seats` int DEFAULT NULL,
  `ticket_price` decimal(10,2) DEFAULT NULL,
  `event_type` enum('Movie','Sports','Concert') DEFAULT NULL,
  `venue_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES ('rock cup','2025-01-01','09:00:00',10050,10050,500.05,'Concert','casagrand'),('worldcup','2025-01-02','09:00:00',10100,10100,500.05,'Sports',NULL),('moonlight','2025-01-03','09:30:00',10050,10052,1500.09,'Concert',NULL),('twilt','2025-01-04','10:00:00',15500,15500,200.05,'Movie','royal'),('football','2025-01-01','10:00:00',10500,10502,700.05,'Sports','popi'),('rocky','2025-01-05','11:10:00',20500,20500,5000.05,'Concert','tres'),('popz','2025-02-01','10:30:00',10050,10050,300.05,'Movie','cres'),('cricket','2025-01-03','09:30:00',18500,18500,2000.09,'Sports','chepauk'),('fire','2025-01-04','08:30:00',10250,10239,200.05,'Movie','theatre'),('tennis','2025-01-05','10:00:00',10020,10020,1000.00,'Sports','tulip'),('sai','2003-09-09','12:56:09',32,32,50.00,'Movie','jesus'),('saraaa','2002-09-09','09:09:09',67,61,89.00,'Sports','jesus'),('ipl','2025-07-09','04:44:44',245,245,1000.09,'Sports','chepauk'),('cookery','2026-09-09','11:09:09',250,250,400.09,'Sports','france ');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-04 18:42:59
