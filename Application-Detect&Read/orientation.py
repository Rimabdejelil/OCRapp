from PIL import Image
import numpy as np
import torch
import albumentations as albu
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from iglovikov_helper_functions.utils.image_utils import load_rgb
from check_orientation.pre_trained_models import create_model
model = create_model("swsl_resnext50_32x4d")

def get_orientation(image_path):
    # Charger le modèle
    #model = create_model("swsl_resnext50_32x4d")
    model.eval()

    # Charger l'image
    image = load_rgb(image_path)

    # Définir les transformations
    transform = albu.Compose([albu.Resize(height=224, width=224), albu.Normalize(p=1)], p=1)

    temp = []
    for k in [0, 1, 2, 3]:
        x = transform(image=np.rot90(image, k))["image"]
        temp += [tensor_from_rgb_image(x)]

    with torch.no_grad():
        prediction = model(torch.stack(temp)).numpy()

    # Trouver l'index de la classe avec la probabilité la plus élevée
    max_index = np.argmax(prediction[0])

    return max_index