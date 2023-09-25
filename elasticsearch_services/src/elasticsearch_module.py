from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import glob
import tqdm
import json
from elasticsearch import helpers

class ElasticSearch():
    def __init__(self, host : str = "localhost", port : int = 9200) -> None:
        self.client  = Elasticsearch(
            "http://localhost:9200",
        )
        print(self.client.info())

    def indexer(index_name):
        es_client = Elasticsearch(hosts=[{"host": "example_es"}])
        index_name = "example"
        number_of_shards = 1
        es_params = {
                "index": index_name,
                "body": {
                    "settings": {"index": {"number_of_shards": number_of_shards}}
                },
            }
        if es_client.indices.exists(index=index_name):
            es_client.indices.delete(index=index_name)
        es_client.indices.create(**es_params)
        bulk(
            es_client,
            df_index.to_dict(orient="records"),
            index=index_name,
        )


    def add_ocr(self, data_path, index_name):
        # self.client.indices.create(index=index_name)

        ocr_file = sorted(glob.glob(os.path.join(data_path, '*.json')))
        id = 0
        for file in tqdm.tqdm(ocr_file):
            with open(file, 'r') as json_file:
                data = json.load(json_file)
            video_id = os.path.basename(file).split('.')[0]
            for frame_id, label in data.items():
                try:
                    response = self.client.index(index=index_name,  # Thay 'ten_chi_muc' bằng tên chỉ mục bạn muốn sử dụng
                                                id=id,  # ID của tài liệu (nếu không có, Elasticsearch sẽ tự động tạo)
                                                document={
                                                    "frame": os.path.join(video_id,frame_id),
                                                    "text": label[0]['description'],
                                                }

                                                )
                    
                    # # Kiểm tra xem việc ingest tài liệu có thành công không
                    if response['result'] == 'created':
                        pass
                        print(f'Tài liệu {id} đã được ingest thành công.')
                        
                    else:
                        print(f'Tài liệu {id} ingest thất bại.')
                                
                    id+=1
                except:
                    continue

    def add_asr(self, index_name='asr', data_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/ASR'):
        save_path = 'asr.json'

        output = []
        asr_file = sorted(glob.glob(os.path.join(data_path, '*.json')))
        id = 0
        for file in tqdm.tqdm(asr_file):
            with open(file, 'r') as json_file:
                data = json.load(json_file)
            video_id = os.path.basename(file).split('.')[0]
            for label in data:
                ann = {
                    'video_id': video_id,
                    "frame_start": int(label['start']),
                    "frame_end": int(label['end']),
                    "text": label['text']
                }
                response = self.client.index(index=index_name,  # Thay 'ten_chi_muc' bằng tên chỉ mục bạn muốn sử dụng
                                            id=id,  # ID của tài liệu (nếu không có, Elasticsearch sẽ tự động tạo)
                                            document=ann
                )
                if response['result'] == 'created':
                    pass
                    print(f'Tài liệu {id} đã được ingest thành công.')
                    
                else:
                    print(f'Tài liệu {id} ingest thất bại.')
                            

                id+=1


    
    def search(self, index_name, query: str, topk: int) -> list:
        #'https://coralogix.com/blog/42-elasticsearch-query-examples-hands-on-tutorial/'
        #'Các chiến lược ở đây, nếu cần gì thì tìm thử'
        search_query = {
                "size": topk,  # Số lượng kết quả bạn muốn lấy
                "query": {
                    "match_phrase": {
                        "text": query  # Truy vấn tìm kiếm trong trường "ocr_text"
                    }
                }
            }
        search_results = self.client.search(index = index_name,body = search_query)
        hits = search_results['hits']['hits']
        # results = [hit['frame_id'] for hit in hits]
        return hits
    
    def delete_index(self, index_name):
        if self.client.indices.exists(index=index_name):
            self.client.indices.delete(index=index_name)



                    
                    




