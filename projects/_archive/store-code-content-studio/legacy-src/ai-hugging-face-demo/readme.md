
# DOWNLOAD AI MODELS
- models take up a lot of space so be aware it will save in your .cache folder
- `C:\Users\USERNAME\.cache\huggingface`




# DIFFUSERS REQUIRE CUDA
- pytorch requires cuda to be turned on... this means youll need the correct version of pytorch
    - `pip uninstall torch torchvision`
    - `pip install torch==2.0.1+cu118 -f https://download.pytorch.org/whl/cu118/torch_stable.html`
    - `pip install torchvision`
    - `pip install opencv-python`




# ONLINE NOTEBOOKS
- running some of these models gives local issues but just run them on google co loab notebooks
- [GOOGLE NOTEBOOK](https://colab.research.google.com/drive/1_lnyxzPZCQ7LVTb4d38NUwFEykbDPZc-?usp=sharing)



```
Transformers: Pretrained models for NLP tasks.
Diffusers: Diffusion models for image and audio generation.
Datasets: Access to datasets for computer vision, audio, and NLP.
Inference API: Free API to experiment with over 200k models.
Tokenizers: Fast tokenizers optimized for research and production.
Accelerate: Tools for multi-GPU, TPU, and mixed-precision training.
```