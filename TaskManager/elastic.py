import json
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')

# # # indexing # # # #
# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
#         '.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzODc0MzE5LCJqdGkiOiJ' \
#         'hZDE2YTQ0M2U0M2M0MzYwODRlMGU2YzgzNmJkMzg5MiIsInVzZXJfaWQiOjF9.9ZawP' \
#         'vbJIzb-R3wUgtnsdv8uq3XkWa_BRRtummVPXiU '
# headers = {'Authorization': 'Token ' + token}
#
# if r.status_code == 200:
#     r = requests.get('http://localhost:8000/task/task/', headers=headers)
#     json_content = json.loads(r.content)
#     for i in range(len(json_content)):
#         es.index(index='search', id=i, doc_type='task', body=json_content[i])
#
# # # # # # # # # # #

# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
query = es.search(index="search",
                  body={'query': {'match': {'title': 'a'}}})['hits']
sub = query['hits']
print(sub)
source = []
for record in sub:
    source = record.get('_source', {})
    print(source)
