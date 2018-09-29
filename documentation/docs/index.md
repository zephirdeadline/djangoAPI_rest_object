[![CircleCI](https://circleci.com/gh/zephirdeadline/djangoAPI_rest_object.svg?style=svg)](https://circleci.com/gh/zephirdeadline/djangoAPI_rest_object)

DOC: https://drive.w4pity.fr/drive/Rest_object_documentation.pdf

## DEPENDANCE

- Django
- djangorestframework
- djoser
- djangorestframework-jwt


## INSTALLATION

in settings:
Configure REST_FRAMEWORK for the authentification you want
```

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```
Tips: You can also you JWT

Add on your INSTALL_APP:

```
'rest_object',
'rest_framework',
'rest_framework_jwt',
'rest_framework.authtoken',
'djoser',
```

Add on your url path (identification, user management):

```    
url(r'^auth/', include('djoser.urls')),
url(r'^auth/', include('djoser.urls.authtoken')),
url(r'^auth/', include('djoser.urls.jwt')),
    
```



Usage:

1- Create your model ('Car' for example)
2- Create your class serializer for this model ('CarSerializer' for example)
3- Create a view for this model like this:
```
def car(request, id_car=None, cursor=None, amount=None):
    return action(request, Car, CarSerializer, id_car, cursor, amount, is_restricted=False, linked_to_user=False)

```
4- Add 2 url for you model:
```
url(r'car/$', views.car, name='car'), # 'car' 
url(r'car/(?P<id_car>\d+)$', views.car, name='carid'),
url(r'car/(?P<cursor>\d+)/(?P<amount>\d+)$', views.car, name='caramount'),
```

Tips: An Activity example is avaible in the source code

## API usage

Tips: Token can be replaced by JWT

Model example:


User is a ForeignKey, so is_restricted ans linked_to_user need to be set as True

```
class Sms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.CharField(max_length=64)
    date = models.DateTimeField()
```

Add Header Token/jwt only if you need it


### QUERY

> GET http://localhost:8000/api/sms/

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json


RESPONSE:

```
[
	{
	    "id": 1,
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	},
	...
]
```

### GET 

> GET http://localhost:8000/api/sms/{id}

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json

RESPONSE:

```
	{
	    "id": 1,
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	}
```


### POST

> POST http://localhost:8000/api/sms/

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json


BODY:

```
[
    saved: [
        {
            "sender": "Jacque",
            "date": "2008-04-10 11:47:58-05",
            "text": "je suis un sms"
        },
        ...
    ],
    fails: [
    ...
    ]
	
]
```

RESPONSE:
```
	{
	    "id": 1,
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	}
```


### PUT 


> PUT http://localhost:8000/api/sms/{id}

id: id of sms

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json

BODY:

```

	{
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	}
	

```

RESPONSE:

```

	{
	    "id": 5,
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	}
```

### Delete

> DELETE http://localhost:8000/api/sms/{id}

id: id of sms to delete

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json


RESPONSE:

```
{"status": "..."}
```

## IDENTIFICATION

Use Djoser documentation to add the identification in your project:

[Documention link](https://djoser.readthedocs.io/en/stable/)



