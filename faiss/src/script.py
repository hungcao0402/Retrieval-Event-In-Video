import numpy as np
import faiss
import time
import json
from PIL import Image
import os
import glob

from modules import Encoder, Faiss

# Testing

database = np.load('data/CLIP_Features_ViT_B16.npy')
print('Database shape', database.shape)

start_time = time.time()
faiss_searcher = Faiss(database)
print('Index time:', time.time() - start_time)

start_time = time.time()
encoder = Encoder()
print('Load model time:', time.time() - start_time)
start_time = time.time()
queries = np.array(['A big cat'])
encoded_text = encoder.encode_texts(queries)
print('Encode time:', time.time() - start_time)

start_time = time.time()
result_indices = faiss_searcher.search(encoded_text, top_k=10).ravel()
print('Search time:', time.time() - start_time)
print(result_indices[0])

with open('data/keyframe_names') as f:
    keyframe_names = json.load(f)
result = [keyframe_names[i] for i in result_indices]
print(result)

for file in glob.glob('faiss/result/*'):
    os.remove(file)
os.makedirs('faiss/result/', exist_ok=True)
for image_file in result:
    img = Image.open(image_file)
    img.save(os.path.join('faiss/result', os.path.basename(image_file)))