import json
import requests

resp=requests.get("https://api.spotprod.segmind.com/inference-model-information/list?segmind_model=True")
resp=json.loads(resp.text)['Inference Segmind Model Information List With Details']

filtered_data = []
for i in resp:
    if i['type']=="textToText" and 'image' in i['parameters']:
        i['type']='imageToText'
    if i['type'] == "textToVideo" and 'image' in i['parameters']:
        i['type']="imageToVideo"
    if i['type'] == "imageTOImage":
        i['type']="imageToImage"

    filtered_data.append(
        {
            'title': i['title'],
            'type': i['type'],
            'description': i['description'],
            'slug': i['slug'],
        }
    )


with open('models.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2)