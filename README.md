# Poisense

Poisense helps to identify the hazardous and poisonous ingredients in the home so that you and your loved ones could be safe

## Link

www.poisense.tech

### Prerequisites

Create an Virtual Environment for Django

```
py -m pip install --user virtualenv
py -m venv env
```
Activate the Virtual Environment that you have created

```
.\(name of the venv)\Scripts\activate
```

### Installing

Setup the git within your Django Project Root

```
git init
```
Create appropriate runtime.txt and requirements.txt file. Heroku Buildpack for OpenCV must be installed prior.

```
heroku buildpacks:add --index 1 heroku-community/apt
```

### pushing code to heroku
1. login to heroku from command prompt
```
heroku login
```
2. Pushing the files to heroku
```
git add .
git commit -am "update poisense"
git push heroku master
```

### Pulling from heroku
1. Login to heroku from command prompt
2. Then run the following command
```
heroku git:clone -a poisenseheroku
```

### To restart Heroku
```
heroku dyno:restart poisenseheroku
```

### To Shutdown Heroku
```
heroku dyno:stop poisenseheroku
```

### Fixing/updating final database output
For chemical sense poisenseapp -> go to database_extract.py to alter the database extraction format or any new info to be displayed.
Similarily for food sense go yo allergy_database_extract.py to alter the database extraction format or any new info to be displayed.

### Image detection API
For any issues in the image detection API, We can access the image_detection.py and allergy_image_detection.py files to fix the errors or update the API keys in them

## Running the tests

Image could be uploaded for testing the ingredients through text detection API or ingredients could be manually fed in text input


## Deployment

GIT push it in the heroku master

```
git push heroku master
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Heroku](https://www.heroku.com/) - Hosting
* [Bootstrap](https://getbootstrap.com/) - UI Design


