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
        self.type = None 
        
        
    def set_highlight(self, x) :
       self.highlight = x 
       
    def set_annot(self, x) :
       self.annot = x 
        
    def set_sentence(self, x) :
       self.sentence = x 
   
    def __str__(self ,rank = False):
        if rank : string =  f"annotation {self.rank} {self.highlight} could be improved  :  {self.annot}  )"
        else : string =  f"In the sentence ' {self.sentence}', the chunk ' {self.highlight} ' could be improved  :  {self.annot}  )"
        if self.type != None : string += "\n the teacher commented on the " +self.type
        return string
    
    
    def classify_comment(self, bavard = True) :
        
        prompt = 'A student wrote the following sentence "' + self.sentence 
        prompt += ' ".Highlighting the segment "' + self.highlight
        prompt += ' "he wrote the following comment "' + self.annot
        prompt += ' ". Did he commented on grammar or vocabulary ? Answer shortly'
        conv = conversation(prompt)
        answ = conv.interrogate()
        if bavard : print(conv.history)
        return answ
        """
        if "grammar" in answ : self.type = "Grammar"
        elif "vocabulary"in answ : self.type = "Vocabulary"
        else : self.type = "None written"
        """
    
    
    
    
""" l'élément clé du programme est de classer les annotations du professeur selon différentes catégories pour proposer le travail
le plus utile.
Il faut faire une typologie des types d'erreur et de ce qu'on attend pour pouvoir les corriger.

* Les erreurs de grammaire : On veut un point de leçon ainsi que des exercices d'application.

* Les erreurs de vocabualire. on veut une explication du terme employé en fr, en anglais , et de pourquoi ça ne marchait pas en contexte.

* Les erreurs de syntaxe : on  veut guider l'étudiant dans la reformulation d'une phrase.

* clarification requests.

NB : Il faudra éviter les redondances. 



Idée du programme : créer 4 sous classes de comments ou un marqueur, et il y aura 4 verions de la méthode "querry" qui communiquera avec chat GPT






"""