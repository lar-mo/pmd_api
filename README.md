# Summary

## This is a Django project with two apps:

### pmd_strings

* This is a REST API that provides the content for pattymdesigns.com.
* It requires an API token which is enforced per view
* The versioning is done manually by adding more sections under app/views, app/serializer, proj/urls.
* The strings are offered in 4 languages: English, Spanish, French, German

### api_wrapper

* This is the API wrapper app for the three APIs that provide content for pattymdesigns.com.
  * _pmd_strings, Flickr, and Blogger (blogspot)_.
* It serves the API response without exposing the various API keys on the front end.
