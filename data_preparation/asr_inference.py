import tqdm

import whisper
import time
import glob
import os
import json
import torch

save_dir = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/ASR'

model = whisper.load_model("medium")

import pandas as pd

fps_map = {}
for file in glob.glob('/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Map_Keyframes/*.csv'):
    video_id = os.path.basename(file).split('.')[0]
    try:
        df = pd.read_csv(file)
        fps_map[video_id] = float(df.loc[0, 'fps'])
    except:
        continue

def process_video(video_folder_path):
    video_id = os.path.basename(video_folder_path)

    list_mp3_file = sorted(glob.glob(os.path.join(video_folder_path, '*')))
    save_path = os.path.join(save_dir, video_id+'.json')
    print(save_path)
    if os.path.exists(save_path):
        return
    output = []
    output2 = []
    for file in tqdm.tqdm(list_mp3_file):
        try:
            with torch.no_grad():
                result = model.transcribe(file)
        except:
            with open('log_convert_asr.txt', 'a') as f:
                f.write(file+'\n')
            continue
        start, end = os.path.basename(file).split('.')[0].split('_')

        output2.append({'start': int(start),
                    'end': int(end),
                    'text': result['text']})

        for element in result['segments']:
            output.append({
                    'start': int(element['start'] * fps_map[video_id] + int(start)),
                    'end': int(element['end'] * fps_map[video_id] + int(start)),
                    'text': element['text']
            })

    with open(save_path, "w") as json_file:
        json.dump(output, json_file)

    save_path2 = os.path.join(save_dir+'30s', video_id+'.json')
    with open(save_path2, "w") as json_file:
        json.dump(output2, json_file)


list_video = sorted(glob.glob('/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data_preparation/asr_batch3/*'))    #3090_1

print(list_video)

for video in tqdm.tqdm(list_video):
    process_video(video)