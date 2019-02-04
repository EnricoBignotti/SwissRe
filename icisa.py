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
    return int(left)/433

#sorts the lines within the page
def sortLines(page):
    lineList = list(page)
    lineList.sort(key=lambda x: (sortColumn(x.attributes['left'].value), int(x.attributes['top'].value)))
    return lineList

#define a dedicated function for finding synonyms
def find_synonim(ontology, name):
    cleaned_name = name.upper().replace('.', '').strip()
    if not ontology.has_key(cleaned_name):
        if '(' in cleaned_name:
            segments = cleaned_name.split('(')
            synonims = []
            for par in range(1, len(segments)):
                synonims = synonims + segments[par].replace(')', '').split(',')
            #this is to remove the cases of synonyms that in the description are within parentheses
            for s in synonims:
                if ontology.has_key(s.strip()):
                    return s.strip()
        out = re.sub(r'\([^)]*\)', '', cleaned_name).replace('  ',' ')
        if ontology.has_key(out):
            return out
        else:
            return difflib.get_close_matches(cleaned_name, ontology.keys(),1,0)[0]
    else:
        return cleaned_name

#parse the xml
xmldoc = minidom.parse('icisa.xml')
pages = xmldoc.getElementsByTagName('page')
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
            if line.attributes['font'].value == '10' and line.attributes['height'].value == '17' and className != "":
                icisa.add_annotation(className, "rdfs:comment", message, lang='de')
                message = ""
            if line.attributes['font'].value == '10' and line.attributes['height'].value == '17':
                className = find_synonim(icisa.ontology, line.firstChild.firstChild.nodeValue)
            if line.attributes['font'].value == '14' and line.attributes['height'].value == '17' and className != "":
                icisa.add_annotation(className, 'rdfs:label', line.firstChild.firstChild.nodeValue, 'de')
                icisa.add_annotation(className, "rdfs:comment", message, lang='en')
                message = ""
            if line.attributes['font'].value in ['11', '15'] and line.attributes['height'].value == '18':
                message += line.firstChild.nodeValue

print icisa.to_turtle()

