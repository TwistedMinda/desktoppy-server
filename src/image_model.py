from diffusers import StableDiffusionPipeline
import torch

def create_image(prompt: str, output: str):
  model_id = "stabilityai/stable-diffusion-2"
  cuda_enabled = torch.cuda.is_available()
  device = "cuda" if cuda_enabled else "cpu"
  try:
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16) if cuda_enabled else StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)
    
    image = pipe(prompt).images[0]
    image.save(output)
  except Exception as e:
    print(f"Error creating image '{output}'", e)
