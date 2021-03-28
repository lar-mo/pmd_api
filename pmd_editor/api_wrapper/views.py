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
    return HttpResponse(response)

def pmdv2DevGetStrings(request):
    pmd_dev_v2_api_key = get_secret('pmd_dev_v2_api_key')
    response = requests.get("http://127.0.0.1:8000/strings/v2/", headers={'Authorization': 'Api-Key '+pmd_dev_v2_api_key})
    return HttpResponse(response)

def pmdv2ProdGetStrings(request):
    pmd_prod_v2_api_key = get_secret('pmd_prod_v2_api_key')
    response = requests.get("http://api.pattymdesigns.com/strings/v2/", headers={'Authorization': 'Api-Key '+pmd_prod_v2_api_key})
    return HttpResponse(response)

def flickrApiGetArrangements(request):
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photosets.getPhotos',
            'user_id': '67858665@N00',
            'photoset_id': '72157718545940976',
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'extras': 'date_upload'
        }
    )
    return HttpResponse(response)

def flickrApiGetContainers(request):
    flickr_api_key = get_secret('flickr_api_key')
    response = requests.get('https://api.flickr.com/services/rest/?',
        params = {
            'method': 'flickr.photosets.getPhotos',
            'user_id': '67858665@N00',
            'photoset_id': '72157718562548688',
            'api_key': flickr_api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'extras': 'date_upload'
        }
    )
    return HttpResponse(response)

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
    return HttpResponse(response)

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
    return HttpResponse(response)

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
    return HttpResponse(response)
