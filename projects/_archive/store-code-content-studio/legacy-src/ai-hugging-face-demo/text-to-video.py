# pip install torch==2.0.1+cu118 torchvision -f https://download.pytorch.org/whl/cu118/torch_stable.html


import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video




# USE CPU
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")





pipe = DiffusionPipeline.from_pretrained("cerspense/zeroscope_v2_576w", torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

prompt = "Darth Vader is surfing on waves"
video_frames = pipe(prompt, num_inference_steps=40, height=320, width=576, num_frames=24).frames
video_path = export_to_video(video_frames, output_video_path=".")
