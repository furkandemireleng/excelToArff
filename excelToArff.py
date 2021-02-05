#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 01:23:24 2021

@author: macxbookpro
"""
import pandas as pd
import xlsxwriter
import  xlwt
from xlwt import Workbook
import re
import tkinter 
from tkinter import simpledialog
from tkinter import filedialog
import os

import csv
from tkinter import *

top = tkinter.Tk()
top.title("ARF Maker") 
top.geometry("500x300")



def openExcel():
    global filename
    #klasor yollari
    filename = filedialog.askopenfilename(initialdir="/Users/macxbookpro/Desktop/", title="Select Excel  File")
    print(filename)
    os.system(filename)
    global dataset
    dataset = pd.read_excel(filename,encoding='utf-8',error_bad_lines=False)
    print(dataset)
    


def tweetDuzenle():
    global dataset1
    
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                          "]+", re.UNICODE)
            
    workbook1 = xlsxwriter.Workbook('deneme1.xlsx')
    worksheet1 = workbook1.add_worksheet()
    num_sayi1=0
    for i in dataset["Tweetler"]:
            a=emoji_pattern.sub(r'', i)
            x = a.rstrip()
            y=emoji_pattern.sub(r'', x)
            y=x.replace('\n', '').replace('\r', '')
            y=y.replace("'", "")
            y=y.replace('"', '')
            z="\'"+y+"\'"
            print(z)
            worksheet1.write(num_sayi1, 0, z)
            num_sayi1 +=1
            print(num_sayi1)
    workbook1.close()
    
    dataset1 = pd.read_excel("deneme1.xlsx",encoding='utf-8',error_bad_lines=False)
    print(dataset1)
    
def konuDuzenle():
    global dataset2
    workbook2 = xlsxwriter.Workbook('deneme2.xlsx')
    worksheet2 = workbook2.add_worksheet()
    num_sayi2=0 
    for i in dataset["Konu"]:
            z="\'"+i+"\'"
            print(z)
            worksheet2.write(num_sayi2, 0, z)
            num_sayi2 +=1
            
    
    workbook2.close()
    dataset2 = pd.read_excel("deneme2.xlsx",encoding='utf-8',error_bad_lines=False)
    print(dataset2)
    
    global konu_list
    konu_list=[]
    konu_list2=[]
    konu_list2.append(dataset["Konu"].unique())
    for i in konu_list2:
        print(i)
        konu_list.append(i)

def Birlestir():
    print(dataset1)
    df = pd.concat([dataset1,dataset2],axis =1)
    print(df)
    df.to_csv('tekkatmanhamtweet.csv', index=False,sep=',')
   
    
def yazdir1():
    f=open('deneme.txt','w+')
    relation = str(E1.get())
    f.write('@relation '+relation+'\n')
    f.write('@attribute text string'+'\n')
    f.write('@attribute class {'+str(konu_list)+'}'+'\n')
    f.write('@data'+'\n')
    f.close()
    
def writeToCSV():
    f=open('deneme2.txt','w+')
    csv_file = filedialog.askopenfilename(initialdir="/Users/macxbookpro/Desktop/", title="select csv")
    txt_file = 'deneme2.txt'
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [ my_output_file.write(",".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()
        
      
def writeToArff():
    arffttxt=open('sonarff.txt','w+')
    filenames = ['deneme.txt', 'deneme2.txt', ]
    with open('sonarff.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
        

     
def arffControl():
    with open('sonarff.txt', 'r') as file :
        filedata = file.read()
        

   
    filedata = filedata.replace('], dtype=object)]', '')
    filedata = filedata.replace('[array([', '')
    
    # Write the file out again
    with open('tekkatmanhamtweet.arff', 'w') as file:
        file.write(filedata)
        

      
def close_window():
    answer = simpledialog.askstring("Input", "kapatiyorum bak emin misin ?")
    if answer == "y":
        top.destroy()
    else:
        pass  


L1 = tkinter.Label(top, text="Relation Name")
E1 = tkinter.Entry(top, bd =5)


button_open = tkinter.Button(top, text ="Excel-Dosyasi-Sec", command = openExcel)
button1 = tkinter.Button(top, text ="Tweet Duzenle", command = tweetDuzenle)
button2 = tkinter.Button(top, text ="Konu Duzenle", command = konuDuzenle)
button4 = tkinter.Button(top, text ="Birlestir", command = Birlestir)
button5 = tkinter.Button(top, text ="CSV'yi Text'e yazdir", command = writeToCSV)
button6 = tkinter.Button(top, text ="Text Dosyasina Yazdir", command = yazdir1)
button7 = tkinter.Button(top, text ="ARFF Yazdir", command = writeToArff)
button8 = tkinter.Button(top, text ="ARFF duzenle", command = arffControl)
L1.pack()
E1.pack()
button_close = tkinter.Button(text = " Quit ! ", command = close_window) 

button_open.pack()

button1.pack()
button2.pack()
button4.pack()
button6.pack()
button5.pack()
button7.pack()
button8.pack()


button_close.pack()

top.mainloop()

