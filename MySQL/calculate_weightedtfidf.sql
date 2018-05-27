use searchengine;

UPDATE term_in_doc SET `weighted_tf-idf` = 
	(`tf-idf` + 2 * (SELECT doc.references FROM doc 
	WHERE doc.id = term_in_doc.doc_id)/(SELECT MAX(doc.references) FROM doc) + 
        1.5 + term_in_doc.meta_frequency/(term_in_doc.meta_frequency + 
        (SELECT doc.total_terms from doc WHERE doc.id = term_in_doc.doc_id)));