
import json
from watson_developer_cloud import DiscoveryV1



url= "https://gateway.watsonplatform.net/discovery/api"
username= "dabe840f-7be5-48c4-ae2b-f060691e9dbd"
password= "pD5FxMUBIpvp"
  
discovery = DiscoveryV1(
  username=username,
  password=password,
  version="2017-10-16"
)

#response = discovery.create_environment(
#  name="my_environment",
#  description="My environment",
#  size=1
#)

environments = discovery.get_environments()
print(json.dumps(environments, indent=2))

news_environments = [x for x in environments['environments'] if x['name'] == 'Watson System Environment']
news_environment_id = news_environments[0]['environment_id']
#print(json.dumps(news_environment_id, indent=2))

collections = discovery.list_collections(news_environment_id)
news_collections = [x for x in collections['collections']]
#print(json.dumps(collections, indent=2))

#qopts = {'query': 'mario oddessey'}
#my_query = discovery.query('system', 'news', qopts)
#print(json.dumps(my_query, indent=2))
#a=json.dumps(my_query, indent=2)

def get_query(text):
    qopts = {'query': text}
    my_query = discovery.query('system', 'news', qopts)
    return my_query

def get_query1(text, count):
    qopts = {'query': text, 'count':count}
    my_query = discovery.query('system', 'news', qopts)
    return my_query

def top_articles(text):
    my_query=get_query(text)  
    a={my_query['results'][i]['title']:my_query['results'][i]['url'] for i in range(len(my_query['results']))}
    return a

def get_sentiments(text, count):
    my_query=get_query1(text, count)  
    a={str(my_query['results'][i]['enriched_text']['sentiment']['document']['label']):0 for i in range(len(my_query['results']))}
    for i in range(len(my_query['results'])):
        a[str(my_query['results'][i]['enriched_text']['sentiment']['document']['label'])]+=1
    return a

def get_hashtags(text):
    my_query=get_query(text)     
    a={}
    for i in range(len(my_query['results'])):
        for j in range(len(my_query['results'][i]['enriched_text']['keywords'])):
            a[my_query['results'][i]['enriched_text']['keywords'][j]['text']]=0
    
    for i in range(len(my_query['results'])):
        for j in range(len(my_query['results'][i]['enriched_text']['keywords'])):
            a[my_query['results'][i]['enriched_text']['keywords'][j]['text']]+=1
    return a