from models.realesrgan_model import RealESRGANModel
from models.realesrnet_model import RealESRNetModel

from .import models

import torch
from PIL import Image
from io import BytesIO
import numpy as np
import torchvision.transforms as transforms
opt = {
    'type': 'RealESRGANModel',  # Added type key with value 'RealESRGANModel'
    'num_gpu': 0,
    'is_train': False,
    'realesrgan_model_path': 'my_app.models.realesrgan_model.RealESRGANModel',
    'realesrnet_model_path': 'my_app.models.realesrnet_model.RealESRNetModel',
    'network_g': {
        'which_model_g': 'rrdb_net',
        'num_feat': 64,
        'num_block': 23,
        'num_input_channels': 3,
        'num_output_channels': 3,
        'upscale': 4
    }
}
def enhance_image(image):
    # Load the ESRGAN model model = RealESRNetModel(opt)  # Initialize the model with appropriate options

    # Preprocess the image
    image = Image.open(image)
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    image = preprocess(image).unsqueeze(0)

    # Enhance the image
    models.eval()
    with torch.no_grad():
        enhanced_image = models(image)

    # Postprocess the enhanced image
    enhanced_image = enhanced_image.squeeze().cpu().detach().numpy()
    enhanced_image = np.clip(enhanced_image * 255.0, 0, 255).astype(np.uint8)
    enhanced_image = Image.fromarray(enhanced_image.transpose(1, 2, 0))

    # Convert the enhanced image to bytes
    enhanced_image_bytes = BytesIO()
    enhanced_image.save(enhanced_image_bytes, format='JPEG')
    return enhanced_image_bytes.getvalue()

