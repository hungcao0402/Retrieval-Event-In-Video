from meilisearch_module import MeiliSearch

meili = MeiliSearch()

result = meili.add_asr(index_name = 'asr')
# result = meili.search('asr2', 'không được', topk=100, matchingStrategy='all')
# result = meili.delete_index(name_index='asr')

print(result)