import re
import time
from test import ocr
#from app import check_sanction

def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

#from paddleocr import PaddleOCR
#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')

def extract_date(text):
    pattern = r'(\d{2}[.\s/-1]?\d{2}[.\s/-1]?\d{4})'


    ##match = re.search(pattern, text)
    
    # Find all matches in the remaining text
    matches = re.findall(pattern, text)
    
    for match in matches:
        # Remove any non-numeric characters from the matched date
        date_without_delimiters = re.sub(r'[^\d]', '', match)
        
        # Check if the cleaned date has the correct format
        if (len(date_without_delimiters) == 8) :
            formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
            return(formatted_date)
        elif (len(date_without_delimiters) == 10):
            formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[3:5]}/{date_without_delimiters[6:]}"
            return formatted_date
    
    # If no valid date is found, return None
    return None

def naissance(text):
    # Remove the first 10 digits from the input
    text = text[10:]
    
    # Define a pattern to match the date in various formats
    pattern = r'(\d{2}[.\s/-]?\d{2}[.\s/-]?\d{4})'
    
    # Find all matches in the remaining text
    matches = re.findall(pattern, text)
    
    for match in matches:
        # Remove any non-numeric characters from the matched date
        date_without_delimiters = re.sub(r'[^\d]', '', match)
        
        # Check if the cleaned date has the correct format
        if len(date_without_delimiters) == 8:
            formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
            return formatted_date
    
    # If no valid date is found, return None
    return None

def process_naissance(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if naissance(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if naissance(text):
                box = data[0][i]
                date = naissance(box[1][0])
                #formatted_date = date.replace(".", "/")  # Convertir . en /
                return date
                
    else:
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])

def process_validite(data,image):
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
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        

def process_deliv(data,image):
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
                if count_dates == 3 :
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
        points = [(227, 278), (380, 278), (380, 307), (227, 307)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return resultat2[0][0][1][0]


def extract_nom_prenom(data):
    nom = ""
    prenom = ""

    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if text.endswith("<<<<<"):
            parts = text.split("<<")
            #if len(parts) == 2:
            nom = parts[0]  # Supprime "P<TUN" du début
            prenom = parts[1]

            nom = nom.replace("<", " ")
            prenom = prenom.replace("<", " ")
            break

    return nom, prenom       

def process_image_data(image):
    data=ocr.ocr(image)
    
    #print(data)
    num = process_num(data,image)
    #nom = process_nom(data,image) 
    #prenom = process_prenom(data,image)
    naissance = process_naissance(data,image)
    validité = process_validite(data,image)
    delivrance = process_deliv(data,image)

    
    output = {
        "type":"titreSejourFRancien",
        #"nom" : nom,
        #"prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        "dateDelivrance": delivrance,
        "dateValidite" : validité,
        "nationalite" : "tunisienne",
        "lieu" : None,
        "IdCin" : None,
        #"sanction":None
        
    }

    return output

import cv2
import os
def run_sejourAncien(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (697,433))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_recto_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))

    os.remove(cropped_recto_path)
    return output
