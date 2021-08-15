from django.shortcuts import render
from django.http import HttpResponse

import requests

import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

def pmdv1dev(request):
    response = requests.get("http://127.0.0.1:8000/strings/v1/")
    return HttpResponse(response, content_type='application/json')

def pmdv2DevGetStrings(request):
    pmd_dev_api_key = get_secret('pmd_dev_api_key')
    response = requests.get("http://127.0.0.1:8000/strings/v2/", headers={'Authorization': 'Api-Key '+pmd_dev_api_key})
    return HttpResponse(response, content_type='application/json')

def pmdv2ProdGetStrings(request):
    pmd_prod_api_key = get_secret('pmd_prod_api_key')
    response = requests.get("https://api.pattymdesigns.com/strings/v2/", headers={'Authorization': 'Api-Key '+pmd_prod_api_key})
    return HttpResponse(response, content_type='application/json')

def pmdv3DevGetStrings(request):
    pmd_dev_api_key = get_secret('pmd_dev_api_key')
    response = requests.get("http://127.0.0.1:8000/strings/v3/", headers={'Authorization': 'Api-Key '+pmd_dev_api_key})
    return HttpResponse(response, content_type='application/json')

def pmdv3ProdGetStrings(request):
    pmd_prod_api_key = get_secret('pmd_prod_api_key')
    response = requests.get("https://api.pattymdesigns.com/strings/v3/", headers={'Authorization': 'Api-Key '+pmd_prod_api_key})
    return HttpResponse(response, content_type='application/json')

def flickrApiGetArrangements(request):
    flickr_user_id = get_secret('flickr_user_id')
    flickr_arrangements_photoset_id = get_secret('flickr_arrangements_photoset_id')
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photosets.getPhotos',
            'user_id': flickr_user_id,
            'photoset_id': flickr_arrangements_photoset_id,
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'extras': 'date_upload'
        }
    )
    arrangements_json = response.json().pop('photoset').pop('photo')
    arrangements_ids = [ arrangements_json[i].pop('id') for i in range(len(arrangements_json)) ]
    arrangements_json_sanitized = json.dumps(arrangements_ids, indent = 4)
    # The following line of code combines a list comprehension (63) AND a data structure conversion (64) into a one-liner
    ### photo_json_sanitized = json.dumps([ photo_json[i].pop('id') for i in range(len(photo_json)) ], indent = 4)
    return HttpResponse(arrangements_json_sanitized, content_type='application/json')
    # return HttpResponse(response, content_type='application/json') # OG: returns everything including sensitive data

def flickrApiGetContainers(request):
    flickr_user_id = get_secret('flickr_user_id')
    flickr_containers_photoset_id = get_secret('flickr_containers_photoset_id')
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photosets.getPhotos',
            'user_id': flickr_user_id,
            'photoset_id': flickr_containers_photoset_id,
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'extras': 'date_upload'
        }
    )
    containers_json = response.json().pop('photoset').pop('photo')
    containers_ids = [ containers_json[i].pop('id') for i in range(len(containers_json)) ]
    containers_json_sanitized = json.dumps(containers_ids, indent = 4)
    return HttpResponse(containers_json_sanitized, content_type='application/json')

def flickrApiGetSizes(request, photo_id):
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photos.getSizes',
            'photo_id': photo_id, # 51014286417
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1
        }
    )
    sizes_json = response.json().pop('sizes').pop('size')
    for i in range(len(sizes_json)):
        if sizes_json[i]['label'] == 'Small':
            thumb = {
                'url': sizes_json[i]['source'],
                'width': sizes_json[i]['width'],
                'height': sizes_json[i]['height'],
            }
    full = {
        'url': sizes_json[-1]['source'],
        'width': sizes_json[-1]['width'],
        'height': sizes_json[-1]['height'],
    }
    thumb_and_full = {'thumb': thumb, 'full': full}
    sizes_json_sanitized = json.dumps(thumb_and_full, indent = 4)
    return HttpResponse(sizes_json_sanitized, content_type='application/json')

def flickrApiGetInfo(request, photo_id):
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photos.getInfo',
            'photo_id': photo_id, # 51014286417
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1
        }
    )
    photo_description = response.json().pop('photo').pop('description').pop('_content')
    photo_description_sanitized = json.dumps(photo_description, indent = 4)
    return HttpResponse(photo_description_sanitized, content_type='application/json')

def bloggerApiGetLatestPost(request):
    blogger_apiv3 = get_secret('blogger_apiv3')
    response = requests.get("https://www.googleapis.com/blogger/v3/blogs/6624714559657687469/posts?",
        params = {
            'key': blogger_apiv3,
            'fetchBodies': 'true',
            'fetchImages': 'true',
            'maxResults': 1,
            'orderBy': 'PUBLISHED',
        }
    )
    return HttpResponse(response, content_type='application/json')
