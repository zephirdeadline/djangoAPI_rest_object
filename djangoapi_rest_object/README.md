## DEPENDANCE

- Django
- djangorestframework
- djoser
- djangorestframework-jwt


## INSTALLATION

in settings:

```
REQUIRE_API_AUTHORISATION = True
IS_GLOBAL_DATA = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```
Explication:

REQUIRE_API_AUTHORISATION = True If you want use an Authorization with your API
IS_GLOBAL_DATA = True If your data is NOT attached to a user

Warning: Both False are not compatible.


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
def car(request, id_car=None):
    return action(request, Car, CarSerializer, id_car)

```
4- Add 2 url for you model:
```
url(r'car/$', views.car, name='car'), # 'car'
url(r'car/(?P<id_car>\d+)$', views.car, name='carid'),
```

## API usage

Model example:

```
class Sms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.CharField(max_length=64)
    date = models.DateTimeField()
```

Add Header Token/jwt only if REQUIRE_API_AUTHORISATION = True


# Get a list of sms of a specific user:

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

# Get a sms :

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


### Create sms for a specific user:

> POST http://localhost:8000/api/sms/

HEADER needed: 

> Authorization: Token e0ae370xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

> Content-Type: application/json


BODY:

```
[
	{
		"sender": "Jacque",
		"date": "2008-04-10 11:47:58-05",
		"text": "je suis un sms"
	},
	...
]
```

RESPONSE:
```
{"status": "..."}
```

# Modify a sms :

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
	},
	

```

RESPONSE:

```
{"status": "..."}
```

# Delete a sms of a specific user:

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

# Fast using of identification

Comming...


