# viaf-dbpedia-reconciliation-python
These Python scripts reconciles personal and corporate names against the Virtual International Authority File (VIAF) and DBpedia, a linked data version of Wikipedia. The scripts retrieve the name and URI of the most relevant match for each name searched. To help assess the quality of the matches, these scripts use the [FuzzyWuzzy](http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/) Python library to compare the name that was searched to the name that was retrieved.

While these automated searches are efficient, they are rarely 100% accurate so the results of this script always require manual review. For example, when searching for "University of Portland," the viafReconciliationCorporate.py script returns "University of Maine. School of Law" and the viafReconciliationCorporate.py script returns "Portland State University."

##Sample Files

####[organizations.txt](organizations.txt)
A sample list of organizations that can be used with [dbpediaReconciliationCorporate.py](dbpediaReconciliationCorporate.py) and [viafReconciliationCorporate.py](viafReconciliationCorporate.py)

####[people.txt](people.txt)
A sample list of people that can be used with [dbpediaReconciliationPeople.py](dbpediaReconciliationPeople.py) and [viafReconciliationPeople.py](viafReconciliationPeople.py)

##Scripts

####[dbpediaReconciliationCorporate.py](dbpediaReconciliationCorporate.py)

####[dbpediaReconciliationPeople.py](dbpediaReconciliationPeople.py)	

####[viafReconciliationCorporate.py](viafReconciliationCorporate.py)
This script uses VIAF's "corporateNames" index and retrieves VIAF, Library of Congress, and International Standard Name Identifier (ISNI) URIs for each potential match.

####[viafReconciliationPeople.py](viafReconciliationPeople.py)
This script uses VIAF's "personalNames" index and retrieves URIs from VIAF, Library of Congress, and International Standard Name Identifier (ISNI) for each potential match.
