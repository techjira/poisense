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


