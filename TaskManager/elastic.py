import requests
from elasticsearch import Elasticsearch
from django.contrib.auth.models import User


def indexing(task):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    r = requests.get('http://localhost:9200')

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
            '.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzODc0MzE5LCJqdGkiOiJ' \
            'hZDE2YTQ0M2U0M2M0MzYwODRlMGU2YzgzNmJkMzg5MiIsInVzZXJfaWQiOjF9.9ZawP' \
            'vbJIzb-R3wUgtnsdv8uq3XkWa_BRRtummVPXiU '
    headers = {'Authorization': 'Token ' + token}

    content = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "is_started": task.is_started,
        "author": User.objects.get(username=task.author).id,
        "assigned": User.objects.get(username=task.assigned).id
    }

    if r.status_code == 200:
        es.index(index='search', id=task.id, doc_type='task', body=content)


def search(request):
    s_key = request.POST.get('abc')
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

        for i in range(len(lis)):
            lis[i]['assigned'] = User.objects.get(id=lis[i]['assigned']).username
            lis[i]['author'] = User.objects.get(id=lis[i]['author']).username

    else:
        lis = None

    return lis


def delete_task_index(task):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    r = requests.get('http://localhost:9200')

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
            '.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzODc0MzE5LCJqdGkiOiJ' \
            'hZDE2YTQ0M2U0M2M0MzYwODRlMGU2YzgzNmJkMzg5MiIsInVzZXJfaWQiOjF9.9ZawP' \
            'vbJIzb-R3wUgtnsdv8uq3XkWa_BRRtummVPXiU '
    headers = {'Authorization': 'Token ' + token}

    if r.status_code == 200:
        es.indices.delete(id=task.id)

# # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# query = es.search(index="search",
#                   body={'query': {'match': {'title': 'a'}}})['hits']
# sub = query['hits']
# print(sub)
# source = []
# for record in sub:
#     source = record.get('_source', {})
#     print(source)


# r = requests.get('http://localhost:8000/task/task/' + str(task.id), headers=headers)
# print(r.content)
# json_content = json.loads(r.content)
# print(json_content)
