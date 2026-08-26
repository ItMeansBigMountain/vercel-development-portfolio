import torch
from diffusers import DiffusionPipeline

class ImageGenerator:
    def __init__(self, model_name, cache_dir=None):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.pipeline = DiffusionPipeline.from_pretrained(model_name, cache_dir=cache_dir).to(self.device)

    def generate_image(self, text):
        if not text:
            raise ValueError("Text input is empty or None.")
        
        # Generate the image using the DiffusionPipeline
        with torch.no_grad():
            result = self.pipeline(text)
        
        image_tensor = result.images[0]   
        return image_tensor

# Uncomment the following line if you want to set the default tensor type to CUDA
# torch.set_default_tensor_type('torch.cuda.FloatTensor')
