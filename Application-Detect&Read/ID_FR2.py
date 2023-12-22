import os
import time
import cv2
#from paddleocr import PaddleOCR
from sanct import check_sanction

#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')
from test import ocr
def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def add_slashes(date_str):
    # Assuming the input date_str is in the format "DDMMYYYY"
    day = date_str[:2]
    month = date_str[2:4]
    year = date_str[4:]

    return f"{day}/{month}/{year}"

def contains_NOM(text):
    return "NOM" in text
def contains_names(text):
    return "names" in text
def contains_NOMs(text):
    return "NOM/" in text
def contains_Sumame(text):
    return "Sumame" in text
def contains_Prenoms(text):
    return "Prenoms" in text
def contains_Prenom(text):
    return "Prenom" in text
def contains_Lieu(text):
    return "LIEU" in text
def contains_Place(text):
    return "Place" in text
def contains_naissance(text):
    return "NAISSANCE" in text

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

##NOM

def process_nom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if (contains_NOM(data[0][i][1][0]) or contains_NOMs(data[0][i][1][0]) or contains_Sumame(data[0][i][1][0])):
            boites = True
            break
            
    if boites :
        for i in range (len(data[0])):
            if (contains_NOM(data[0][i][1][0]) or contains_NOMs(data[0][i][1][0]) or contains_Sumame(data[0][i][1][0])): 
                box = data[0][i+1]
                nom=box[1][0]
                return(nom)
            
            
    else :
        points =[(224, 84), (353, 84), (353, 107), (224, 107)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        

##PRENOM

def process_prenom(data,image):
    #data=ocr.ocr(image)
    
    nom = False
    prenom = False
    
    for i in range (len(data[0])):
        if (contains_Prenoms(data[0][i][1][0]) or contains_Prenom(data[0][i][1][0]) or contains_names(data[0][i][1][0])):
            prenom = True
        elif (contains_NOM(data[0][i][1][0]) or contains_NOMs(data[0][i][1][0]) or contains_Sumame(data[0][i][1][0])):
            nom = True
            
    if prenom :
        for i in range (len(data[0])):
            if (contains_Prenoms(data[0][i][1][0]) or contains_Prenom(data[0][i][1][0]) or contains_names(data[0][i][1][0])):
                box = data[0][i+1]
                prenom = box[1][0]
                return(prenom)
    elif nom:
        for i in range (len(data[0])):
            if (contains_NOM(data[0][i][1][0]) or contains_NOMs(data[0][i][1][0]) or contains_Sumame(data[0][i][1][0])):
                box = data[0][i+3]
                prenom = box[1][0]
                return(prenom)

            
            
    else :
        points =[(229, 136), (400, 136), (400, 158), (229, 158)]
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
        if re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{9}$', text):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{9}$', text):
                numeric_boxes = data[0][i]
                return numeric_boxes[1][0]
        # Si on n'a pas trouvé de correspondance, retourner None
        return None
    else:
        points = [(227, 278), (380, 278), (380, 307), (227, 307)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return resultat2[0][0][1][0]
        
##NATIONALITe

def process_nationalité(data,image):
    #data = ocr.ocr(image)
    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if len(data[0][i][1][0]) == 3 and data[0][i][1][0].isupper():
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        for i in range(len(data[0])):
            if len(data[0][i][1][0]) == 3 and data[0][i][1][0].isupper():
                box = data[0][i]
                nation = box[1][0]
                return(nation)
            
    else:
        points = [(288, 182), (325, 182), (325, 204), (288, 204)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        

##LIEU DE NAISSANCE

def process_lieu(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if (contains_Lieu(data[0][i][1][0]) or contains_Place(data[0][i][1][0]) or contains_naissance(data[0][i][1][0])):
            boites = True
            break
            
    if boites :
        for i in range (len(data[0])):
            if (contains_Lieu(data[0][i][1][0]) or contains_Place(data[0][i][1][0]) or contains_naissance(data[0][i][1][0])):
                box = data[0][i+1]
                nom=box[1][0]
                return(nom)
            
            
    else :
        points =[(222, 216), (337, 216), (337, 236), (222, 236)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
## DATE DE NAISSANCE 

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
        points = [(412, 183), (521, 182), (520, 202), (413, 205)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))


##DATE D'EXPIRATION

def process_expirer(data,image):
    #data = ocr.ocr(image)
    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
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
        points = [(413, 275), (516, 275), (516, 297), (413, 297)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        

corrections ={
    "MAKHLOUE":"MAKHLOUF"
}
        
def corriger_mot(mot, corrections):
    return corrections.get(mot, mot)

def process_image_data(image):
    data = ocr.ocr(image)
    print(data)
    num = process_num(data,image)
    nom = corriger_mot(process_nom(data,image),corrections) 
    prenom = process_prenom(data,image)
    naissance = process_naiss(data,image)
    expiration = process_expirer(data,image)
    natio = process_nationalité(data,image)
    lieu = process_lieu(data,image)
    sanction = check_sanction(nom, prenom, naissance, "française")
    
    output = {
        "type":"cinFRnouvelle",
        "nom" : nom,
        "prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        "dateDelivrance": None,
        "dateValidite" : expiration,
        "nationalite" : "française",
        "lieu" : lieu,
        "IdCin" : None,
        "sanction": sanction
    }

    return output

def run_CINFR2(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (570, 375))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))
        
        # Supprimer l'image après avoir généré la sortie
    os.remove(cropped_recto_path)
    return output