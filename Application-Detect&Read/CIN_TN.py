# -*- coding: utf-8 -*-
from flask import Flask, request , jsonify
from paddleocr import PaddleOCR
import numpy as np
import cv2
import sys
from PIL import Image
import os
from flask import render_template,flash,redirect
from PIL import Image
import time

#from io import BytesIO


sys.stdout.reconfigure(encoding='utf-8')


ocr = PaddleOCR(use_angle_cls = True ,lang='ar')
#ocr = PaddleOCR(use_angle_cls = True ,det_model_dir="https://paddleocr.bj.bcebos.com/PP-OCRv3/multilingual/Multilingual_PP-OCRv3_det_infer.tar",rec_model_dir="https://paddleocr.bj.bcebos.com/PP-OCRv3/multilingual/arabic_PP-OCRv3_rec_infer.tar")

def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def extract_closest_position(target_position, positions):
    closest_position = None
    closest_distance = float('inf')

    for position_list in positions:
        for position in position_list:
            distance = calculate_distance(target_position, position)
            if distance < closest_distance:
                closest_distance = distance
                closest_position = position

    return closest_position

def calculate_distance(position1, position2):
    # Calculate the distance between two positions (x and y coordinates)
    x1_min, y1_min = position1[0]
    x1_max, y1_max = position1[2]

    x2_min, y2_min = position2[0]
    x2_max, y2_max = position2[2]

    x1_avg = (x1_min + x1_max) / 2
    y1_avg = (y1_min + y1_max) / 2
    x2_avg = (x2_min + x2_max) / 2
    y2_avg = (y2_min + y2_max) / 2

    distance = ((x2_avg - x1_avg)**2 + (y2_avg - y1_avg)**2)**0.5
    return distance


def process_nom(data,image):
    #data = ocr.ocr(image)


     
    boites_numeriques_trouvees = False
    

    for i in range(len(data[0])):
        if data[0][i][1][0] in ['للقب', 'اللّقب', 'اللقب','اللي','االلقب','الي','ااقب','لقب','قب','اللء']:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
               
        numeric_boxes = []
        start_index = None
        end_index = None

        for i in range(len(data[0])):
            if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) <= 8:
                start_index = i
            elif data[0][i][1][0] in ['للقب', 'اللّقب', 'اللقب','اللي','االلقب','الي','ااقب','لقب','قب','اللء']:
                end_index = i

            if start_index is not None and end_index is not None:
                numeric_boxes = [box for box in data[0][start_index+1:end_index]]
                break
        if numeric_boxes and all(item[1][1] > 0.80 for item in numeric_boxes) :
            name_parts = []
            for line in numeric_boxes:
                name_parts.append(line[1][0])
            if name_parts[-1] in ['ابن','بن']:
                name = ' '.join(name_parts[::-1])
            else:
                name = ''.join(name_parts[::-1])
            return(name)
        else :
            points = [(330, 158), (506, 158), (506, 212), (330, 212)]
            x, y, width, height = get_bounding_rectangle(points)
            cropped_image = image[y:y+height, x:x+width]
            resultat2 = ocr.ocr(cropped_image)
            if (len(resultat2[0]) >0) :
                name_parts=[]
                for line in resultat2[0][:3]:
                    name_parts.append(line[1][0])
                if name_parts[-1] in ['ابن','بن']:
                    name = ' '.join(name_parts[::-1])
                else:
                    name = ''.join(name_parts[::-1])
                return(name)
            
    else:
   
        points = [(330, 158), (506, 158), (506, 212), (330, 212)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if (len(resultat2[0]) >0) :
            name_parts=[]
            for line in resultat2[0][:3]:
                name_parts.append(line[1][0])
            if name_parts[-1] in ['ابن','بن']:
                name = ' '.join(name_parts[::-1])
            else:
                name = ''.join(name_parts[::-1])
            return(name)
        

def process_num(data,image):
    #data = ocr.ocr(image)


    boites_numeriques_trouvees = False
 
    for i in range(len(data[0])):
        if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        
        # Extraire les boîtes ou le texte spécifique
        numeric_boxes = []
        start_index = None
        end_index = None
    
        for i in range(len(data[0])):
            if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
                numeric_boxes = [box for box in data[0][i]]
                break
        if numeric_boxes :
            return(numeric_boxes[1][0])
        #resultats_boites_numeriques.append(numeric_boxes)
    else:
        #points = [(226, 116), (377, 116), (377, 150), (226, 150)]
        points = [(216, 116), (393, 116), (393, 163), (216, 163)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        

def process_prenom(data,image):
    #data = ocr.ocr(image)


            # Parcourir l'output
    boites_numeriques_trouvees = False
    target_position = [(423, 201), (507, 201), (507, 235), (423, 235)]
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if data[0][i][1][0] in ['الاسم','الاسيم','ل','االاسم']:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        for i in range(len(data[0])):
            if data[0][i][1][0] in ['الاسم','الاسيم','ل','االاسم']:
                previous_line = data[0][i - 1]  
                next_line = data[0][i + 1] 
                closest_position = extract_closest_position(target_position, [[previous_line[0]], [next_line[0]]])
                if closest_position == previous_line[0]:
                    prenom = previous_line
                else :
                    prenom = next_line
                if data[0][i-2][1][0] not in ['للقب', 'اللّقب', 'اللقب', 'اللي', 'االلقب', 'الي', 'ااقب', 'لقب', 'قب', 'اللء'] and data[0][i-1][1][0] == 'محمد':
                    mot_precedent = data[0][i - 2][1][0]
                    return  prenom[1][0]  + " " +  mot_precedent
                else:
                    return prenom[1][0]
                    
                #return(prenom[1][0])
                 #print("Ligne précédente :", previous_line)
                    #print("Ligne suivante :", next_line)
    else:
        points = [(455, 207), (521, 218), (515, 253), (450, 242)]           
        #points = [(423, 201), (507, 201), (507, 235), (423, 235)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) >0 :
            return(resultat2[0][0][1][0])
                #resultats_boites_numeriques.append(resultat)


def naissance(data,image):
    
    #data = ocr.ocr(image)

            
    day = None
    month = None
    year = None
    months = ['جانفي', 'فيفري', 'مارس', 'افريل', 'ماي', 'جوان', 'جويلية', 'اوت', 'سبتمبر', 'اكتوبر', 'نوفمبر', 'ديسمبر']

    for box in data[0]:
        text = box[1][0]

        if text.isdigit():
            if len(text) == 2 and day is None:
                day = text
            elif len(text) == 4 and year is None:
                year = text
        elif text in months and month is None:
            month = months.index(text) + 1

        # Step 4: Return the formatted date
    if day is not None and month is not None and year is not None:
        #formatted_date = f"{day} {months[month - 1]} {year}"
        formatted_date = "{} {} {}".format(day, months[month - 1], year)
        return formatted_date
    else:
        points = [(249, 265), (465, 265), (465, 316), (249, 316)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
            #print(resultat2)
        for box in resultat2[0]:
            text = box[1][0]
            if text.isdigit():
                if len(text) == 2 and day is None:
                    day = text
                elif len(text) == 4 and year is None:
                    year = text
            elif text in months and month is None:
                month = months.index(text) + 1

        if day is not None and month is not None and year is not None:
            #formatted_date = f"{day} {months[month - 1]} {year}"
            formatted_date = "{} {} {}".format(day, months[month - 1], year)
            return formatted_date
        

corrections = {
    "شماء": "شيماء",
    "هدفاء": "هيفاء",
    "شبسى": "حسني",
    "الغريي" : "الغربي"    
}
def corriger_mot(mot, corrections):
    return corrections.get(mot, mot)

def process_image_data(image):
    data = ocr.ocr(image)
    print(data)
    num = process_num(data,image)
    #nom = process_nom(image)
    nom = corriger_mot(process_nom(data,image), corrections)  # Correction du nom
    prenom = corriger_mot(process_prenom(data,image), corrections)
    #prenom = process_prenom(image)
    date = naissance(data,image)
    
    output2 = {
        "الرقم": num,
        "الاسم": prenom,
        "اللقب": nom,
        "تاريخ الولادة": date
    }

    return output2



import json
import sys
from PIL import Image

# Import your functions and corrections here

def run_cin(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (570,375))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_recto{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))

    os.remove(cropped_recto_path)
    return output