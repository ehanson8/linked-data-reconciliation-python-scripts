# VIAF and DBpedia Reconciliation Python Scripts
These Python scripts reconcile personal and corporate names against the Virtual International Authority File (VIAF) and DBpedia, a linked data version of Wikipedia. The scripts retrieve the name and URI of the most relevant match for each name searched. To help assess the quality of the matches, these scripts use the [FuzzyWuzzy](http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/) Python library to compare the name that was searched to the name that was retrieved.

While these automated searches are efficient, they are rarely 100% accurate so the results of this script always require manual review. For example, when searching for "University of Portland," the viafReconciliationCorporate.py script returns "University of Maine. School of Law" and the dbpediaReconciliationCorporate.py script returns "Portland State University."

## Sample Files

#### [organizations.csv](organizations.csv)
A sample list of organizations that can be used with [dbpediaReconciliationCorporate.py](dbpediaReconciliationCorporate.py) and [viafReconciliationCorporate.py](viafReconciliationCorporate.py)

#### [people.csv](people.csv)
A sample list of people that can be used with [dbpediaReconciliationPeople.py](dbpediaReconciliationPeople.py) and [viafReconciliationPeople.py](viafReconciliationPeople.py)

## Scripts

#### [dbpediaReconciliationCorporate.py](dbpediaReconciliationCorporate.py)
This script searches DBpedia records with the class of "Organisation."

#### [dbpediaReconciliationGeneral.py](dbpediaReconciliationGeneral.py)
This script searches DBpedia records without specifiying a class. By not specifying a class, this script tends to be less accurate than [dbpediaReconciliationPeople.py](dbpediaReconciliationPeople.py) or [dbpediaReconciliationCorporate.py](dbpediaReconciliationCorporate.py), but it could be used for a list that contains both personal and corporate names.

#### [dbpediaReconciliationPeople.py](dbpediaReconciliationPeople.py)	
This script searches DBpedia records with the class of "Person." Given that DBpedia stores personal names in direct order ("George Washington") and most name headings in library and archival data are stored in indirect order ("Washington, George"), this script creates a "searchDirectOrder" column that places the name in direct order based on the placement of the first comma.  The script then compares the retrieved DBpedia name to the "searchDirectOrder" column rather than the "search" column. If there is only one name in "search" column (e.g. "Voltaire," "Prince"), the script will place "N/A" in the "searchDirectOrder" column and compares the retrieved DBpedia name to the original "search" column rather the "searchDirectOrder" column.

#### [viafReconciliationCorporate.py](viafReconciliationCorporate.py)
This script uses VIAF's "corporateNames" index and retrieves VIAF, Library of Congress, and International Standard Name Identifier (ISNI) URIs for each potential match.

#### [viafReconciliationPeople.py](viafReconciliationPeople.py)
This script uses VIAF's "personalNames" index and retrieves VIAF, Library of Congress, and International Standard Name Identifier (ISNI) URIs for each potential match.
