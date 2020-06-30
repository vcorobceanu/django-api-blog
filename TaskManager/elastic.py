import json
import requests
from elasticsearch import Elasticsearch


def indexing(task):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    r = requests.get('http://localhost:9200')

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
            '.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzODc0MzE5LCJqdGkiOiJ' \
            'hZDE2YTQ0M2U0M2M0MzYwODRlMGU2YzgzNmJkMzg5MiIsInVzZXJfaWQiOjF9.9ZawP' \
            'vbJIzb-R3wUgtnsdv8uq3XkWa_BRRtummVPXiU '
    headers = {'Authorization': 'Token ' + token}

    if r.status_code == 200:
        r = requests.get('http://localhost:8000/task/task/' + task.id, headers=headers)
        json_content = json.loads(r.content)

        for i in range(len(json_content)):
            es.index(index='search', id=i, doc_type='task', body=json_content[i])


def search(request):
    s_key = request.POST.get('abc')
    context = {}
    lis = []

    if s_key:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        query = es.search(
            index="search",
            body={'query': {'match': {'title': s_key}}}
        )['hits']
        sub = query['hits']

        for record in sub:
            source = record.get('_source', {})
            lis.append(dict(source))

    else:
        lis = None

    return lis

# # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# query = es.search(index="search",
#                   body={'query': {'match': {'title': 'a'}}})['hits']
# sub = query['hits']
# print(sub)
# source = []
# for record in sub:
#     source = record.get('_source', {})
#     print(source)
