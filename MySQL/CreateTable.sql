CREATE DATABASE IF NOT EXISTS `cs121`;
USE cs121;

DROP TABLE IF EXISTS `position_list`;
DROP TABLE IF EXISTS `term_in_doc`;
DROP TABLE IF EXISTS `term`;
DROP TABLE IF EXISTS `doc`;

CREATE TABLE `term` (
	`id` int NOT NULL AUTO_INCREMENT UNIQUE,
	`name` varchar(50) NOT NULL UNIQUE,
    `total_frequency` int DEFAULT 1, 
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10101 DEFAULT CHARSET=latin1;

 CREATE TABLE `doc` (
	`id` int NOT NULL AUTO_INCREMENT UNIQUE,
	`name` varchar(10) NOT NULL UNIQUE,
    `url` varchar(200) DEFAULT NULL,
    `total_terms` int DEFAULT NULL, 
	PRIMARY KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `term_in_doc` (
	`doc_id` int NOT NULL,
	`term_id` int NOT NULL,
    `frequency` int DEFAULT 0, 
    `tf-idf` varchar(25)  DEFAULT NULL, 
    `meta_frequency` int DEFAULT 0, 
	PRIMARY KEY (`doc_id`, `term_id`),
	CONSTRAINT `term_doc_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `doc` (`id`) ON DELETE CASCADE,
	CONSTRAINT `term_doc_ibfk_2` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `position_list` (
	`id` int NOT NULL AUTO_INCREMENT UNIQUE,
	`doc_id` int NOT NULL,
	`term_id` int NOT NULL,
    `position` int NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `position_list_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `term_in_doc` (`doc_id`) ON DELETE CASCADE,
	CONSTRAINT `position_list_ibfk_2` FOREIGN KEY (`term_id`) REFERENCES `term_in_doc` (`term_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


