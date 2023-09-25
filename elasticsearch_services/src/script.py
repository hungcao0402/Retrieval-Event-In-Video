from elasticsearch_module import ElasticSearch
es = ElasticSearch()

# es.add_ocr(data_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/OCR2',index_name='ocr')
# es.add_asr(data_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/ASR',index_name='asr')

rs = es.search(index_name='asr', query='ba phương tiện nằm ngỗn ngang', topk=10)    

print(rs)


