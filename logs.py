# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:56:44 2023

@author: 3b13j
"""
import os
import streamlit as st




def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_log(file_name, logs_folder="logs"):
    file_name = file_name.split(".pdf")[0] + "_correction_log_v8"
    create_folder("logs")
    
    path =  os.path.join(logs_folder, file_name)
    if not os.path.isfile(path) :

        try:
            with open(path, 'a') as new_file:
                print(f"File '{file_name}' created in '{logs_folder}' folder.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
    return path

def update_log(file_path, content):

    try:
        with open(file_path, 'a') as file:
            file.write(content)
            print("Content appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def erase_log(file_path) : 
    try:
        with open(file_path, 'w') as file:
            file.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def eliminate(liste, text) :
    for el in liste :
        while el in text :
            text = text.replace(el, "")
        return text 
    
def extract_log(log_path):
    
        with open(log_path, 'r') as file:

            liste = ["\nn", "\n", "\\"]
            file = str(file.read())
            
            #file = eliminate(liste, file)
            file = file.replace (" {", "{")
            file = file.replace ("'s ", " s ")
            while "  " in file:
                file = file.replace ("  ", " ")
            file = file.split("*") 
            if file[0] == "" :  file = file [1:]
    
            dic = {}
            print("FILE")
            print()
            print(len(file))
            print()
            print(file)
            
            for i in range(int(len(file)/2) -1):
                a = 2*i 
                b = a+1
                fa = int(file[a])
                fb = file[b]
                """
                if '"' not in fb[-10:]  and "'" not in fb[-10:]:
                        fb += '"'
                if "}" not in fb[-12:] : 
                       fb +=  "}"
                """
                d = eval (fb)
                dic[fa-1] = d
               
            return  file, dic

  

def log_price(name, tok,price) :
    file_path = "tok_price"
    create_log(file_path, logs_folder="logs")
    with open(file_path, 'a') as file:
        file.write(f'for file {name}      tokens : {tok}     price : {price}   \n')
    
    
### TODO

"""
fix stqdm in the main page while correcting
reput the chat into work
fixing log system with right name
"""

    
    
    
    
    
    
    