# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:43:18 2023

@author: 3b13j
"""
from gpt_pipeline import conversation 

class comment() :
    
    def __init__(self, rank ):
        self.rank = rank
        self.highlight = ""
        self.annot = ""
        self.sentence = ""
        
    def set_highlight(self, x) :
       self.highlight = x 
       
    def set_annot(self, x) :
       self.annot = x 
        
    def set_sentence(self, x) :
       self.sentence = x 
   
    def __str__(self ,rank = False):
        
        string = f" sentence : {self.sentence}   highlight : {self.highlight}       annot : {self.annot} "
        return string
    