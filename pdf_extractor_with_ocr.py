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
# Main PB : get the annotated higlihht and the sentence its been extracted from 
# annot.info.content to get the content of the message

def deal_with_annotation(path) :
    pdf_document = fitz.open(path)
    chunks = []
    
    index = 0
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text = page.get_text()
        annotations = page.annots()
        words = page.get_text("words")
        
      
        sentences = nltk.sent_tokenize(page.get_text())
        sentences = [s.replace("\n", "") for s in sentences]
            
        
        sent_to_words = sentences_to_coord(sentences, words)
        
        highlights = []
        for annot in annotations: 
            
            
            com = comment(index)
            index += 1 
            com.highlight = get_highlight(words, annot)
            com.sentence =  assign_sentence(sentences,com.highlight, annot, sent_to_words )
            com.annot =   annot.info.get("content", "")
            chunks.append(com)
            
   
    return  chunks

def sentences_to_coord(sentences, words):
    sent_to_words = {}
    i = 0
    for sent in sentences  :
        members = []
        for wd in sent.split(" ") :
            members.append(words[i])
            i += 1
        sent_to_words[sent] = members
        
    return sent_to_words

def pick(annot, candidates, sent_to_words) :
    means = {}
    score = {}
    gold = set(annot.rect)
    for sent in candidates : 
        means[sent] = term_by_term_mean( [x[0:4] for x in sent_to_words[sent]])
        score[sent] = rectangle_similarity(gold, means[sent])
        
    return  max(score, key=lambda k: score[k])


    
def rectangle_similarity(rect1_coords, rect2_coords):
    # Convert the rectangles to sets of coordinates

    # Calculate the intersection area
    intersection = rect1_coords.intersection(rect2_coords)
    intersection_area = len(intersection)

    # Calculate the union area
    union_area = len(rect1_coords) + len(rect2_coords) - intersection_area

    # Calculate the Jaccard similarity
    jaccard_similarity = intersection_area / union_area

    return jaccard_similarity
    
def term_by_term_mean(list_of_lists):
    if not list_of_lists:
        return None  # Handle empty input list

    num_lists = len(list_of_lists)
    num_elements = len(list_of_lists[0])  # Assuming all inner lists have the same length

    # Initialize a list to store the means
    means = [0] * num_elements

    # Calculate the sum of each element across all lists
    for sublist in list_of_lists:
        for i in range(num_elements):
            means[i] += sublist[i]

    # Divide the sum by the number of lists to get the mean
    for i in range(num_elements):
        means[i] /= num_lists

    return means
    

def assign_sentence(sentences, highlight, annot, sent_to_words, recurse = True) :
    
    candidates = [sent for sent in sentences if highlight in sent]
    if len(candidates) == 1 : return candidates [0]
    
    elif len(candidates) > 1 :
        return pick (annot,candidates, sent_to_words)

    
    elif recurse == True : 
        # the highlight is bigger than a sentence 
        sub_highs = nltk.sent_tokenize(highlight)
        for D in sentences : print(D)
        print("SUBS" , sub_highs)
        
        subsentences = []
        for sub in sub_highs : 
            subsentences.append( assign_sentence(sentences, sub, annot, sent_to_words, False) )
        
        print("SUBS SELECTEs", subsentences)
        return " ".join(set(subsentences))
        
    else : return ""
    
    

def get_highlight(words, annot) : 
    if annot.vertices == None : return None 
    content = []  
    if len(annot.vertices) == 4:
        highlight_coord = fitz.Quad(annot.vertices).rect
    else : 
        highlight_coord = annot.rect
        
    for wd in words :
        if fitz.Rect(wd[0:4]).intersects(highlight_coord):
                content.append(wd[4])           
    content = " ".join(content)
    
    return content 
    
    
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
        sentences = [  s.replace ("\n", " ") for s in sentences  ]
        
        
        thresh = 0
        for annotation in annotations:
            
            
                try :
                    all_coordinates = annotation.vertices
                    if len(all_coordinates) == 4:
                        highlight_coord = fitz.Quad(all_coordinates).rect
                    highlight = [w[4] for w in words if   fitz.Rect(w[0:4]).intersects(highlight_coord)]
                    highlight = " ".join(highlight)
                except : 
                    highlight = ""
                    for word in words:
                        if annotation.rect.intersects(word[:4]):
                            highlight += word[4] +" "
                closest_sentence = None
                closest_distance = float('inf')
                for word in words:
                    if annotation.rect.intersects(word[:4]):
                        highlight += word[4] +" "
              
                candidates = []
                for sentence in sentences:
                    if highlight in sentence :
                        candidates.append(sentence)
                print(".....")
                print(sentences)
                print(highlight)
                print(candidates)
                if len(candidates) == 0 :
                    final_sentence = highlight
                    
                    for sentence in sentences : 
                        if highlight in sentence :
                            i = sentences.index(sentence)
                            try : final_sentence = sentences[i -1] + final_sentence 
                            except :  print("fail")
                            final_sentence = unite_coinciding_strings(sentence, final_sentence)
                        
                        
                elif len(candidates) == 1 : 
                    final_sentence = candidates[0]
                    thresh = sentences.index(final_sentence)
                else :
                    
                    indexes = [ sentences.index(sent) for sent in candidates ]
                    
                    try : 
                        cand = [c for c in indexes if c >= thresh]
                        final_i = min(cand)
                        final_sentence = sentences [final_i]
                    except : 
                        final_sentnce = candidates[0]
                    
                    try: thresh = sentences.index(final_sentence)
                    except :  print("modif failed")
                
                highlights.append([highlight, final_sentence, annotation.info.get("content", "")])

    chunks = []
    for i in range(len(highlights)) :
        
        com = comment(i)
        com.highlight = highlights[i][0]
        com.sentence =  highlights[i][1]
        com.annot =  highlights[i][2]
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
    
 
    
def unite_coinciding_strings(string1, string2):
    # Find the common substring
    common_substring = ""
    for i in range(len(string1)):
        for j in range(len(string2)):
            k = 0
            while i + k < len(string1) and j + k < len(string2) and string1[i + k] == string2[j + k]:
                k += 1
            if k > len(common_substring):
                common_substring = string1[i:i + k]

    if common_substring:
        # Combine the strings where they coincide
        result = string1 + string2[len(common_substring):]
        return result
    else:
        # If there's no common substring, simply concatenate the two strings
        return string1 + string2

    
 
    
 
    
 
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