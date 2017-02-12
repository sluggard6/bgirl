-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: bgirl
-- ------------------------------------------------------
-- Server version	5.7.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_log`
--

DROP TABLE IF EXISTS `admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(20) NOT NULL COMMENT '行为',
  `user_id` int(11) DEFAULT NULL COMMENT '用户id',
  `key1` varchar(50) DEFAULT NULL COMMENT '查询关键字1',
  `key2` varchar(50) DEFAULT NULL COMMENT '查询关键字2',
  `key3` varchar(50) DEFAULT NULL COMMENT '查询关键字3',
  `data` mediumtext,
  `ip` char(15) DEFAULT NULL COMMENT 'ip',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `action` (`action`),
  KEY `user_id` (`user_id`),
  KEY `key1` (`key1`),
  KEY `key2` (`key2`),
  KEY `key3` (`key3`),
  KEY `create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_log`
--

LOCK TABLES `admin_log` WRITE;
/*!40000 ALTER TABLE `admin_log` DISABLE KEYS */;
INSERT INTO `admin_log` VALUES (1,'创建系统用户',1,'1','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:18:55'),(2,'创建系统用户',1,'2','透视诱惑',NULL,NULL,'127.0.0.1','2017-02-12 08:20:47'),(3,'创建系统用户',1,'3','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:26:03'),(4,'创建系统用户',1,'4','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:28:55'),(5,'创建系统用户',1,'5','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:29:19'),(6,'创建系统用户',1,'6','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:32:14'),(7,'创建系统用户',1,'7','诱人',NULL,NULL,'127.0.0.1','2017-02-12 08:41:54'),(8,'创建系统用户',1,'8','test',NULL,NULL,'127.0.0.1','2017-02-12 09:06:05'),(9,'创建系统用户',1,'9','test',NULL,NULL,'127.0.0.1','2017-02-12 09:06:39'),(10,'创建系统用户',1,'10','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:18:12'),(11,'创建系统用户',1,'11','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:21:46'),(12,'创建系统用户',1,'12','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:24:32'),(13,'创建系统用户',1,'13','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:25:14'),(14,'创建系统用户',1,'14','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:26:17'),(15,'更新系统用户',1,'1','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:31:08'),(16,'更新系统用户',1,'1','诱人',NULL,NULL,'127.0.0.1','2017-02-12 09:31:58'),(17,'创建系统用户',1,'15','test1',NULL,NULL,'127.0.0.1','2017-02-12 09:32:18'),(18,'创建系统用户',1,'16','test1',NULL,NULL,'127.0.0.1','2017-02-12 09:32:21'),(19,'创建系统用户',1,'17','fff',NULL,NULL,'127.0.0.1','2017-02-12 09:38:16'),(20,'创建系统用户',1,'18','fff',NULL,NULL,'127.0.0.1','2017-02-12 09:38:41'),(21,'创建系统用户',1,'19','123',NULL,NULL,'127.0.0.1','2017-02-12 09:46:55'),(22,'创建系统用户',1,'20','123',NULL,NULL,'127.0.0.1','2017-02-12 09:46:59'),(23,'创建系统用户',1,'21','123',NULL,NULL,'127.0.0.1','2017-02-12 09:47:02'),(24,'创建系统用户',1,'22','345',NULL,NULL,'127.0.0.1','2017-02-12 09:54:33'),(25,'更新系统用户',1,'22','345',NULL,NULL,'127.0.0.1','2017-02-12 09:54:49'),(26,'创建系统用户',1,'23','含含',NULL,NULL,'127.0.0.1','2017-02-12 11:29:54'),(27,'新组添加',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 11:40:29'),(28,'更新系统用户',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 11:41:39'),(29,'新组添加',1,'2','北包包',NULL,NULL,'127.0.0.1','2017-02-12 11:41:53'),(30,'更新',1,'1',NULL,NULL,'[u\'2\']','127.0.0.1','2017-02-12 12:07:48'),(31,'更新',1,'1',NULL,NULL,'[u\'2\']','127.0.0.1','2017-02-12 12:08:52'),(32,'更新',1,'1',NULL,NULL,'[u\'2\']','127.0.0.1','2017-02-12 12:09:45'),(33,'更新',1,'1',NULL,NULL,'[u\'1\']','127.0.0.1','2017-02-12 12:09:53'),(34,'创建系统权限',1,'111','频道管理',NULL,NULL,'127.0.0.1','2017-02-12 12:15:44'),(35,'更新系统权限',1,'111','频道管理',NULL,NULL,'127.0.0.1','2017-02-12 12:17:10'),(36,'创建系统权限',1,'111001','频道列表',NULL,NULL,'127.0.0.1','2017-02-12 12:18:47'),(37,'创建系统权限',1,'111002','专辑列表',NULL,NULL,'127.0.0.1','2017-02-12 12:20:17'),(38,'创建系统角色',1,'2','管理员',NULL,NULL,'127.0.0.1','2017-02-12 12:20:57'),(39,'更新系统角色权限',1,'2','管理员',NULL,'[u\'111\', u\'111001\', u\'111002\']','127.0.0.1','2017-02-12 12:21:29'),(40,'创建系统用户',1,'2','gxx',NULL,NULL,'127.0.0.1','2017-02-12 12:22:17'),(41,'更新系统用户角色',1,'2',NULL,NULL,'[u\'2\']','127.0.0.1','2017-02-12 12:22:44'),(42,'更新',2,'1',NULL,NULL,'[u\'2\', u\'1\']','127.0.0.1','2017-02-12 12:23:32'),(43,'更新系统用户角色',1,'1',NULL,NULL,'[u\'2\', u\'1\']','127.0.0.1','2017-02-12 13:40:23'),(44,'修改组',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 15:38:00'),(45,'新组添加',1,'3','test',NULL,NULL,'127.0.0.1','2017-02-12 15:39:09'),(46,'修改组',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 17:08:48'),(47,'修改组',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 17:10:03'),(48,'修改组',1,'1','aaa',NULL,NULL,'127.0.0.1','2017-02-12 17:22:45'),(49,'新组添加',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 17:25:31'),(50,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 17:41:41'),(51,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 17:48:45'),(52,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 17:52:47'),(53,'新组添加',1,'5','456',NULL,NULL,'127.0.0.1','2017-02-12 17:55:20'),(54,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 17:59:41'),(55,'新组添加',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:07:21'),(56,'新组添加',1,'7','222',NULL,NULL,'127.0.0.1','2017-02-12 18:09:12'),(57,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:09:31'),(58,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:09:40'),(59,'修改组',1,'5','456',NULL,NULL,'127.0.0.1','2017-02-12 18:09:48'),(60,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 18:09:56'),(61,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 18:10:04'),(62,'修改组',1,'4','123',NULL,NULL,'127.0.0.1','2017-02-12 18:11:21'),(63,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:11:27'),(64,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:11:33'),(65,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:12:44'),(66,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:14:21'),(67,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:14:34'),(68,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:14:43'),(69,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:17:20'),(70,'修改组',1,'6','111',NULL,NULL,'127.0.0.1','2017-02-12 18:17:25');
/*!40000 ALTER TABLE `admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_permission`
--

DROP TABLE IF EXISTS `admin_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_permission` (
  `id` varchar(20) NOT NULL DEFAULT '' COMMENT '权限分级id',
  `parent_id` varchar(20) NOT NULL COMMENT '父id',
  `name` varchar(50) NOT NULL COMMENT '权限名',
  `key` varchar(50) DEFAULT NULL COMMENT '权限关键字 - 关联程序实现，慎修改',
  `path` varchar(200) DEFAULT NULL COMMENT '权限路径, 无功能则无路径',
  `description` varchar(200) DEFAULT NULL COMMENT '权限描述',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_permission`
--

LOCK TABLES `admin_permission` WRITE;
/*!40000 ALTER TABLE `admin_permission` DISABLE KEYS */;
INSERT INTO `admin_permission` VALUES ('111','0','频道管理','channel','','频道管理',1),('111001','111','频道列表','channel','/channel/list','',1),('111002','111','专辑列表','group','/channel/group_list','',1),('999','0','系统管理','','','',1),('999001','999','后台用户管理','sys_user','/manage/user','添加、修改、移除用户，关联角色。',1),('999002','999','角色管理','sys_role','/manage/role','添加、修改、移除角色，关联权限。',1),('999003','999','权限管理','sys_permission','/manage/permission','添加、修改、移除权限',1),('999004','999','系统日志','sys_log','/manage/log','',1);
/*!40000 ALTER TABLE `admin_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_role`
--

DROP TABLE IF EXISTS `admin_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL COMMENT '角色名',
  `description` varchar(200) DEFAULT NULL COMMENT '角色描述',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_role`
--

LOCK TABLES `admin_role` WRITE;
/*!40000 ALTER TABLE `admin_role` DISABLE KEYS */;
INSERT INTO `admin_role` VALUES (1,'admin','系统管理员',1),(2,'管理员','管理员',1);
/*!40000 ALTER TABLE `admin_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_role_permission`
--

DROP TABLE IF EXISTS `admin_role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_role_permission` (
  `role_id` int(11) NOT NULL,
  `permission_id` varchar(20) NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `fk_admin_role_permission_admin_role1_idx` (`role_id`),
  KEY `fk_admin_role_permission_admin_permission1_idx` (`permission_id`),
  CONSTRAINT `fk_admin_role_permission_admin_permission1` FOREIGN KEY (`permission_id`) REFERENCES `admin_permission` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_admin_role_permission_admin_role1` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_role_permission`
--

LOCK TABLES `admin_role_permission` WRITE;
/*!40000 ALTER TABLE `admin_role_permission` DISABLE KEYS */;
INSERT INTO `admin_role_permission` VALUES (1,'999'),(1,'999001'),(1,'999002'),(1,'999003'),(1,'999004'),(2,'111'),(2,'111001'),(2,'111002');
/*!40000 ALTER TABLE `admin_role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_role_user`
--

DROP TABLE IF EXISTS `admin_role_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_role_user` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `fk_admin_role_user_admin_user1_idx` (`user_id`),
  KEY `fk_admin_role_user_admin_role1_idx` (`role_id`),
  CONSTRAINT `fk_admin_role_user_admin_role1` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_admin_role_user_admin_user1` FOREIGN KEY (`user_id`) REFERENCES `admin_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_role_user`
--

LOCK TABLES `admin_role_user` WRITE;
/*!40000 ALTER TABLE `admin_role_user` DISABLE KEYS */;
INSERT INTO `admin_role_user` VALUES (1,1),(1,2),(2,2);
/*!40000 ALTER TABLE `admin_role_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_user`
--

DROP TABLE IF EXISTS `admin_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL COMMENT '用户名',
  `password` varchar(50) NOT NULL DEFAULT '' COMMENT '密码',
  `description` varchar(50) DEFAULT NULL COMMENT '用户描述',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_user`
--

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;
INSERT INTO `admin_user` VALUES (1,'admin','e10adc3949ba59abbe56e057f20f883e','系统管理员',1,'2014-03-13 06:52:46'),(2,'gxx','e10adc3949ba59abbe56e057f20f883e','',1,'2017-02-12 12:22:16');
/*!40000 ALTER TABLE `admin_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT '0',
  `name` varchar(45) NOT NULL COMMENT '频道表',
  `description` text,
  `thumb` varchar(200) DEFAULT NULL COMMENT '缩略图',
  `status` int(11) NOT NULL DEFAULT '1' COMMENT '0:失效，1:有效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COMMENT='频道表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
INSERT INTO `channel` VALUES (1,0,'诱人','诱人',NULL,1,'2017-02-12 16:18:55','2017-02-12 08:18:55'),(2,0,'透视诱惑','透视诱惑',NULL,1,'2017-02-12 16:20:46','2017-02-12 08:20:46'),(3,0,'诱人','诱人',NULL,1,'2017-02-12 16:26:02','2017-02-12 08:26:02'),(4,0,'诱人','诱人',NULL,1,'2017-02-12 16:28:55','2017-02-12 08:28:55'),(5,0,'诱人','诱人',NULL,0,'2017-02-12 16:29:19','2017-02-12 08:29:19'),(6,0,'诱人','诱人',NULL,1,'2017-02-12 16:32:14','2017-02-12 08:32:14'),(7,0,'诱人','诱人',NULL,1,'2017-02-12 16:41:53','2017-02-12 08:41:53'),(8,0,'test','test',NULL,1,'2017-02-12 17:06:05','2017-02-12 09:06:05'),(9,0,'test','test',NULL,1,'2017-02-12 17:06:38','2017-02-12 09:06:38'),(10,0,'诱人','诱人',NULL,1,'2017-02-12 17:18:11','2017-02-12 09:18:11'),(11,0,'诱人','诱人',NULL,1,'2017-02-12 17:21:45','2017-02-12 09:21:45'),(12,0,'诱人','诱人',NULL,1,'2017-02-12 17:24:31','2017-02-12 09:24:31'),(13,0,'诱人','诱人',NULL,1,'2017-02-12 17:25:14','2017-02-12 09:25:14'),(14,0,'诱人','诱人',NULL,1,'2017-02-12 17:26:16','2017-02-12 09:26:16'),(15,0,'test1','test1',NULL,1,'2017-02-12 17:32:18','2017-02-12 09:32:18'),(16,0,'test1','test1',NULL,1,'2017-02-12 17:32:20','2017-02-12 09:32:20'),(17,0,'fff','fff',NULL,1,'2017-02-12 17:38:16','2017-02-12 09:38:16'),(18,0,'fff','fff',NULL,1,'2017-02-12 17:38:40','2017-02-12 09:38:40'),(19,0,'123','123',NULL,1,'2017-02-12 17:46:55','2017-02-12 09:46:55'),(20,0,'123','123',NULL,1,'2017-02-12 17:46:58','2017-02-12 09:46:58'),(21,0,'123','123',NULL,1,'2017-02-12 17:47:02','2017-02-12 09:47:02'),(22,0,'345','456',NULL,1,'2017-02-12 17:54:32','2017-02-12 09:54:49'),(23,0,'含含','含含',NULL,1,'2017-02-12 19:29:53','2017-02-12 11:29:53');
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charge`
--

DROP TABLE IF EXISTS `charge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `charge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL COMMENT '用户id，可以为空',
  `phone` varchar(16) DEFAULT NULL COMMENT '用户手机号码，可以为空',
  `amount` int(11) DEFAULT NULL COMMENT '金额，单位为分',
  `status` int(11) DEFAULT '1' COMMENT '状态，1 新建，2 完成，3 取消',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ip` varchar(32) DEFAULT NULL,
  `score` int(11) DEFAULT NULL COMMENT '充值赠送积分',
  `paid` int(11) DEFAULT NULL COMMENT '实际需要支付金额，单位为分',
  `category` int(11) DEFAULT '1' COMMENT '充值类型，用户，系统',
  `source` int(11) DEFAULT NULL,
  `pay_by` int(11) DEFAULT NULL,
  `ask_for` int(11) DEFAULT NULL COMMENT '充值邀请用户',
  `memo` varchar(200) DEFAULT NULL COMMENT '备注',
  `ask_for_status` int(11) DEFAULT NULL COMMENT '邀请充值状态',
  `discount_info` varchar(200) DEFAULT NULL COMMENT '充值折扣活动',
  `day` int(5) DEFAULT NULL,
  `discount_id` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_charge_user_id` (`user_id`),
  KEY `idx_charge_pay_by` (`pay_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charge`
--

LOCK TABLES `charge` WRITE;
/*!40000 ALTER TABLE `charge` DISABLE KEYS */;
/*!40000 ALTER TABLE `charge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '名称',
  `description` text COMMENT '说明',
  `status` int(11) DEFAULT '1',
  `thumb` varchar(200) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='图片分组';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
INSERT INTO `group` VALUES (1,'aaa','aaa版本',1,NULL,'2017-02-12 19:40:29','2017-02-12 11:41:39'),(2,'北包包','北包包',1,NULL,'2017-02-12 19:41:53','2017-02-12 11:41:53'),(3,'test','test1',1,'','2017-02-12 23:39:09','2017-02-12 15:39:09'),(4,'123','123',0,'2017/02/13/03058ce9b42532ad.jpg','2017-02-13 01:25:30','2017-02-12 17:59:41'),(5,'456','ss',0,'2017/02/13/312819e1ccc642b1.jpg','2017-02-13 01:55:20','2017-02-12 17:55:20'),(6,'111','',1,'','2017-02-13 02:07:20','2017-02-12 18:17:20'),(7,'222','',0,'','2017-02-13 02:09:11','2017-02-12 18:09:11');
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_channel_mapping`
--

DROP TABLE IF EXISTS `group_channel_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_channel_mapping` (
  `group_id` int(11) NOT NULL COMMENT '分组id',
  `channel_id` int(11) NOT NULL COMMENT '频道id',
  PRIMARY KEY (`group_id`,`channel_id`),
  KEY `channel_id_idx` (`channel_id`),
  KEY `group_id_idx` (`group_id`),
  CONSTRAINT `channel_id` FOREIGN KEY (`channel_id`) REFERENCES `channel` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='频道图组映射表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_channel_mapping`
--

LOCK TABLES `group_channel_mapping` WRITE;
/*!40000 ALTER TABLE `group_channel_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_channel_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_pic_mapping`
--

DROP TABLE IF EXISTS `group_pic_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_pic_mapping` (
  `group_id` int(11) NOT NULL,
  `pic_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`pic_id`),
  KEY `group_pic_id_idx` (`pic_id`),
  KEY `pic_group_id_idx` (`group_id`),
  CONSTRAINT `group_pic_id` FOREIGN KEY (`pic_id`) REFERENCES `pic` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pic_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_pic_mapping`
--

LOCK TABLES `group_pic_mapping` WRITE;
/*!40000 ALTER TABLE `group_pic_mapping` DISABLE KEYS */;
INSERT INTO `group_pic_mapping` VALUES (1,6),(1,7),(1,8),(5,23),(4,25),(6,31),(6,32);
/*!40000 ALTER TABLE `group_pic_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pic`
--

DROP TABLE IF EXISTS `pic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL COMMENT '文字说明',
  `min` varchar(200) NOT NULL COMMENT '图片地址(小)',
  `normal` varchar(200) NOT NULL COMMENT '图片地址(中)',
  `max` varchar(200) NOT NULL COMMENT '图片地址(大)',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COMMENT='图片表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pic`
--

LOCK TABLES `pic` WRITE;
/*!40000 ALTER TABLE `pic` DISABLE KEYS */;
INSERT INTO `pic` VALUES (1,'aaa','2017/02/13/fb31d8c890ec9616.jpg','2017/02/13/fb31d8c890ec9616.jpg','2017/02/13/fb31d8c890ec9616.jpg','2017-02-13 01:08:30','2017-02-12 17:08:30'),(2,'aaa','2017/02/13/9f749a5bf44578f4.jpg','2017/02/13/9f749a5bf44578f4.jpg','2017/02/13/9f749a5bf44578f4.jpg','2017-02-13 01:08:30','2017-02-12 17:08:30'),(3,'aaa','2017/02/13/c0168f814ace49cb.jpg','2017/02/13/c0168f814ace49cb.jpg','2017/02/13/c0168f814ace49cb.jpg','2017-02-13 01:08:30','2017-02-12 17:08:30'),(4,'aaa','2017/02/13/78c6338db2867cd2.jpg','2017/02/13/78c6338db2867cd2.jpg','2017/02/13/78c6338db2867cd2.jpg','2017-02-13 01:08:30','2017-02-12 17:08:30'),(5,'aaa','2017/02/13/6a38f46dccac8104.jpg','2017/02/13/6a38f46dccac8104.jpg','2017/02/13/6a38f46dccac8104.jpg','2017-02-13 01:08:30','2017-02-12 17:08:30'),(6,'aaa','2017/02/13/c0168f814ace49cb.jpg','2017/02/13/c0168f814ace49cb.jpg','2017/02/13/c0168f814ace49cb.jpg','2017-02-13 01:19:48','2017-02-12 17:19:48'),(7,'aaa','2017/02/13/78c6338db2867cd2.jpg','2017/02/13/78c6338db2867cd2.jpg','2017/02/13/78c6338db2867cd2.jpg','2017-02-13 01:19:48','2017-02-12 17:19:48'),(8,'aaa','2017/02/13/6a38f46dccac8104.jpg','2017/02/13/6a38f46dccac8104.jpg','2017/02/13/6a38f46dccac8104.jpg','2017-02-13 01:19:48','2017-02-12 17:19:48'),(9,'123','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017-02-13 01:24:37','2017-02-12 17:24:37'),(10,'123','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017-02-13 01:24:37','2017-02-12 17:24:37'),(11,'123','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017-02-13 01:38:13','2017-02-12 17:38:13'),(12,'123','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017-02-13 01:38:13','2017-02-12 17:38:13'),(13,'123','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017-02-13 01:48:08','2017-02-12 17:48:08'),(14,'123','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017-02-13 01:48:08','2017-02-12 17:48:08'),(15,'123','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017-02-13 01:51:52','2017-02-12 17:51:52'),(16,'123','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017-02-13 01:51:52','2017-02-12 17:51:52'),(17,'456','','','','2017-02-13 01:54:31','2017-02-12 17:54:31'),(18,'123','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017/02/13/2ae49198dd85a38a.jpg','2017-02-13 01:54:31','2017-02-12 17:54:31'),(19,'123','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017/02/13/6a71994f2d19a69e.jpg','2017-02-13 01:54:31','2017-02-12 17:54:31'),(20,'111','','','','2017-02-13 02:06:02','2017-02-12 18:06:02'),(21,'111','','','','2017-02-13 02:08:50','2017-02-12 18:08:50'),(22,'111','','','','2017-02-13 02:08:50','2017-02-12 18:08:50'),(23,'456','','','','2017-02-13 02:08:50','2017-02-12 18:08:50'),(24,'123','','','','2017-02-13 02:08:50','2017-02-12 18:08:50'),(25,'123','','','','2017-02-13 02:08:50','2017-02-12 18:08:50'),(26,'111','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(27,'111','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(28,'111','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(29,'111','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(30,'111','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(31,'111','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017/02/13/5207278782df259d.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50'),(32,'111','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017/02/13/5750beecc34bf2a8.jpg','2017-02-13 02:13:50','2017-02-12 18:13:50');
/*!40000 ALTER TABLE `pic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `amount` int(11) DEFAULT NULL COMMENT '交易金额，单位为分',
  `pay_type` varchar(32) DEFAULT NULL COMMENT '交易类型，比如支付宝',
  `object_type` varchar(32) NOT NULL COMMENT '交易对象类型',
  `object_id` int(11) NOT NULL COMMENT '交易对象ID，比如充值订单ID',
  `status` varchar(32) NOT NULL COMMENT '状态',
  `memo` text COMMENT '备注',
  `pay_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '支付时间',
  `out_serial_no` varchar(128) DEFAULT NULL COMMENT '外部系统交易号',
  `title` varchar(128) DEFAULT NULL COMMENT '订单标题',
  `callback` varchar(512) DEFAULT NULL COMMENT '回调地址',
  `detail` varchar(1024) DEFAULT NULL COMMENT '订单详情',
  `payment_account` varchar(128) DEFAULT NULL COMMENT '支付帐号',
  `ip` varchar(32) DEFAULT NULL,
  `origin_object_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `object_type_id` (`object_type`,`object_id`),
  KEY `origin_object_id` (`origin_object_id`),
  KEY `object_id` (`object_id`),
  KEY `pay_type` (`pay_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) NOT NULL COMMENT '手机号码',
  `passwd` varchar(45) NOT NULL COMMENT '密码md5',
  `ucode` varchar(45) NOT NULL COMMENT 'ucode',
  `nick` varchar(45) DEFAULT NULL COMMENT '昵称',
  `realname` varchar(45) DEFAULT NULL COMMENT '真实姓名',
  `birthday` datetime DEFAULT NULL COMMENT '出生日期',
  `score` int(11) NOT NULL DEFAULT '0' COMMENT '积分账户',
  `balance` int(11) NOT NULL DEFAULT '0' COMMENT '金币账户（备用）',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态,0-无效，1-有效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-13  2:18:01
