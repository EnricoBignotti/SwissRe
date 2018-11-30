README

included:

-icisa.owl: the ICISA ontology
-icisa.py: the script for extracting the information and then build the ontology
-icisa.xml: the .xml version of the ICISA_DE.pdf source 
-TurtleOWL.py: a dedicated library for automatically create .owl files in Turtle format 

#ICISA

My strategy was as follows:

1) I read the file to understand its structure, and I noted that the index gave me a shallow hierarchical structure of the terms and that the terms' description followed the same order throughout, i.e., english then german.
2) I decided the strategy would be first to create the classes hierarchy by looking at the index, where the more general domain has a set of more specific domains then to add the bilingual description and german label by extracting the information there
3) I opted for converting the pdf into .xml at https://www.freefileconvert.com/pdf-xml, hoping that the tags could give me some hints for the structure to obtain the information. Another option would have been to use pdfminer.
4) I understood how to exploit the position of in the page and font of the words to distinguish english from german description and the position in the index
5) I  first obtained the shallow taxonomy from the english index only, since merging the german index was too complicated, by defining the classes and their subclasses 
6) I clicled through the parts of the document with descriptions and added them as rdfs:comment and then took the german name and added it as a rdfs:label
7) The automatic creation of the ontology was obtained via a TurtleOWL.py, a dedicated library for automatically create .owl files in Turtle format, which provides a simpler strcuture to manipulate and inputting the language information. If I used any other syntax, I would have had to change the structure of the tag
8) The final output is an ontology in Turtle format, that can be opened using Protègè or similar visualization tools


What next?

I see the following improvements:

1) Actually using other "semantic" sources, such as DBpedia, GoodRelations or schema.org, to enrich the general terms especially.
2) Fix some issues with the automatic labelling and commenting of the classes
