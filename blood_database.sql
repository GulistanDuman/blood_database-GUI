-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: blood_database
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.22.04.1

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
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `block` varchar(50) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `date` date DEFAULT NULL,
  `room_number` varchar(50) DEFAULT NULL,
  `patient_id` char(8) DEFAULT NULL,
  `doctor_id` char(8) DEFAULT NULL,
  `hospital_id` varchar(50) DEFAULT NULL,
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`ID`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`ID`),
  CONSTRAINT `appointment_ibfk_3` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`host_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES ('A3','13:00:00','2024-11-18','213','20369673','20012002','MOZAIK'),('A3','14:00:00','2024-01-15','215','20369673','20012002','MOZAIK'),('A3','14:00:00','2024-01-15','215','19992002','20012002','GUL'),('A','17:26:50','2025-01-04','216.0','19992002','20012002','GUL'),('A3','23:24:53','2025-01-24',NULL,'19992002','20012002','GUL'),('A3','12:43:59','2025-01-17',NULL,'19992002','20012002','GUL');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bloodtype`
--

DROP TABLE IF EXISTS `bloodtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloodtype` (
  `blood_group` varchar(6) NOT NULL,
  PRIMARY KEY (`blood_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloodtype`
--

LOCK TABLES `bloodtype` WRITE;
/*!40000 ALTER TABLE `bloodtype` DISABLE KEYS */;
INSERT INTO `bloodtype` VALUES ('A RH-'),('A RH+'),('AB RH-'),('AB RH+'),('B RH-'),('B RH+'),('O RH-'),('O RH+');
/*!40000 ALTER TABLE `bloodtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `ID` char(8) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `shift` varchar(50) DEFAULT NULL,
  `vigil` varchar(10) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES ('20012002','FERHUN YORGANCI','08:00-16:00','Monday','images/20012002.jpeg'),('20022003','CEM KALYONCU','08:00-16:00','Tuesday','images/20022003.jpeg'),('20032004','VESILE EVRIM','08:00-16:00','Wednesday','images/20032004.jpeg'),('20042005','YONAL KIRSAL','08:00-16:00','Thursday','images/20042005.jpeg'),('20052006','ZAFER ERENEL','08:00-16:00','Friday','images/20052006.jpeg'),('20062007','FADIL ERSOZ','08:00-16:00','Saturday','images/20062007.jpeg'),('20072008','ALI DAYIOGLU','08:00-16:00','Sunday','images/20072008.jpeg');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `name` varchar(50) DEFAULT NULL,
  `ID` char(8) NOT NULL,
  `age` int DEFAULT NULL,
  `blood_group` varchar(6) DEFAULT NULL,
  `disease` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES ('Ragıp','19991999',25,'O RH-','None'),('Ahmet','20002000',36,'00 RH+','None'),('MEHMET AKIN','20120653',24,'O RH-',NULL),('YAREN ESKI','21120360',22,'O RH+',NULL),('Gülistan','21120379',23,'A0 RH+','none'),('MURAT AKIN','21120488',15,'A RH-','Thyroid Disorder'),('KAAN ARSLAN','21124022',24,'B RH+',NULL),('Dünya','24121068',18,'A0 RH+','GRİP'),('ISMAIL KUYUCU','24121871',14,'AB RH+','Anemia'),('GÜL','60006000',18,'0 RH-','None');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital`
--

DROP TABLE IF EXISTS `hospital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospital` (
  `host_name` varchar(50) NOT NULL,
  `address` varchar(50) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `dept_host` varchar(50) DEFAULT NULL,
  `block` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`host_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital`
--

LOCK TABLES `hospital` WRITE;
/*!40000 ALTER TABLE `hospital` DISABLE KEYS */;
INSERT INTO `hospital` VALUES ('GUL','ISTANBUL',6400,'PSYCHIATRY','A3'),('INCI','ANTALYA',9000,'TRAINING AND RESEARCH','C7'),('MELEK','IZMIR',5000,'GENERAL','B4'),('MOZAIK','HATAY',3000,'MATERNITY','D5');
/*!40000 ALTER TABLE `hospital` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurse`
--

DROP TABLE IF EXISTS `nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse` (
  `ID` char(8) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `shift` varchar(50) DEFAULT NULL,
  `vigil` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse`
--

LOCK TABLES `nurse` WRITE;
/*!40000 ALTER TABLE `nurse` DISABLE KEYS */;
INSERT INTO `nurse` VALUES ('20102011','AYSE DEMIR','08:00-18:00','Monday-Friday'),('20112012','ILKAY KARATAS','08:00-18:00','Tuesday-Thursday'),('20122013','SENA OKSUZ','08:00-18:00','Wednesday-Friday-Saturday'),('20132014','DEFNE ARSLAN','08:00-18:00','Thursday-Sunday');
/*!40000 ALTER TABLE `nurse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `ID` char(8) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `need_bloodgroup` varchar(6) DEFAULT NULL,
  `host_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES ('19992002','RAVZA EKER','IZMIR','O RH-','MELEK'),('20012005','SEZEN AY','HATAY','A RH+','MOZAIK'),('20072002','UMIT CUZDAN','ANTALYA','O RH+','INCI'),('20112008','MECIT KARA','ISTANBUL','B RH+','GUL'),('20369673','GONUL YILMAZ','USAK','AB RH-','MOZAIK');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('Berivan','12345'),('Gülistan','Glstn825136!'),('Gülistan ','Glstn825136!');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-03 19:52:29
