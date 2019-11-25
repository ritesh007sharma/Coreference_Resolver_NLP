Team members: Ritesh Sharma, Mark Wolfson

------------------ LIBRARIES ---------------------
Used library Spacy, which can be found at https://spacy.io/

-------------------- USE -------------------------
Please install spacy by executing (pip install spacy) 
And run the program in Anaconda Navigator by uncommenting file name.

You may also need to download the "en_core_web_md" model using
python -m spacy download en_core_web_md

----------------------OR-------------------------- 

run the program on local machine by installing spacy.

To run the program:

	python3 coref.py <ListFile> <ResponseDir>

For example:

	python3 coref test1.listfile /home/yourname/project/coref/output/

----------------------OR---------------------------

run the following command to run the code in virtual environment:

from the root directory:

python3.6 -m venv venv
source venv/bin/activate
pip install spacy
python -m spacy download en_core_web_md

To run the program:

	python3 coref.py <ListFile> <ResponseDir>

For example:

	python3 coref test1.listfile /home/yourname/project/coref/output/


Note: if any problems are encountered. Please email u1120289@utah.edu

------------------ TIME ESTIMATE -----------------
Time Estimate for tst1 document:
Approximately 30 seconds.

---------------- Contributions -------------------
Ritesh:
    File IO
    Parsing
    Head noun to coref comparison
    Word similarity comparisons

Mark:
    Parsing(Tried parsing did not work eventually used Ritesh parsing function.)
    Named Entity Recognition.
  
---------------- KNOWN ISSUES --------------------
None