"""
Created on Mon Apr  3 05:05:31 2023

@author: 3b13j
"""
import streamlit as st

import PyPDF2
import fitz
import re
import nltk
nltk.download('punkt')
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
    
    
    return text.replace("   ", " ")
    
    

def base_extractor(path, texte) : 
    
     

    
    
    dic = {}
    date = {}
    pdf_document = fitz.open(path)

    # trouver texte annoté et contenu de l'annotation 
    for page_n in range(pdf_document.page_count):
        page = pdf_document.load_page(page_n)
        all_words = page.get_text("words")
        page_annotations = page.annots()

        # Get all words on the current page
      

        # Iterate through annotations on the current page
        for annot in page_annotations:
           all_coordinates = annot.vertices
           try : 
               if len(all_coordinates) == 4:
                   highlight_coord = fitz.Quad(all_coordinates).rect
               sentence = [w[4] for w in all_words if   fitz.Rect(w[0:4]).intersects(highlight_coord)]
               highlight = (" ".join(sentence))
               highlight = highlight.rsplit(".")[0]
               content = annot.info.get("content", "")
               dic[highlight] = content
               date[highlight] = annot.info["creationDate"]
           except : print("sorry Lindsay")
    date = sort_dict_by_values(date)
    
    sents = nltk.sent_tokenize(texte)
    st.session_state.highlight = list(date.keys())
    #st.session_state.texte = sents
    matrix  = {}
    for h in st.session_state.highlight :
        matrix[h] = []
        for sent in sents : 
            if  h in sent : matrix [h].append(sent) 
            
            else :  matrix[h].append (h in sent)
    #st.session_state.matrix= matrix 
    
    high_2_sent = {}
    for h in matrix.keys() :
        high_2_sent[h] = []
        for el in matrix[h] : 
            if el != False :
                high_2_sent[h].append(el)
                
    #st.session_state.high_2_sent = high_2_sent
    ## idée ; faire sur nombre d annot avec texte fouillé décroissant. pour ce faire matrice stocke liste de True, et on prend le premier 
    
    
    """
    
  
    c = 0 
    for sent in texte :
        for high in st.session_state.highlights :
            if high in sent :
                com = comment(c)
                com.sentence = sent
                com.highlight = high
                com.annot = dic[high]
    
    """
    #st.session_state.sentence=[]
    c = 0
    
    try : 
        sent_considered = sents[0]
        idx = sents.index( sent_considered )
        chunks = []
        for h in st.session_state.highlight :
            com = comment(c)
            cand = candide(high_2_sent[h])
           
            candidats =  [ el for el in  high_2_sent[h] if sents.index( el) >= idx ]
            if len(candidats) != 0 :
                    senten = candidats[0]
                    sent_considered = senten 
                    idx = sents.index( sent_considered )
            else : 
                if len(cand) == 1 : senten = cand[0]
                else : 
                    senten = "oopsie"
            com.sentence = senten
            #st.session_state.sentence.append(senten)
            com.highlight = h
            com.annot = dic[h]
            c+=1
            if com.annot != "" : chunks.append(com)
        return chunks
    except : return []
 
def sort_dict_by_values(input_dict):
    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1]))
    return sorted_dict


def find_sentences_with_string(sent, text):
    
    st.session_state.depression = []
    texte = text.replace(".", "")
    texte = texte.replace("?", "")
    texte = texte.replace("!", "")
    
    for s in sent  : 
        
        if str(texte) in str(sent) : 
            return s
     
    
    
    
    return "Oupsie"


def candide(liste) : return [el for el in liste if el != False]