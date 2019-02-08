#-*- encoding: utf-8 -*-
from xml.dom import minidom
#import for regular expressions and comparing files
import re
import difflib
#import dedicated library for automatically build the .owl file
from TurtleOWL import *
import operator
#extracts the column from its coordinates
def sortColumn(left):
    return int(left)//433
#checks if colums 0 or 1, 433 is based on pdf and checking how many pixels con l' applicazione crosshair da pdf

#sorts the lines within the page
def sortLines(page):
    lineList = list(page)
    lineList.sort(key=lambda x: (sortColumn(x.attributes['left'].value), int(x.attributes['top'].value)))
    return lineList
#difatto xml ha un tag che si chiama text. sort però non volgio l'alfabetico, voglio sortarli per attributi. key è la chiave
#define a dedicated function for finding synonyms si basa sui tag left e top per iniziare, primo valore il numero della colonna e secondo valore con la distaza dall'alto 
#classe element, attributes è un attr, name, local name, prefix è int perché è stored in string sorta il primo elemeto e poi il secondo indice
def find_synonim(ontology, name):
    cleaned_name = name.upper().replace('.', '').strip()
    if not ontology.has_key(cleaned_name):
        if '(' in cleaned_name:
            segments = cleaned_name.split('(')
            synonims = []
            for par in range(1, len(segments)):
                synonims = synonims + segments[par].replace(')', '').split(',')
                #crea una lista di liste di tutte le parole in mezzo  alle parentesij
            #this is to remove the cases of synonyms that in the description are within parentheses
            for s in synonims:
                if ontology.has_key(s.strip()):
                    return s.strip()
        out = re.sub(r'\([^)]*\)', '', cleaned_name).replace('  ',' ')
        #range di caratteri tutti quelli non ) cancello tutti i caratteri tra le due parentesi
        if ontology.has_key(out):
            return out
        else:
            return difflib.get_close_matches(cleaned_name, ontology.keys(),1,0)[0]
        #return only one not 3, il cutoff è la possibilità  ma non scartrlo perché deve esserci una roba quantomeno simile, se non la trovi
        #prendi la cosa più simile
    else:
        return cleaned_name

#parse the xml
xmldoc = minidom.parse('icisa.xml')
pages = xmldoc.getElementsByTagName('page')
#iterable non è una lista
#define the owl ontology
icisa = TurtleOWL("http://www.semanticweb.org/it.enricobignotti/ICISA")

#declare the superclass as the most general classes, message being the content, and className being the name of the class
superclass = ''
message = ""
className = ""

#go through the english index
for index, page in enumerate(pages):
    if index >= 3 and index <= 8:
        for line in sortLines(page.getElementsByTagName('text')):
            if line.attributes['font'].value == '10' and line.attributes['height'].value == '17':
                superclass = line.firstChild.firstChild.nodeValue
                #<text top="305" left="53" width="136" height="17" font="10"><b>Insurable debtors</b></text> primo first prende b secondo il testo che poi prende nodevalue
                #reach all the the way to text
                #create the superclass removing spaces and putting uppercase and then create the rdfs:label to name the class
                icisa.add_class(superclass.strip().upper())
                icisa.add_annotation(superclass.strip().upper(), "rdfs:label", superclass, lang="en")
            if line.attributes['font'].value == '11' and line.attributes['height'].value == '18':
                name = line.firstChild.nodeValue.split(". .")[0]
                 #create the subclasses removing points and putting uppercase and then create the rdfs:label to name the subclasses and structuring them
                icisa.add_class(name.strip().upper(), superclass.strip().upper())
                icisa.add_annotation(name.strip().upper(), "rdfs:label", name, lang="en")
                
    #cicle trough the rest of the file where the descriptions are 
    if index >= 15 and index <= 51:

        #for each line, I check its position and depending on whether it is, I add it as a comment, specifying the language or as a lable of the class 
        for line in sortLines(page.getElementsByTagName('text')):
            if line.attributes['font'].value == '10' and line.attributes['height'].value == '17':
                className = find_synonim(icisa.ontology, line.firstChild.firstChild.nodeValue)
            if line.attributes['font'].value in ['11', '15'] and line.attributes['height'].value == '18':
                message += line.firstChild.nodeValue
            if line.attributes['font'].value == '14' and line.attributes['height'].value == '17' and className != "":
                icisa.add_annotation(className, 'rdfs:label', line.firstChild.firstChild.nodeValue, 'de')
                icisa.add_annotation(className, "rdfs:comment", message, lang='en')
                message = ""
                #guardo attraverso il testo il rpimo che trovo con valore è in en oppure in de
            if line.attributes['font'].value == '10' and line.attributes['height'].value == '17' and className != "":
                icisa.add_annotation(className, "rdfs:comment", message, lang='de')
                message = ""
                #evitato elif per non essere esclusivi, agiscono tutti insieme 3 e 4 uno per linea, se entri in uno
           
            

print(icisa.to_turtle())

