from meilisearch_module import MeiliSearch

meili = MeiliSearch()

result = meili.add_ocr(index_name = 'ocr')
result = meili.add_asr(index_name = 'asr')

# result = meili.search('asr', 'không được', topk=100, matchingStrategy='all')
# result = meili.delete_index(name_index='asr')

print(result)