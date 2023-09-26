# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 09:03:18 2023

@author: 3b13j
"""
"""
# Code mostly inspired by https://medium.com/social-impact-analytics/extract-text-from-unsearchable-pdfs-for-data-analysis-using-python-a6a2ca0866dd

import cv2
import pytesseract
import os
import numpy as np
import pandas as pd
import re
from pdf2image import convert_from_bytes

# Some help functions 
def get_conf(page_gray):
    '''return a average confidence value of OCR result '''
    df = pytesseract.image_to_data(page_gray,output_type='data.frame')
    df.drop(df[df.conf==-1].index.values,inplace=True)
    df.reset_index()
    return df.conf.mean()
  
def deskew(image):
    '''deskew the image'''
    gray = cv2.bitwise_not(image)
    temp_arr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(temp_arr > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated
  


def ocr(file) : 

    # convert pdf into image
    pdf_file = convert_from_bytes(open(os.path.join(file), 'rb').read())
    # create a df to save each pdf's text
    pages_df = pd.DataFrame(columns=['conf','text'])
    for (i,page) in enumerate(pdf_file) :
        try:
            # transfer image of pdf_file into array
            page_arr = np.asarray(page)
            # transfer into grayscale
            page_arr_gray = cv2.cvtColor(page_arr,cv2.COLOR_BGR2GRAY)
            # deskew the page
            page_deskew = deskew(page_arr_gray)
            # cal confidence value
            page_conf = get_conf(page_deskew)
            # extract string 
            pages_df = pages_df.append({'conf': page_conf,'text': pytesseract.image_to_string(page_deskew)}, ignore_index=True)
        except:
            # if can't extract then give some notes into df
            pages_df = pages_df.append({'conf': -1,'text': 'N/A'}, ignore_index=True)
            continue
         
    return pages_df
"""
"""




import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

if platform.system() == "Windows":
    # We may need to do some additional downloading and setup...
    # Windows needs a PyTesseract Download
    # https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine
 
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
 
    # Windows also needs poppler_exe
    path_to_poppler_exe = Path(r"C:\.....")
     
    # Put our output files in a sane place...
    out_directory = Path(r"~\Desktop").expanduser()
else:
    out_directory = Path("~").expanduser()   
    

PDF_file = Path(r"d.pdf")
 
# Store all the pages of the PDF in a variable

 

 
def ocr(PDF_file):
    
    ''' Main execution point of the program'''
    PDF_file= Path(PDF_file)
    image_file_list = []
    text_file = out_directory / Path("out_text.txt")
    with TemporaryDirectory() as tempdir:
        # Create a temporary directory to hold our temporary images.
 
      
 
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                PDF_file, 500, poppler_path=path_to_poppler_exe
            )
        else:
            pdf_pages = convert_from_path(PDF_file, 500)
        # Read in the PDF file at 500 DPI
 
        # Iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            # enumerate() "counts" the pages for us.
 
            # Create a file name to store the image
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
 
            page.save(filename, "JPEG")
            image_file_list.append(filename)
 
       
        pages = []
        for image_file in image_file_list:
 
            text = str(((pytesseract.image_to_string(Image.open(image_file)))))
            text = text.replace("-\n", "")
            pages.append(text)
        return pages

"""

import ocrmypdf
def ocr_path(path) : 
    ocrmypdf.ocr(path, path, skip_text= True )



















