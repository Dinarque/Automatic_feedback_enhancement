# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 05:05:31 2023

@author: 3b13j
"""

import PyPDF2
import fitz
import re
import nltk
from annotation import comment

def get_composition(pdf_file, bavard = False) : 
    
    

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create an empty string to store the text
    text = ''

    # Iterate through each page in the PDF
    for page in pdf_reader.pages : 
        
        # Extract the text from the page
        page_text = page.extract_text()
        # Add the page text to the overall text string
        text += page_text
        if bavard :  print("PAGE TEXt", page_text)
    
    
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    
    # Print the extracted text
    if bavard :  
        print("here is the composition")
        print(text)
    
    
    # Close the PDF file
    #pdf_file.close()
    
    
    return text
    
    
  
def get_highlighted_text(annotation, nb_page, doc, bavard = False) :
    

    
    doc = fitz.open(doc)
    pag = doc[nb_page]
    all_words = pag.get_text("words")
   # print("all words")
    #print(all_words)
    
    if bavard :
        print(all_words)
        print()
        print(annotation)
    
    h = annotation['/Rect']
    h = fitz.Rect(h)
    
    
    sentence = [w[4] for w in all_words if   fitz.Rect(w[0:4]).intersects(h)]   
    sentence = " ".join(sentence)
    
    return sentence

### PB to access the real file 
def base_extractor(file) : 
    
    doc = fitz.open(file)
    
    highlight_text = []
# Total page in the pdf
   
# taking page for further processing

    dic = {}


    for page in doc :
   
            # list to store the co-ordinates of all highlights
        highlights = {}
        
        # loop till we have highlight annotation in the page
        annot = page.first_annot 
        
       
        while annot : 
            texte = annot.info["content"]
            
            
            if annot.type[0] == 8:
                all_coordinates = annot.vertices
                if len(all_coordinates) == 4:
                    highlight_coord = fitz.Quad(all_coordinates).rect
                    highlights[highlight_coord] = texte
                    
                else:
                    all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                    for i in range(0,len(all_coordinates)):
                        coord = fitz.Quad(all_coordinates[i]).rect
                        highlights[coord] = texte
                        
           
           
            annot = annot.next
            
          
        
        
        all_words = page.get_text("words")
        
        
        
        # List to store all the highlighted texts
        
        
        for h in highlights.keys():
        
            sentence = [w[4] for w in all_words if   fitz.Rect(w[0:4]).intersects(h)]
            texte_annot = (" ".join(sentence))
            dic[texte_annot] = highlights[h]
          
           
        
    return dic
 
def sort_dict_by_values(input_dict):
    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1]))
    return sorted_dict

def processing(path, texte, return_obj = True) :
    
    #texte = get_composition(path)  
    dick = base_extractor(path)
    
    
    """ on a besoin de trois données en parallèle pour lancer les querries : 
        le commentaire, la portion strictement délimitée, mais aussi la phrase entière.
    On va essayer de récupérer cette dernière information ici
    """
    print("teub")
    print(texte)
    
    texte = nltk.sent_tokenize(texte)
    
    high_2_sent = {}
    
    for high in dick.keys() :
        for sentence in texte : 
            if high in sentence : 
                high_2_sent[high] = sentence
                
    high_2_sent = sort_dict_by_values(high_2_sent)
   
    
    """
    nd = {} 
    
    for sent in texte :
        if sent in high_2_sent.values() :
            for key in high_2_sent.keys() :
                if high_2_sent[key] == sent :
                    nd[key] = sent 
    high_2_sent = nd
   
    
    for k in high_2_sent.keys() :
        print( "key : ",   k ,"\n", "value : ",  high_2_sent[k] , "\n" )
    """
    
    
   
    
    if  not return_obj  :
        for k in dick.keys() :
            print()
            print (k)
            print(high_2_sent[k])
            print(dick[k])
    
   
    else : 
        comments = []
        c = 0
        
        """
        for k in dick.keys() :
            com = comment(c)
            com.highlight = k 
            com.annot = dick[k]
            if k in high_2_sent.keys() : com.sentence = high_2_sent[k]
            else : com.sentence = ""
            comments.append(com)
            c += 1
        """
        
        for k in high_2_sent.keys() :
            com = comment(c)
            com.highlight = k 
            com.sentence = high_2_sent[k]
            
            
            if k in dick.keys() : com.annot = dick[k]
            else : com.annot = ""
            comments.append(com)
            c += 1
            
            
        return comments
    
def common(list1, list2) :
    
    for element in list1:
        if element in list2:
            print(element)
            
def uncommon(list1, list2) :
    
    for element in list1:
        if element not in list2:
            print(element)            
    
    
"""

PB : some stupid student do not use punctuation properly

Solution  ; utiliser un parseur d'entités nommées pour essayer de couper après les majuscules...'
"""