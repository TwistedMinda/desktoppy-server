from diffusers import StableDiffusionPipeline
import torch

model_id = "stabilityai/stable-diffusion-2"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

prompt = "An ancient library with many books and scrolls. The room is dimly lit by a few candles."
image = pipe(prompt).images[0]

image.save("output.png")