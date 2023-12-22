import os
import cv2
import time
from test import ocr
from sanct import check_sanction
#from paddleocr import PaddleOCR
#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')

def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def extract_date(text):
    pattern = r'(\d{2}[.\s]?\d{2}[.\s]?\d{4})'
    match = re.search(pattern, text)
    
    if match:
        date_with_possible_delimiters = match.group(1)
        date_without_delimiters = date_with_possible_delimiters.replace(".", "").replace(" ", "")
        formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
        return formatted_date
    else:
        return None

def contains_NOM(text):
    return "Nom" in text
def contains_Prenoms(text):
    return "Prenoms" in text
def contains_Prenom(text):
    return "Prenom" in text

def process_nom(data,image):
    #data=ocr.ocr(image)
    
    nom = False
    prenom = False
    
    for i in range (len(data[0])):
        if contains_NOM(data[0][i][1][0]):
            nom = True
        elif contains_Prenom(data[0][i][1][0]):
            prenom=True
            break
            
    if nom :
        for i in range (len(data[0])):
            if contains_NOM(data[0][i][1][0]): 
                box = data[0][i+1]
                nom=box[1][0]
                return(nom)
    elif prenom :
        for i in range (len(data[0])):
            if contains_Prenom(data[0][i][1][0]): 
                box = data[0][i-1]
                nom=box[1][0]
                return(nom)
        
            
            
    else :
        points =[(197, 109), (274, 109), (274, 134), (197, 134)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_prenom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if (contains_Prenoms(data[0][i][1][0]) or contains_Prenom(data[0][i][1][0])):
            boites = True
            break
            
    if boites :
        for i in range (len(data[0])):
            if (contains_Prenoms(data[0][i][1][0]) or contains_Prenom(data[0][i][1][0])): 
                box = data[0][i+1]
                prenom = box[1][0]
                return(prenom)
            
            
    else :
        points = [(197, 107), (281, 107), (281, 135), (197, 135)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
import re

def process_num(data,image):
    #data = ocr.ocr(image)

    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        text = data[0][i][1][0]
        if re.match(r'.*\d.*[a-zA-Z].*', text) and len(text) == 9:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if re.match(r'.*\d.*[a-zA-Z].*', text) and len(text) == 9:
                numeric_boxes = data[0][i]
                return numeric_boxes[1][0]
        # Si on n'a pas trouvé de correspondance, retourner None
        return None
    else:
        points = [(196, 159), (261, 159), (261, 184), (196, 184)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return resultat2[0][0][1][0]
        

def process_nationalité():
    Nationlité= "française"
    return(Nationlité)
        
def add_slashes(date_str):
    # Assuming the input date_str is in the format "DDMMYYYY"
    day = date_str[:2]
    month = date_str[2:4]
    year = date_str[4:]

    return f"{day}/{month}/{year}"

def process_naiss(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                box = data[0][i]
                date = extract_date(box[1][0])
                #formatted_date = date.replace(".", "/")  # Convertir . en /
                return date
            
    else:
        points = [(199, 191), (265, 191), (265, 202), (199, 202)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        
def process_delivrer(data,image):
    #data = ocr.ocr(image)
    # Parcourir l'output
    boites_numeriques_trouvees = False
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        count_dates = 0
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                count_dates+=1
                if count_dates == 2 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    #formatted_date = date.replace(".", "/")  # Convertir . en /
                    return date
            
    else:
        points = [(197, 311), (285, 311), (285, 337), (197, 337)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        
def process_expirer(data,image):
    #data = ocr.ocr(image)
    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        count_dates = 0
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                count_dates+=1
                if count_dates == 3 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    #formatted_date = date.replace(".", "/")  # Convertir . en /
                    return date
            
    else:
        points = [(198, 411), (295, 411), (295, 440), (198, 440)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        
def process_lieu(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
                numeric_boxes = data[0][i+1]
                lieu = numeric_boxes[1][0]
                return(lieu)
            
    else:
        points = [(328, 257), (523, 257), (523, 289), (328, 289)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def extract_nom_prenom(data):
    nom = ""
    prenom = ""

    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if text.startswith("P<FRA"):
            parts = text.split("<<")
            #if len(parts) == 2:
            nom = parts[0][5:]  # Supprime "P<FRA" du début
            prenom = parts[1]

            nom = nom.replace("<", " ")
            prenom = prenom.replace("<", " ")
            break

    return nom, prenom
        
def process_image_data(image):
    data = ocr.ocr(image)
    num = process_num(data,image)
    nom ,prenom = extract_nom_prenom(data) 
    #prenom = process_prenom(data,image)
    naissance = process_naiss(data,image)
    delivrance = process_delivrer(data,image)
    expiration = process_expirer(data,image)
    natio = process_nationalité()
    lieu = process_lieu(data,image)
    sanction = check_sanction(nom, prenom, naissance, "française")
    
    output = {
        "type":"passeportFR",
        "nom" : nom,
        "prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        "dateDelivrance": delivrance,
        "dateValidite" : expiration,
        "nationalite" : "française",
        "lieu" : lieu,
        "IdCin" : None,
        "sanction": sanction
    }

    return output



def run_PASSEPORT2(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (640,640))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))
        
        # Supprimer l'image après avoir généré la sortie
    os.remove(cropped_recto_path)
    return output