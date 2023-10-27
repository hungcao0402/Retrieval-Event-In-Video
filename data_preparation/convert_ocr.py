import pandas as pd
import json
import glob
import os
import logging
import tqdm
ocr_path = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/OCR'
path_map = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Map_Keyframes'

file = open('log_convert_ocr.txt', 'w')

for file_csv in tqdm.tqdm(sorted(glob.glob(os.path.join(path_map, '*')))):
    video_id = os.path.basename(file_csv).split('.')[0]

    data_map = pd.read_csv(file_csv)
    list_map = data_map['frame_idx'].to_list()
    ocr_file = os.path.join(ocr_path, video_id+'.json')

    with open(ocr_file, 'r') as json_file:
        data = json.load(json_file)
    new_dict = dict()
    for frame_id, label in data.items():
        new_name = str(int(list_map[int(frame_id)-1])).zfill(8) +'.jpg'
        new_dict[new_name] = label

    with open(os.path.join('/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/OCR2', os.path.basename(ocr_file)), "w", encoding="utf-8") as json_file2:
        json.dump(new_dict, json_file2, indent=4)

