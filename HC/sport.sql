/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1_3306
Source Server Version : 50562
Source Host           : 127.0.0.1:3306
Source Database       : sport

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2020-10-17 01:52:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for athletic_test
-- ----------------------------
DROP TABLE IF EXISTS `athletic_test`;
CREATE TABLE `athletic_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(32) NOT NULL,
  `st_ID` varchar(32) NOT NULL,
  `st_push_up` int(11) NOT NULL,
  `st_plank` float NOT NULL,
  `st_Pro_Agility` float NOT NULL,
  `st_suppleness` float NOT NULL,
  `run_20m` float NOT NULL,
  `st_Vertical_Jump` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of athletic_test
-- ----------------------------

-- ----------------------------
-- Table structure for physical_test
-- ----------------------------
DROP TABLE IF EXISTS `physical_test`;
CREATE TABLE `physical_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(32) NOT NULL,
  `st_ID` varchar(32) NOT NULL,
  `st_stature` float NOT NULL,
  `st_weight` float NOT NULL,
  `st_grade` varchar(32) NOT NULL,
  `st_age` int(11) NOT NULL,
  `st_sex` varchar(32) NOT NULL,
  `st_position` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of physical_test
-- ----------------------------

-- ----------------------------
-- Table structure for rugby_test
-- ----------------------------
DROP TABLE IF EXISTS `rugby_test`;
CREATE TABLE `rugby_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(32) NOT NULL,
  `st_ID` varchar(32) NOT NULL,
  `st_40yards_dash` float NOT NULL,
  `st_bench_press` int(11) NOT NULL,
  `st_vertical_jump` float NOT NULL,
  `st_long_jump` float NOT NULL,
  `st_20yards_toandfrom` float NOT NULL,
  `st_5yards_L` float NOT NULL,
  `st_60yards_toandfrom` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rugby_test
-- ----------------------------

-- ----------------------------
-- Table structure for standard_score
-- ----------------------------
DROP TABLE IF EXISTS `standard_score`;
CREATE TABLE `standard_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age_group` varchar(32) NOT NULL,
  `push_up` int(11) NOT NULL,
  `plank` float NOT NULL,
  `standing_leap` float NOT NULL,
  `run_20m` float NOT NULL,
  `Pro_Agility` float NOT NULL,
  `T_test` float NOT NULL,
  `Vertical_Jump` float NOT NULL,
  `suppleness` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of standard_score
-- ----------------------------

-- ----------------------------
-- Table structure for student_info
-- ----------------------------
DROP TABLE IF EXISTS `student_info`;
CREATE TABLE `student_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(32) NOT NULL,
  `st_ID` varchar(32) NOT NULL,
  `st_Tel` varchar(32) NOT NULL,
  `st_age` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student_info
-- ----------------------------
INSERT INTO `student_info` VALUES ('1', '刘振龙', '000001', '15263692675', '21');
INSERT INTO `student_info` VALUES ('2', '王乐之', '000002', '187526555555', '20');

-- ----------------------------
-- Table structure for student_score
-- ----------------------------
DROP TABLE IF EXISTS `student_score`;
CREATE TABLE `student_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(32) NOT NULL,
  `st_ID` varchar(32) NOT NULL,
  `test_time` datetime DEFAULT NULL,
  `st_age` int(11) NOT NULL,
  `push_up` int(11) NOT NULL,
  `plank` float NOT NULL,
  `standing_leap` float NOT NULL,
  `run_20m` float NOT NULL,
  `Pro_Agility` float NOT NULL,
  `T_test` float NOT NULL,
  `Vertical_Jump` float NOT NULL,
  `suppleness` float NOT NULL,
  `age_group` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student_score
-- ----------------------------
