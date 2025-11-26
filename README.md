# Summary

## This is a Django project with two apps:

### pmd_strings

* This is a REST API that provides the content for pattymdesigns.com.
* It requires an API token which is enforced per view
* The versioning is done manually by adding more sections under app/views, app/serializer, proj/urls.
* The strings are offered in 4 languages: English, Spanish, French, German

### api_wrapper

* This is the API wrapper app for the three APIs that provide content for pattymdesigns.com.
  * _pmd_strings_
  * _Flickr_
  * _Blogger_ (blogspot)
* It serves the API responses without exposing the various API keys on the front end.

### local dev

# Add pipenv to your PATH so you don't need the full path:
export PATH="$PATH:/Users/larrymoiola/Library/Python/3.9/bin"

# Activate the virtual environment
pipenv shell

# Run commands in the virtualenv without activating
pipenv run python manage.py runserver

# Install a new package
pipenv install <package-name>

# Install dev dependencies
pipenv install --dev <package-name>

# See installed packages
pipenv graph

# From the pmd_api directory:
cd pmd_editor

# Run server (always use --settings flag for local dev)
pipenv run python manage.py runserver --settings=pmd_editor.settings_local

# Run migrations
pipenv run python manage.py migrate --settings=pmd_editor.settings_local

# Create superuser
pipenv run python manage.py createsuperuser --settings=pmd_editor.settings_local

# Access Django shell
pipenv run python manage.py shell --settings=pmd_editor.settings_local
