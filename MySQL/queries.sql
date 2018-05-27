USE searchengine;

#OR SELECT

#SELECT d.name, d.url, `weighted_tf-idf` FROM doc d
#	INNER JOIN term_in_doc td on d.id = td.doc_id 
#	INNER JOIN term t on t.id = td.term_id 
#  WHERE t.name = "alyssa" OR t.name = "horizons" order by `weighted_tf-idf` desc LIMIT 100;
    
#AND SELECT   
 
SELECT doc.name, doc.url FROM doc WHERE doc.id IN
	(SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term 
    WHERE term.name = "computer" AND term_in_doc.term_id = term.id)
    AND doc.id IN 
    (SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term 
    WHERE term.name = "science" AND term_in_doc.term_id = term.id)
    ORDER BY ((SELECT `tf-idf` from term_in_doc, term WHERE doc_id = doc.id
    AND term.name = "computer" AND term_in_doc.term_id = term.id) + 
    (SELECT `tf-idf` from term_in_doc, term WHERE doc_id = doc.id
    AND term.name = "science" AND term_in_doc.term_id = term.id)) ASC;

#POSITION SELECT    

#SELECT position FROM position_list WHERE doc_id = (
#	SELECT id FROM doc WHERE doc.name = "26/447") 
#    AND term_id = (
#    SELECT id FROM term WHERE term.name = "alyssa")


