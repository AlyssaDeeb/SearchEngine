USE mydb;

DROP TABLE IF EXISTS term_in_doc_temp;

CREATE TABLE `term_in_doc_temp` (
  `doc_id` int(11) NOT NULL,
  `term_id` int(11) NOT NULL,
  `frequency` int(11) DEFAULT '0',
  `tf-idf` varchar(25) DEFAULT NULL,
  `meta_frequency` int(11) DEFAULT '0',
  `weighted_tf-idf` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`doc_id`,`term_id`),
  KEY `term_doc2_ibfk_2` (`term_id`),
  CONSTRAINT `term_doc2_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `doc` (`id`) ON DELETE CASCADE,
  CONSTRAINT `term_doc2_ibfk_2` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

# insert the content of term_in_doc along with the caculation for weighted tf-idf into the temp table
INSERT INTO term_in_doc_temp (doc_id, term_id, frequency, `tf-idf`, meta_frequency, `weighted_tf-idf`)  
  (SELECT term_in_doc.doc_id, term_in_doc.term_id, term_in_doc.frequency, term_in_doc.`tf-idf`, 
  term_in_doc.meta_frequency,
  # sum of tf-idf, 2*normalized reference count, 1.5 (offsets negative tf-idfs), 
  # fraction of term's occurances in meta
  (term_in_doc.`tf-idf` + 2*doc.references/(SELECT MAX(doc.references) FROM doc) + 
        1.5 + term_in_doc.meta_frequency/(term_in_doc.meta_frequency + doc.total_terms))
      
		FROM doc
       
		JOIN term_in_doc ON doc.id = term_in_doc.doc_id
		JOIN term ON term.id = term_in_doc.term_id );

# clear out the contents of term_in_doc and add column for weighted tf-idf
TRUNCATE term_in_doc;
ALTER TABLE term_in_doc ADD `weighted_tf-idf` varchar(25) DEFAULT NULL;

# add everything from temp table to term_in_doc
INSERT INTO term_in_doc (doc_id, term_id, frequency, `tf-idf`, meta_frequency, `weighted_tf-idf`) SELECT * FROM term_in_doc_temp;

# delete the temp table
DROP TABLE term_in_doc_temp;
