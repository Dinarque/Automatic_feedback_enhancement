# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:07:24 2023

@author: 3b13j
"""
import streamlit as st 

def markdown_underline(sentence, segment, colour = "yellow" ) :
    
    if segment in sentence : 
        store = sentence.split(segment)
        """
        mkd = f"{store[0]}**:{colour}[{segment}]**{store[1]}"
        """
        mkd = f'{store[0]}**<span style="color:{colour};">{segment}</span>**{store[1]}'
        store.append("")
        return mkd

    else : return sentence
    



def just(text, position = "justify") : 
    
    return f'<div style="text-align: {position};">'+text+'</div>'

def l(text, position = "justify") :
    return st.markdown(just(text, position), unsafe_allow_html=True)
 
def centered_title(text) :
    title_alignment= '<style> '+text+' {text-align: center}</style>'
    print(title_alignment)
    st.markdown(title_alignment, unsafe_allow_html=True)

def title(text, colour = "white", align="center") :
    
    line = f"<h2 style='text-align: {align}; color: {colour};'>" + text + "</h2>"
    st.markdown(line, unsafe_allow_html=True)
    
def centered_button (label) :
    
    c1, c2,c3 = st.columns(3)
    with c2 : 
        st.button(label)
        
def colour_html (text, segment, colour ="yellow") :
    if segment in text : 
        borders = text.split(segment)
        answ = f'{borders[0]} <span style="color:{colour};">{segment}</span> {borders[1]}'
        if len(borders) > 2 : 
            for el in borders [2:] : answ += el 
        return answ
    return text 
    
def underline_segments(text, segments, colour="yellow") :
    for seg in segments :
        text = colour_html(text, seg, colour)
    return text

def add_alinea(text) :
    return f"<p style='margin-left: 30px;'>{text}</p>"
    
    
# the banshees of Inisherin