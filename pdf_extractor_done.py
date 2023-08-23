# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 05:05:31 2023

@author: 3b13j
"""
import streamlit as st

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
    
    

def base_extractor(path) : 
    
    
    

        
    
    
    chunks = {}

    pdf_document = fitz.open(path)

    for page_n in range(pdf_document.page_count):
        page = pdf_document.load_page(page_n)
        page_annotations = page.annots()

        # Get all words on the current page
        words = page.get_text("words")

        # Iterate through annotations on the current page
        for annot in page_annotations:
            
            rect = annot.rect
            words_under_annot = [word for word in words if fitz.Rect(word[:4]).intersects(rect)]
            highlight = " ".join(word[4] for word in words_under_annot)

            # Extract the content of other annotations if available
           
            content = annot.info.get("content", "")

          

            chunks[highlight] = content

  
   
    return chunks
 
def sort_dict_by_values(input_dict):
    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1]))
    return sorted_dict


    
def common(list1, list2) :
    
    for element in list1:
        if element in list2:
            print(element)
            
def uncommon(list1, list2) :
    
    for element in list1:
        if element not in list2:
            print(element)            
    
