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
        if bavard :  print("PAGE TEXT", page_text)
    
    
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    
    # Print the extracted text
    if bavard :  
        print("here is the composition")
        print(text)
    
    
    # Close the PDF file
    #pdf_file.close()
    
    
    return text.replace("   ", " ")
    
    

    
def base_extractor(pdf_file, texte):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    # Initialize an empty list to store highlighted text
    highlights = []
    matrix = {}
    sents = nltk.sent_tokenize(texte)
    
    # Iterate through each page of the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        
        # Get the annotations (including highlights) on the page
        annotations = page.annots()

        # Get the words on the page
        words = page.get_text("words")

        sentences = nltk.sent_tokenize(page.get_text())
        
        
        thresh = 0
        for annotation in annotations:
            
            
                highlight = ""
                closest_sentence = None
                closest_distance = float('inf')
                for word in words:
                    if annotation.rect.intersects(word[:4]):
                        highlight += word[4] +" "
              
                candidates = []
                for sentence in sentences:
                    if highlight in sentence or sentence in highlight:
                        candidates.append(sentence)
                        
                if len(candidates) == 1 : final_sentence = candidates[0]
                else :
                    indexes = [ sentences.index(sent) for sent in candidates ]
                    final_i = min([x] for x in indexes if x >= thresh)
                    final_sentence = sentences [final_i]
                thresh = sentences.index(final_sentence)
                        
                highlights.append([highlight, final_sentence, annotation.info.get("content", "")])

    chunks = []
    for c in range(len(highlights)) :
        com = comment(c)
        com.highlight = highlights[c][0]
        com.sentence =  highlights[c][1]
        com.annot =  highlights[c][2]
        chunks.append(com)
    return chunks

"""
        # Iterate through the annotations on the page
        for annotation in annotations:
            content = annotation.info.get("content", "")
            highlight = ""
            if annotation.type[0] == 8:  # 8 corresponds to "Highlight" annotation type
                for word in words:
                    if annotation.rect.intersects(word[:4]):
                        highlight += word[4] +" "
                        
            highlights.append([highlight, content])

"""
    
 
    
   

    
 
    
 
    
 
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