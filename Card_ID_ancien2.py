import os
import cv2
#from paddleocr import PaddleOCR
import time
from sanct import check_sanction

#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')




from test import ocr

def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def contains_NOM(text):
    pattern = r'(?i)Nom[^A-Z]*([A-Z\s]+)' 
    return re.search(pattern, text) is not None

def contains_Prenom(text):
    return "Prenom" in text

def contains_Prénom(text):
    return "Prénom" in text

def contains_Prenoms(text):
    return "Prenoms" in text

import re

def extract_nom(text):
    pattern = r'(?i)Nom[^A-Z]*([A-Z\s]+)'  
    matches = re.findall(pattern, text)
    
    if matches:
        uppercase_parts = [part.strip() for part in matches[-1].split() if part.isupper()]
        if uppercase_parts:
            return ' '.join(uppercase_parts)
    
    return None

def extract_prenom(text):
    
    pattern = r'([A-Z\s]+)'
    matches = re.findall(pattern, text)
    
    if matches:
        uppercase_parts = [part.strip() for part in matches[-1].split() if part.isupper()]
        if uppercase_parts:
            return ' '.join(uppercase_parts)
    
    return None

def extract_date(text):
    if re.search(r'\d{12}', text):
        return None
    pattern = r'(\d{2}[.\s]?\d{2}[.\s]?\d{4})'
    match = re.search(pattern, text)
    
    if match:
        date_with_possible_delimiters = match.group(1)
        date_without_delimiters = date_with_possible_delimiters.replace(".", "").replace(" ", "")
        formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
        return formatted_date
    else:
        return None
    
def extract_nationalite(text):
    pattern = r'Nationalite\s?(\w+)' 
    match = re.search(pattern, text, re.IGNORECASE)  # Ignorer la casse

    if match:
        return match.group(1)
    else:
        return None

def extract_nationalité(text):
    pattern = r'Nationalité\s?(\w+)'  # Recherche du mot après Nationalite
    match = re.search(pattern, text, re.IGNORECASE)  # Ignorer la casse

    if match:
        return match.group(1)
    else:
        return None

def extract_number(text):
    pattern = r'^\d{12}'  # Recherche d'une séquence de 12 chiffres au début du texte
    match = re.match(pattern, text)
    
    if match:
        return match.group(0)
    else:
        return None

def process_nom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if (contains_NOM(data[0][i][1][0])):
            boites = True
            break
            
    if boites :
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if contains_NOM(text):
                box = data[0][i]
                nom = extract_nom(box[1][0])
                if "BEN" in nom:
                    nom_parts = nom.split("BEN")
                    nom_parts_cleaned = [part.strip() for part in nom_parts if part.strip()]
                    nom = "BEN " + " ".join(nom_parts_cleaned)
                return(nom)
            
    else :
        points =[(227, 74), (303, 74), (302, 94), (228, 94)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_prenom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if (contains_Prenom(data[0][i][1][0])) or (contains_Prénom(data[0][i][1][0])):
            boites = True
            break
            
    if boites :
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if contains_Prenom(text) or (contains_Prénom(data[0][i][1][0])):
                box = data[0][i]
                prenom = extract_prenom(box[1][0])
                if "MOHAMED" in prenom:
                    nom_parts = prenom.split("MOHAMED")
                    nom_parts_cleaned = [part.strip() for part in nom_parts if part.strip()]
                    prenom = "MOHAMED " + " ".join(nom_parts_cleaned)
                return prenom
    
            
    else :
        points =[(251, 113), (313, 113), (313, 131), (251, 131)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_num(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if extract_number(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_number(text):
                box = data[0][i]
                num = extract_number(box[1][0])
                return(num)
                
    else:
        points = [(259, 48), (371, 48), (371, 71), (259, 71)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_date(data,image):
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
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_natio(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if (extract_nationalite(data[0][i][1][0]) or extract_nationalité(data[0][i][1][0])) :
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_nationalite(text):
                box = data[0][i]
                natio = extract_nationalite(box[1][0])
                return(natio)
            elif extract_nationalité(text):
                box = data[0][i]
                nation = extract_nationalité(box[1][0])
                return(nation)
                
    else:
        points = [(473, 55), (531, 54), (532, 75), (472, 74)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])

corrections ={
    "Francaise":"française"
}
def corriger_mot(mot, corrections):
    return corrections.get(mot, mot)
def process_image_data(image):
    data = ocr.ocr(image)
    num = process_num(data,image)
    nom = process_nom(data,image) 
    prenom = process_prenom(data,image)
    naissance = process_date(data,image)
    natio = corriger_mot(process_natio(data,image),corrections)
    sanction = check_sanction(nom, prenom, naissance, "française")
    
    output = {
        "type":"cinFRancienne",
        "nom" : nom,
        "prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        #"dateDelivrance": None,
        #"dateValidite" : None,
        "nationalite" : "française",
        "lieu" : None,
        "IdCin" : None,
        "sanction": sanction
    }

    return output



def run_CINFR_ancien2(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (570, 375))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_recto_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))
        
        # Supprimer l'image après avoir généré la sortie
    os.remove(cropped_recto_path)
    return output