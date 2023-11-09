# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:12:42 2023

@author: 3b13j  
"""

## code hyperparameters

Link_2_GPT = True
dvlper_mode = False
colored = True

button= False

#14 13 28 110 121 188 228 258

## imports 

import streamlit as st
import nltk
import os
from  pdf_extractor_with_ocr import  deal_with_annotation , get_composition
from dotenv import load_dotenv , find_dotenv 
load_dotenv(find_dotenv(), override=True)
from displaying_tools import  l, title,  colour_html, add_alinea
from logs import create_log, update_log, extract_log, log_price
from content_analysis import get_data, create_review 
if Link_2_GPT : 
    from gpt_pipeline import correction_prompt,  sum_up, create_extra, streamlit_chat, update_cost, create_exo
from stqdm import stqdm
from ocr import ocr_path


## setting the streamlit session state

if "price" not in st.session_state : 
    st.session_state.price = 0 

if "mission" not in st.session_state:
    st.session_state.mission = False
    
if "display_menu" not in st.session_state:
    st.session_state.display_menu = False

if "displayed_chunk" not in st.session_state:
    st.session_state.displayed_chunk = False
    
if "chunk_analysis" not in st.session_state:
    st.session_state.chunk_analysis = {}
    
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    
if "token_used" not in st.session_state:
    st.session_state.token_used = 0

if "buffer" not in st.session_state : 
    st.session_state.buffer = "buffer"
    
if "disp_price" not in st.session_state : 
    st.session_state.disp_price = False
    
st.session_state.name = ""
    
def set_mission(pm):
    st.session_state.mission =pm
     
def display_menu (bol = True):
    st.session_state.display_menu = bol
 
def launch_extraction() :
    with open("buffer.pdf", "wb") as f:
        f.write(st.session_state.file.getbuffer())

        st.session_state.str_file = get_composition("buffer.pdf")
        if st.session_state.str_file == "" or st.session_state.str_file == None : 
            ocr_path("buffer.pdf")
            st.session_state.OCR = True
            st.session_state.str_file = get_composition("buffer.pdf")
            
            
        st.session_state.chunks= deal_with_annotation("buffer.pdf")
        st.session_state.nb_chunks = len(st.session_state.chunks)

      
    

def cleanse(session_state) : 
    session_state.chunk_analysis = {}
    session_state.synthesis = {}
    session_state.summary = None
    session_state.vocabulary = None 
    session_state.displayed_chunk = 0
    session_state.chunks = []
    
    
import PyPDF2
def pdf_read(file) :
    
        pdf_reader = PyPDF2.PdfReader(file)
        # Initialize a variable to store the PDF text
        pdf_text = ""
        # Iterate through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text
    
    
def correct_all(session_state) :
    
    for i in stqdm(range(len(session_state.chunks)))  :
       
        
        if i not in session_state.chunk_analysis.keys() : 
            answer, cb  = correction_prompt(session_state.chunks[i])
            update_cost(st.session_state, cb)
            session_state.chunk_analysis[i] = answer
            update_log(session_state.log_path, f'*{i}* \n {answer}  \n \n \n', )
        else  : st.write(f"chunk {i}  was already corrected ")
        

## Main code

st.title("Automatic Feedback Enhancement")
if dvlper_mode : st.session_state
"___"

st.session_state

## sidebar
with st.sidebar : 
    
    c1, c2 = st.columns([10, 2])
    with c1 : title("Please configurate the learning tool")
    with c2 : st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
    
    "___"
    api_key = st.text_input("OpenAI API Key (alreaydy pre-entered)",  type="password")
    if api_key: 
        os.environ['OPENAI_API_KEY'] = api_key
     
    c1, c2 = st.columns(2) 
    with c1 :language = st.selectbox(label= "Choose the feedback language", options= ["English", "French"], index=0, key="language")
    with c2 : target = st.selectbox(label= "Choose the target language", options= ["English", "French"], index=1, key="target")
    "___"
    title("Load a file")
    file = st.file_uploader(label="", type=["pdf",'txt'], accept_multiple_files=False, key="file")
    
    if file is not None:
        
        lb, rb , tb = st.columns(3)
        
        
        if file is not None and file.name != st.session_state.buffer :
            if  lb.button(label="launch feedback") :
                cleanse(st.session_state)
                display_menu(True)
                h = launch_extraction()
                path = create_log(file.name)
                st.session_state.name = st.session_state.file.name
                st.session_state.log_path = path
                st.session_state.buffer = file.name
                if not api_key  or api_key =="Already filled in this tryout version" :
                    os.environ['OPENAI_API_KEY'] = ""
                    st.session_state.OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
                st.experimental_rerun
                    
        elif file is not None and file.name == st.session_state.buffer : 
            if lb.button("Menu") : 
                     display_menu(True)
                     set_mission(False)
                     st.experimental_rerun() 
                     
        if "log_path" in st.session_state :
                if rb.button("load from log") :
                    
                    file, log_analysis  = extract_log(st.session_state.log_path)
                    st.session_state.chunk_analysis = log_analysis
                    
                
                if tb.button("display cost") :
                    st.session_state.disp_price = not st.session_state.disp_price
                if st.session_state.disp_price : 
                    st.write (st.session_state.price)
        
                
## menu

if st.session_state.display_menu :   
    
    l("Thanks for uploading a file.  You can now display it or proceed to correction", position="center")
    "___"
    left, mid, mid2, mid3,  right = st.columns(5)
    with left :  
        if st.button(label="Display") :
            display_menu(False)
            set_mission("dis")
            st.experimental_rerun() 
            
    with right : 
        if st.button(label="Tutorial") :
            display_menu(False)
            set_mission("pic")
            st.experimental_rerun() 
            
    with mid : 
         if st.button(label="Correct") : 
             display_menu(False)
             set_mission("cor")
             st.experimental_rerun() 
             
    with mid2 : 
         if st.button(label="Display statistics") : 
             display_menu(False)
             set_mission("stat")
             st.experimental_rerun() 
             
    with mid3 :
        if st.button(label="Generate review pdf") : 
            if "summary" not in st.session_state :
                summary, cb = sum_up(st.session_state)
                update_cost(st.session_state, cb)
                st.session_state.summary = summary
            create_review(st.session_state)
            display_menu(False)
            set_mission("pdf")
            st.experimental_rerun() 
    "___"      
    st.image("https://cdn.pixabay.com/photo/2016/10/21/00/50/editing-1756958_1280.jpg")
   
    

else :   
            
     ## pic   
    
    if st.session_state.mission == "pic" : 
        st.subheader("Access a tutorial")
       
        st.write(" open in your browser [link](https://drive.google.com/file/d/1X3tsGjavG_mwRWdEcUnKhW3dZfG1CWFF/view?usp=sharing)")
       
        if st.button("Come back to the menu") : 
            display_menu(True)
            set_mission(False)
            st.experimental_rerun() 
            
            
            
    ## pdf 
    
    elif st.session_state.mission =="pdf" :
        
        
        import docx2txt

        file_path = "review_document.docx"  # Replace with the actual path to your DOCX file
        st.subheader("Here is your review document. The pagination option are limited on the app, please download the file for better readability")
        
        from docx import Document
        doc = Document(file_path)
        
        import io
        doc_download = doc
        try : 
            fn =  f"Review_document_for_{st.session_state.file.name}.docx"
        except : 
            fn = "Review_document.docx"
        bio = io.BytesIO()
        doc_download.save(bio)
        if doc_download:
            st.download_button(
                label="Download the file",
                data=bio.getvalue(),
                file_name=fn,
                mime="docx"
            )
        try:
            text = docx2txt.process(file_path)
            st.text(text)
        except Exception as e:
            st.text("Error:", e)
        
   
        if st.button("Come back to the menu") : 
            display_menu(True)
            set_mission(False)
            st.experimental_rerun() 

        
    
    ## dis
    
    elif st.session_state.mission =="dis" :
        
        l ("Here is the original work : ", "center")
        "___"
        texte = texte = nltk.sent_tokenize(st.session_state.str_file)
        st.session_state.texte = texte 
        st.session_state.sentence  = [chunk.sentence for chunk in st.session_state.chunks]
        sentences = [com.sentence for com in st.session_state.chunks]
        segments = [com.highlight for com in st.session_state.chunks]
        
        text = ""
        
        for sent in texte :
            for i in range(len(sentences)): 
                if sentences[i] == sent : sent = colour_html(sent, segments[i])
            text += sent
        
        l(add_alinea(text) )
        "___"
        
        if "summary" in st.session_state :
            st.subheader("Summary :")
            st.session_state.summary
            "___"
        
        left, right = st.columns(2)
        
        with left : 
            if st.button("proceed to correction ?") : 
                set_mission("cor")
                st.experimental_rerun() 
        with right : 
            if st.button("Back to the menu") : 
                display_menu(True)
                set_mission(False)
                st.experimental_rerun() 
    ## stat

    elif st.session_state.mission == "stat" :
        get_data(st.session_state)
        if st.button("Back to the menu") : 
            display_menu(True)
            set_mission(False)
            st.experimental_rerun() 
        
    ## cor
    elif st.session_state.mission == "cor" :
        
        
       
            
    
        chunk = st.session_state.chunks [st.session_state.displayed_chunk]
        title(f"Chunk n°{st.session_state.displayed_chunk+1}")
            
        "___"
                 
            
       
        if colored : 
                from displaying_tools import markdown_underline 
                mkd = markdown_underline(chunk.sentence, chunk.highlight)
                
                l(f"Look at the following sentence : {mkd} ")
                l(f"I quote your teacher : '{chunk.annot}'")
         
                "___"
                
        else: 
                
                l(f"In the sentence '{chunk.sentence}', the segment '{chunk.highlight}' is not correct. I quote your dear teacher : '{chunk.annot}'")
                "___"
            
        if st.session_state.displayed_chunk not in st.session_state.chunk_analysis.keys() :
                z1, z2, z3 = st.columns(3) 
                
                with z1 : 
                    
                    
                    if st.button("Correct this segment") :
                        answer, cb = correction_prompt(chunk)
                        update_cost(st.session_state, cb)
                        st.session_state.chunk_analysis[st.session_state.displayed_chunk] = answer
                        update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                        st.experimental_rerun() 
                        
                with z2 : 
                    if st.button("Correct a batch of 10") :
                        
                        
                        for i  in stqdm(range(st.session_state.displayed_chunk, min( (st.session_state.displayed_chunk+10), len(st.session_state.chunks)))) :
                            if i not in st.session_state.chunk_analysis.keys() : 
                                answer, cb  = correction_prompt(st.session_state.chunks[i])
                                update_cost(st.session_state, cb)
                                st.session_state.chunk_analysis[i] = answer
                                update_log(st.session_state.log_path, f'*{i}* \n {answer}  \n \n \n', )
                        st.experimental_rerun() 
                                
                if z3.button("Correct all") :
                        correct_all(st.session_state)
                        st.experimental_rerun() 
                
        else: 
                
              
                 
                dic  = (st.session_state.chunk_analysis[st.session_state.displayed_chunk])
                if type(dic) is not dict  and type(dic) is str : 
                    try  : dic = eval(dic)
                    except : 
                        answer, cb = correction_prompt(chunk)
                        update_cost(st.session_state, cb)
                        st.session_state.chunk_analysis[st.session_state.displayed_chunk] = answer
                        update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                        st.experimental_rerun() 
            
                
                l(f'This is a {dic["Type"]} mistake.')
                "___"
                st.subheader("Explanation : ")
                l(dic["Explanation"])
                "___"
                st.subheader("Suggested correction : ")
                l(dic["Corrected Sentence"])
                
                
                if "Extra" in dic.keys() :
                    "___"
                    if dic["Type"] == "grammar" : st.subheader(f"Lesson on {dic['Label']}) :")
                    else : st.subheader("Here are some ressources :")
                                                             
                    dic["Extra"]
                    
                    
                if "Exo" in dic.keys():
                    "___"
                    
                    st.subheader("Exercise :")
                    dic["Exo"]["exercise"]
                    "\n \n"
                    disp = False 
                    if st.button ("Display answer key") :
                        disp =True
                    if disp : 
                        st.subheader("Answer key :")
                        dic["Exo"]["answer_key"]
                    
                
                
                
                if "Chat" in dic.keys() : 
                    
                    if dic["Chat"] :
                        "___"
                        st.subheader("Virtual assistant")
                        
                        streamlit_chat(dic, st.session_state.OPENAI_API_KEY)
                        
                        "___"
                
                "___"
                "if you are not satisfied with this correction, you cantry to run it again"
                "___"
                
                z1, z2, z3= st.columns(3)
                
                if "Chat" in dic.keys() and dic["Chat"] :
                    z3_mes ='Hide virtual assistant'
                else :
                    z3_mes ="Ask our virtual assistant"
                
                with z1 : 
                    if st.button("Rerun correction") :
                        answer, cb = correction_prompt(chunk)
                        st.session_state.cb = cb
                        st.session_state.chunk_analysis[st.session_state.displayed_chunk] = answer
                        update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {answer}  \n \n \n', )
                        st.experimental_rerun() 
                
                 
                with z2 : 
                    if "Extra" not in dic.keys() :  mes = "Display more information"
                    else : mes = "Regenerate extra content"
                    
                    if st.button(mes) :
                        
                        extra, cb = create_extra(dic, chunk.sentence, st.session_state)
                        if dic["Type"] == "grammar" :
                            update_cost(st.session_state, cb)
                        dic["Extra"] = extra
                        st.session_state.chunk_analysis[st.session_state.displayed_chunk] = dic
                        update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                        st.experimental_rerun() 
                        
                    if "Extra" in dic.keys() and "Exo" not in dic.keys() :
                        
                        if st.button("Generate an exercise ") :
                            if "summary" not in st.session_state :
                                summary, cb = sum_up(st.session_state)
                                update_cost(st.session_state, cb)
                                st.session_state.summary = summary
                                
                            exo, cb = create_exo(dic, st.session_state.summary)
                            update_cost(st.session_state, cb)
                            try : dic["Exo"] = eval(exo)
                            except : 
                                exo, cb = create_exo(dic, st.session_state.summary)
                                dic["Exo"] = eval(exo)
                                update_cost(st.session_state, cb)
                            st.session_state.chunk_analysis[st.session_state.displayed_chunk] = dic
                            update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                            st.experimental_rerun()
                            
                    if "Extra" in dic.keys() and "Exo" in dic.keys() :
                        
                        if st.button("Regenerate another exercise ") :
                            
                            if "summary" not in st.session_state :
                                summary, cb = sum_up(st.session_state)
                                update_cost(st.session_state, cb)
                                st.session_state.summary = summary
                            exo, cb = create_exo(dic, st.session_state.summary)
                            update_cost(st.session_state, cb)
                            dic["Exo"] = eval( exo)
                            st.session_state.chunk_analysis[st.session_state.displayed_chunk] = dic
                            update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                            st.experimental_rerun()
                            
                        
                        
                with z3 : 
                    if st.button(z3_mes) :
                       if "Chat" not in dic.keys() : dic["Chat"]  = False
                       dic["Chat"] = not dic["Chat"]
                       update_log(st.session_state.log_path, f'*{st.session_state.displayed_chunk+1}* \n {st.session_state.chunk_analysis[st.session_state.displayed_chunk]}  \n \n \n', )
                       st.experimental_rerun() 
                
                "___"
                
                
                
               
            
        fc, left, mid, right, lc = st.columns(5)
            
        with fc : 
                if st.button(label="First chunk")  :
                    st.session_state.displayed_chunk = 0
                    st.experimental_rerun() 
                
        with lc : 
                 if st.button(label="Last chunk")  :
                     st.session_state.displayed_chunk =  len(st.session_state.chunks)-1
                     st.experimental_rerun() 
             
            
        if st.session_state.displayed_chunk != 0 : 
                with left :  
                    if st.button(label="Prev chunk")  :
                        st.session_state.displayed_chunk = st.session_state.displayed_chunk -1
                        st.experimental_rerun() 
                        
        if st.session_state.displayed_chunk != (len(st.session_state.chunks)-1) :
                with right : 
                    if st.button(label="Next chunk")   and st.session_state.displayed_chunk < len(st.session_state.chunks) :
                        st.session_state.displayed_chunk = st.session_state.displayed_chunk +1
                        st.experimental_rerun() 
        with mid : 
                 if st.button("Back to menu") : 
                     display_menu(True)
                     set_mission(False)
                     st.experimental_rerun() 
        lc, rc = st.columns ([4,1] )    
        slider = lc.slider("Select a chunk", min_value=1, max_value=len(st.session_state.chunks), value=1)
            # need 2 update streamlit label_visibility="collapsed"
        with rc : 
                if st.button(label=f"Go to chunk {slider}")  :
                    st.session_state.displayed_chunk = slider -1
                    st.experimental_rerun() 
            
        if len(st.session_state.chunks) == 0 :
            "There is apparently no mistake in this homework ! Well done !"
        
    else : 
        
        l("This app aims at helping students review and correct their writing in a foreign language. You have to upload a corrected pdf file where the mistakes have been highlighted by an educator. The work will be divided into chunks and the application will call a Large Language Model to help provide a more detailed feedback. For each chunk, grammatical or vocabular explanation will be provided. You will be able to request further exercises. At the end of the session, all the information will be gathered in a synthetic pdf that will work as a revision tool.  Enjoy :100: !  ")
           
if dvlper_mode : st.session_state



for i in range(10) :
    st.write("")
st.write(" © Automatic Feedback Enhancement App created by Louis Jourdain")




