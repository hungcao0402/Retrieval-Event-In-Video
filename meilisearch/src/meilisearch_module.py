import meilisearch
import json
import glob
import os
import tqdm

class MeiliSearch():
    def __init__(self, url: str = 'http://127.0.0.1:7701') -> None:
        self.client = meilisearch.Client(url, 'mmlab')

    def add_ocr(self, index_name, data_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/OCR2'):
        log_file = open('log.txt','w')
        index = self.client.index(index_name)

        save_path = 'ocr.json'
        if os.path.exists(save_path):
            print(f"The file {save_path} exists.")
            with open(save_path, 'r') as json_file:
                data = json.load(json_file)

            index.add_documents(data) 

        else:

            ocr_file = sorted(glob.glob(os.path.join(data_path, '*.json')))
            id = 0
            output = []
            for file in tqdm.tqdm(ocr_file):
                with open(file, 'r') as json_file:
                    data = json.load(json_file)
                video_id = os.path.basename(file).split('.')[0]
                for frame_id, label in data.items():
                    try:
                        ann = {
                            'id': id,
                            "frame": os.path.join(video_id,frame_id),
                            "text": label[0]['description']
                        }
                        output.append(ann)
                    except:
                        log_file.write(f'{file}: {frame_id}\n')
                    id+=1
            with open(save_path, 'w') as json_file:
                json.dump(output, json_file)

            index.add_documents(output) 

    def add_asr(self, index_name='asr', data_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/ASR'):
        save_path = 'asr.json'
        index = self.client.index(index_name)

        # self.client.index('movies').add_documents(movies)
        if os.path.exists(save_path):
            print(f"The file {save_path} exists.")
            json_file = open(save_path, encoding='utf-8')
            data = json.load(json_file)

            asr = []

            for i in data:
                asr.append({
                    'id' : int(i['id']),
                    'frame_start' : i['frame_start'],
                    'frame_end': i['frame_end'],
                    'video_id': i['video_id'],
                    'text': i['text'],
                })
            self.client.index(index_name).add_documents(asr)

        else:
            output = []
            asr_file = sorted(glob.glob(os.path.join(data_path, '*.json')))
            id = 0
            for file in tqdm.tqdm(asr_file):
                with open(file, 'r') as json_file:
                    data = json.load(json_file)
                video_id = os.path.basename(file).split('.')[0]
                for label in data:
                    ann = {
                        'id': id,
                        'video_id': str(video_id),
                        "frame_start": int(label['start']),
                        "frame_end": int(label['end']),
                        "text": label['text']
                    }
                    output.append(ann)

                    id+=1

                    self.client.index(index_name).add_documents(output)

                    break
                break
            with open(save_path, 'w') as json_file:
                json.dump(output, json_file)



    def search(self, index_name, query: str, topk: int, matchingStrategy: str) -> list:
        '''
        matchinStrategy:
            all - only returns documents that contain all query terms
            last - returns documents containing all the query terms first. If there are not enough results containing all query terms to meet the requested limit
        
        return list keyframe name: ['L01/L01_V018/0183', 'L01/L01_V019/0424', ...]
        '''
        index = self.client.index(index_name)
        result = index.search(query, {
                'limit': topk,
                'matchingStrategy': matchingStrategy
                })['hits']
        
        # result = [i['frame'] for i in result]
        
        return result

    def delete_index(self, name_index) -> None:
        self.client.delete_index(name_index)

        