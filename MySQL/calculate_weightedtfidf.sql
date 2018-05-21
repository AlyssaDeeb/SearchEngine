(select term_in_doc.term_id, term_in_doc.doc_id, (term_in_doc.`tf-idf` + 2*doc.references/(select max(doc.references) from doc) + 
        1.5 + term_in_doc.meta_frequency/(term_in_doc.meta_frequency + doc.total_terms)) as result
       
		from doc
       
		join term_in_doc on doc.id = term_in_doc.doc_id
		join term on term.id = term_in_doc.term_id )