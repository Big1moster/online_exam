-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: online_exam2
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add 用户数据表',6,'add_userprofile'),(17,'Can change 用户数据表',6,'change_userprofile'),(18,'Can delete 用户数据表',6,'delete_userprofile'),(19,'Can add 试卷',7,'add_exam'),(20,'Can change 试卷',7,'change_exam'),(21,'Can delete 试卷',7,'delete_exam'),(22,'Can add 试卷模板',8,'add_examtemplate'),(23,'Can change 试卷模板',8,'change_examtemplate'),(24,'Can delete 试卷模板',8,'delete_examtemplate'),(25,'Can add 知识点',9,'add_knowledge'),(26,'Can change 知识点',9,'change_knowledge'),(27,'Can delete 知识点',9,'delete_knowledge'),(28,'Can add 试卷方案',10,'add_plan'),(29,'Can change 试卷方案',10,'change_plan'),(30,'Can delete 试卷方案',10,'delete_plan'),(31,'Can add 问题',11,'add_question'),(32,'Can change 问题',11,'change_question'),(33,'Can delete 问题',11,'delete_question'),(34,'Can add 考试记录表',12,'add_examrecord'),(35,'Can change 考试记录表',12,'change_examrecord'),(36,'Can delete 考试记录表',12,'delete_examrecord');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(32) NOT NULL,
  `idcard` varchar(32) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `level` varchar(32) NOT NULL,
  `major` varchar(32) NOT NULL,
  `role` varchar(32) NOT NULL,
  `is_checked` tinyint(1) NOT NULL,
  `touxiang` varchar(100) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `idcard` (`idcard`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'2020-03-02 19:26:09.020778',0,'','',0,1,'2020-02-28 22:46:23.164891','邓晟峰','362502199702062658','pbkdf2_sha256$100000$6H5WV10uRUkj$3rqSoJ2y4QyTzt/3Bsw3UHRuIY3hFRu/PiGKYSxKE1g=','本科','软件工程','administrator',1,'images/2020/03/1.jpg','','2020-02-28 22:46:23.250665','2020-03-02 19:25:56.475282'),(2,NULL,0,'','',0,1,'2020-02-29 20:59:47.710054','邓晟峰1','362502199702062659','pbkdf2_sha256$100000$NvjnQ2asJAk1$fv8KT9TVXWpawufzffg3hdIGmjwOHyLInXYtHmRikKw=','本科','软件工程','student',0,'images/2019/12/touxiang_img.png','','2020-02-29 20:59:47.786850','2020-02-29 20:59:47.786850'),(3,NULL,0,'','',0,1,'2020-02-29 20:59:56.872024','邓晟峰2','362502199702062650','pbkdf2_sha256$100000$GLs4zhWPlviE$dBe64/wzDT5AO4GOrGAeuFpz8JCaF4Je/jhIAnzOqZY=','本科','软件工程','student',0,'images/2019/12/touxiang_img.png','','2020-02-29 20:59:56.941836','2020-02-29 20:59:56.941836'),(4,NULL,0,'','',0,1,'2020-02-29 21:00:04.685895','邓晟峰3','362502199702062657','pbkdf2_sha256$100000$2pAMnz691dHW$ox4SWCZ9+2jJSrk8IW0E9BQgEp2TN8exY7oR19axnZU=','本科','软件工程','student',1,'images/2019/12/touxiang_img.png','','2020-02-29 21:00:04.754712','2020-03-01 10:00:01.906252'),(5,'2020-03-02 19:06:44.652215',0,'','',0,1,'2020-03-02 19:06:44.358998','邓晟峰6','362502199702062611','pbkdf2_sha256$100000$IbxfdlZlTkSd$JA54HJ1G0NyI7SH3e77m2WQWEoW1d1f0sS2S2Hum1Jg=','本科','软件工程','student',0,'images/2019/12/touxiang_img.png','','2020-03-02 19:06:44.455737','2020-03-02 19:06:44.455737');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_userprofile_id_group_id_c3cc12c8_uniq` (`userprofile_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_userprofile_id_4ee96490_fk_auth_user_id` FOREIGN KEY (`userprofile_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissio_userprofile_id_permissio_97197848_uniq` (`userprofile_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permi_userprofile_id_7dc30d06_fk_auth_user` FOREIGN KEY (`userprofile_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(7,'users','exam'),(12,'users','examrecord'),(8,'users','examtemplate'),(9,'users','knowledge'),(10,'users','plan'),(11,'users','question'),(6,'users','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-02-28 21:38:32.704842'),(2,'contenttypes','0002_remove_content_type_name','2020-02-28 21:38:34.572151'),(3,'auth','0001_initial','2020-02-28 21:38:40.573107'),(4,'auth','0002_alter_permission_name_max_length','2020-02-28 21:38:41.861659'),(5,'auth','0003_alter_user_email_max_length','2020-02-28 21:38:41.932470'),(6,'auth','0004_alter_user_username_opts','2020-02-28 21:38:42.019238'),(7,'auth','0005_alter_user_last_login_null','2020-02-28 21:38:42.100060'),(8,'auth','0006_require_contenttypes_0002','2020-02-28 21:38:42.227723'),(9,'auth','0007_alter_validators_add_error_messages','2020-02-28 21:38:42.320466'),(10,'auth','0008_alter_user_username_max_length','2020-02-28 21:38:42.453078'),(11,'auth','0009_alter_user_last_name_max_length','2020-02-28 21:38:42.520930'),(12,'users','0001_initial','2020-02-28 21:39:00.646588'),(13,'admin','0001_initial','2020-02-28 21:39:05.977820'),(14,'admin','0002_logentry_remove_auto_add','2020-02-28 21:39:06.056611'),(15,'sessions','0001_initial','2020-02-28 21:39:07.484791'),(16,'users','0002_auto_20200228_2244','2020-02-28 22:44:25.513793'),(17,'users','0003_exam_allot','2020-02-29 14:49:26.172883'),(18,'users','0004_auto_20200229_2124','2020-02-29 21:25:06.023106'),(19,'users','0005_auto_20200301_1128','2020-03-01 11:28:55.554359'),(20,'users','0006_exam_exam_describe','2020-03-01 12:58:52.508457'),(21,'users','0007_auto_20200301_2041','2020-03-01 20:41:44.522528');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('em7le3idklnzgtaur7k87n5as7jcfrd2','ZTE2NmNlZWJkMWIwOGI3ZTkzN2VhMmM1MjdmNTQ0NWM1ZjY5MzM2Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNDM2YjRjYzk3NzA3MDM5OWNkYTg5NGI2YjVkOTZiMzc3ZGQ1NmNlIn0=','2020-03-15 01:05:01.513557'),('j9fyudfkt5mkzytp9ojydxe7lf543wa9','NmVlODQxNWQwYTQ2YjU4Nzg1MTRiYTViNDQxYjExMTA3YTEwYzk3ZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiNjc4ZmU4MjY2YzUyYTkzNDllMDE1OWIyZDMyNjQ0ZDliMmM5Njc5IiwicXVlcnlfZXhhbV9yZWNvcmRfZm9ybSI6eyJsZXZlbCI6Ilx1NjcyY1x1NzlkMSIsInN1YmplY3QiOiJcdTUzMTZcdTViNjYiLCJtYWpvciI6Ilx1OGY2Zlx1NGVmNlx1NWRlNVx1N2EwYiIsInVzZXJuYW1lIjoiIiwiaWRjYXJkIjoiIn0sInF1ZXJ5X2V4YW1fYWxsb3RfZm9ybSI6eyJsZXZlbCI6Ilx1NjcyY1x1NzlkMSIsInN1YmplY3QiOiJcdTUzMTZcdTViNjYiLCJtYWpvciI6Ilx1OGY2Zlx1NGVmNlx1NWRlNVx1N2EwYiIsImV4YW1fdGVtcGxhdGUiOiIifX0=','2020-03-16 23:16:17.597558');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge`
--

DROP TABLE IF EXISTS `knowledge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `knowledge_name` varchar(128) NOT NULL,
  `subject` varchar(32) NOT NULL,
  `level` varchar(32) NOT NULL,
  `major` varchar(32) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge`
--

LOCK TABLES `knowledge` WRITE;
/*!40000 ALTER TABLE `knowledge` DISABLE KEYS */;
INSERT INTO `knowledge` VALUES (1,'gbffdgshgfdhd','数学','本科','软件工程','2020-02-28 23:10:00.306970','2020-02-28 23:10:00.306970'),(2,'gbkjghkydtbcfhd','数学','本科','软件工程','2020-02-28 23:10:00.673986','2020-02-28 23:10:00.673986'),(3,'知识点3','化学','本科','软件工程','2020-02-28 23:14:13.720842','2020-02-28 23:14:13.720842'),(4,'化学知识点','化学','本科','软件工程','2020-02-28 23:44:14.263112','2020-02-28 23:44:14.263112');
/*!40000 ALTER TABLE `knowledge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_name` longtext NOT NULL,
  `option` longtext NOT NULL,
  `answer` varchar(8) NOT NULL,
  `score` int(11) NOT NULL,
  `subject` varchar(32) NOT NULL,
  `question_type` varchar(32) NOT NULL,
  `difficult` varchar(32) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  `knowledge_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_knowledge_id_2131a939_fk_knowledge_id` (`knowledge_id`),
  CONSTRAINT `question_knowledge_id_2131a939_fk_knowledge_id` FOREIGN KEY (`knowledge_id`) REFERENCES `knowledge` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'判断1','对@错','对',5,'数学','判断题','一般','2020-02-28 23:10:00.418712','2020-02-28 23:10:00.418712',1),(2,'判断2','对@错','对',51,'数学','判断题','困难','2020-02-28 23:10:00.739810','2020-02-28 23:10:00.739810',2),(3,'单选1','A、option_a\nB、option_b\nC、option_c\nD、option_d','a',51,'数学','单选题','困难','2020-02-28 23:10:00.805646','2020-02-28 23:10:00.805646',2),(4,'单选2','A、option_a\nB、option_b\nC、option_c\nD、option_d','a',51,'数学','单选题','困难','2020-02-28 23:10:00.887415','2020-02-28 23:10:00.887415',2),(5,'多选1','A、option_a\nB、option_b\nC、option_c\nD、option_d','ab',51,'数学','多选题','困难','2020-02-28 23:10:00.990142','2020-02-28 23:10:00.990142',2),(6,'题目1','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',1,'化学','单选题','简单','2020-02-28 23:15:07.913512','2020-02-28 23:15:07.913512',3),(7,'题目2','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',2,'化学','多选题','困难','2020-02-28 23:15:29.413383','2020-02-28 23:15:29.413383',3),(8,'题目3','','y',1,'化学','判断题','困难','2020-02-28 23:15:46.929637','2020-02-28 23:15:46.929637',3),(9,'单选题1','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',2,'化学','单选题','困难','2020-02-28 23:44:45.928802','2020-03-02 20:34:55.904033',4),(10,'多选题','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',1,'化学','多选题','困难','2020-02-28 23:45:08.330533','2020-02-28 23:45:08.331529',4),(11,'多选题2','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',2,'化学','多选题','困难','2020-02-28 23:45:26.375896','2020-02-28 23:45:26.375896',4),(12,'化学题3','A、选项a\nB、选项a\nC、选项a\nD、选项a','a',1,'化学','多选题','困难','2020-02-28 23:45:50.506401','2020-02-28 23:45:50.506401',4),(13,'判断1','','y',2,'化学','判断题','困难','2020-02-28 23:46:04.968713','2020-02-28 23:46:04.968713',4),(14,'判断2','','y',2,'化学','判断题','困难','2020-02-28 23:46:19.825966','2020-02-28 23:46:19.825966',4),(15,'判断3','','y',5,'化学','判断题','困难','2020-02-28 23:46:32.950064','2020-02-28 23:46:32.950064',4),(16,'判断4','','y',5,'化学','判断题','困难','2020-02-28 23:46:46.338120','2020-02-28 23:46:46.338120',4),(17,'判断4','','y',8,'化学','判断题','困难','2020-02-28 23:47:01.184050','2020-02-28 23:47:01.184050',4),(18,'判断5','','y',9,'化学','判断题','困难','2020-02-28 23:47:13.664847','2020-02-28 23:47:13.664847',4);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_exam`
--

DROP TABLE IF EXISTS `users_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `major` varchar(32) NOT NULL,
  `level` varchar(32) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  `exam_template_id` int(11) NOT NULL,
  `exam_name` varchar(32) NOT NULL,
  `question_id_ls` varchar(128) NOT NULL,
  `exam_describe` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_exam_exam_template_id_0fb5e438_fk_users_examtemplate_id` (`exam_template_id`),
  CONSTRAINT `users_exam_exam_template_id_0fb5e438_fk_users_examtemplate_id` FOREIGN KEY (`exam_template_id`) REFERENCES `users_examtemplate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_exam`
--

LOCK TABLES `users_exam` WRITE;
/*!40000 ALTER TABLE `users_exam` DISABLE KEYS */;
INSERT INTO `users_exam` VALUES (7,'软件工程','本科','2020-02-29 00:57:42.567340','2020-03-01 00:34:41.718760',2,'试卷1','{\"single_choice_id_ls\": [9], \"mul_choice_id_ls\": [10, 10, 11], \"judge_id_ls\": [14, 16, 13, 14, 17]}','的哈佛i说大话覅欧式的基础阶段是VS的'),(11,'软件工程','本科','2020-02-29 09:45:55.675684','2020-03-01 01:02:44.829598',2,'试卷2','{\"single_choice_id_ls\": [9], \"mul_choice_id_ls\": [11, 7, 10], \"judge_id_ls\": [14, 15, 16, 14, 18]}','山豆根地方手感特好投入微软'),(12,'软件工程','本科','2020-02-29 09:45:55.675684','2020-03-01 01:02:38.002504',2,'试卷2','{\"single_choice_id_ls\": [9], \"mul_choice_id_ls\": [11, 7, 10], \"judge_id_ls\": [14, 14, 14, 15, 13]}','狗头人问一问如物价和肉体上');
/*!40000 ALTER TABLE `users_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_exam_allot`
--

DROP TABLE IF EXISTS `users_exam_allot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_exam_allot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `userprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_exam_allot_exam_id_userprofile_id_15f9b496_uniq` (`exam_id`,`userprofile_id`),
  KEY `users_exam_allot_userprofile_id_48fe3df5_fk_auth_user_id` (`userprofile_id`),
  CONSTRAINT `users_exam_allot_exam_id_518a22a1_fk_users_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `users_exam` (`id`),
  CONSTRAINT `users_exam_allot_userprofile_id_48fe3df5_fk_auth_user_id` FOREIGN KEY (`userprofile_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_exam_allot`
--

LOCK TABLES `users_exam_allot` WRITE;
/*!40000 ALTER TABLE `users_exam_allot` DISABLE KEYS */;
INSERT INTO `users_exam_allot` VALUES (11,11,1),(3,11,2),(2,11,3),(1,11,4),(8,12,1),(10,12,2),(6,12,3),(5,12,4);
/*!40000 ALTER TABLE `users_exam_allot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_examrecord`
--

DROP TABLE IF EXISTS `users_examrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_examrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer` varchar(128) DEFAULT NULL,
  `grade` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  `exam_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_examrecord_exam_id_ced4a086_fk_users_exam_id` (`exam_id`),
  KEY `users_examrecord_user_id_38f94405_fk_auth_user_id` (`user_id`),
  CONSTRAINT `users_examrecord_exam_id_ced4a086_fk_users_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `users_exam` (`id`),
  CONSTRAINT `users_examrecord_user_id_38f94405_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_examrecord`
--

LOCK TABLES `users_examrecord` WRITE;
/*!40000 ALTER TABLE `users_examrecord` DISABLE KEYS */;
INSERT INTO `users_examrecord` VALUES (3,'',200,'2020-03-02 20:33:16.545240','2020-03-02 20:33:53.275810',12,1),(4,'',20,'2020-03-02 20:34:56.006758','2020-03-02 20:36:02.212468',12,1);
/*!40000 ALTER TABLE `users_examrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_examtemplate`
--

DROP TABLE IF EXISTS `users_examtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_examtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_template_name` varchar(32) NOT NULL,
  `exam_name` varchar(32) NOT NULL,
  `exam_th` int(11) NOT NULL,
  `subject` varchar(32) NOT NULL,
  `difficult` varchar(32) NOT NULL,
  `exam_start_time` datetime(6) NOT NULL,
  `exam_end_time` datetime(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  `plan_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exam_template_name` (`exam_template_name`),
  UNIQUE KEY `exam_name` (`exam_name`),
  KEY `users_examtemplate_plan_id_8a02ccb5_fk_users_plan_id` (`plan_id`),
  CONSTRAINT `users_examtemplate_plan_id_8a02ccb5_fk_users_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `users_plan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_examtemplate`
--

LOCK TABLES `users_examtemplate` WRITE;
/*!40000 ALTER TABLE `users_examtemplate` DISABLE KEYS */;
INSERT INTO `users_examtemplate` VALUES (1,'试卷模板1','第一次考试',1,'化学','简单','2020-01-01 09:00:00.000000','2020-01-01 11:00:00.000000','2020-02-28 22:47:38.129594','2020-02-28 22:47:38.129594',1),(2,'模板2','考试2',1,'化学','困难','2020-01-01 09:00:00.000000','2020-01-01 11:00:00.000000','2020-02-28 23:11:41.325896','2020-02-28 23:11:41.325896',1);
/*!40000 ALTER TABLE `users_examtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_plan`
--

DROP TABLE IF EXISTS `users_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(32) NOT NULL,
  `single_choice_num` int(11) NOT NULL,
  `single_choice_score` int(11) NOT NULL,
  `mul_choice_num` int(11) NOT NULL,
  `mul_choice_score` int(11) NOT NULL,
  `judge_num` int(11) NOT NULL,
  `judge_score` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `plan_name` (`plan_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_plan`
--

LOCK TABLES `users_plan` WRITE;
/*!40000 ALTER TABLE `users_plan` DISABLE KEYS */;
INSERT INTO `users_plan` VALUES (1,'方案1',1,2,3,4,5,6,'2020-02-28 22:47:14.091914','2020-02-28 22:47:14.091914');
/*!40000 ALTER TABLE `users_plan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-05 10:44:43
