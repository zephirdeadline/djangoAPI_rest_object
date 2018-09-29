from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient


# Create your tests here.
from exemple.models import Car, CarUser


class NoIdentification(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/car/'


    # Good tests
    def test_post_a_car(self):
        request = self.client.post(self.url, [{'name': 'newCar2000', "maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 1)


    def test_post_two_cars(self):
        request = self.client.post(self.url, [{'name': 'newCar2001', "maxspeed": 150},
                                                 {'name': 'newCar2002', "maxspeed": 160}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 2)

    def test_post_a_cars_more_field_than_requierd(self):
        request = self.client.post(self.url, [{'name': 'newCar2003', "maxspeed": 150, "power": 50}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 1)

    def test_get_all_cars(self):
        request = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), len(Car.objects.all()))

    def test_put_car(self):
        car = self.client.get(self.url).data[0]
        id = car.pop('id')
        request = self.client.put(self.url + str(id), {"name": car['name'], "maxspeed": 2000}, format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(request.data['name'], car['name'])
        self.assertNotEqual(request.data['maxspeed'], car['maxspeed'])
        car = self.client.get(self.url + str(id)).data
        self.assertEqual(request.data['name'], car['name'])
        self.assertEqual(request.data['maxspeed'], 2000)

    def test_delete_car(self):
        request = self.client.get(self.url + str(1))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = self.client.delete(self.url + str(1))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = self.client.get(self.url + str(1))
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_more_field_car(self):
        request = self.client.put(self.url + str(1), {"name": "newCar2000", "maxspeed": 180, "power": 10}, format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_get_with_amount(self):
        request = self.client.get('/api/car/0/2')
        self.assertEqual(len(request.data), 2)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_with_big_amount(self):
        request = self.client.get('/api/car/0/9999999')
        self.assertEqual(len(request.data), len(Car.objects.all()))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_with_bad_cursor(self):
        request = self.client.get('/api/car/5555/2')
        self.assertEqual(len(request.data), 0)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    # Bad tests

    def test_post_a_bad_field_car(self):
        request = self.client.post(self.url, [{'fullname': 'newCar2000', "maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 1)
        self.assertEqual(len(request.data['saved']), 0)

    def test_post_two_bad_cars(self):
        request = self.client.post(self.url, [{'fullname': 'newCar2000', "maxspeed": 180},
                                                 {'fullname': 'newCar2006', "maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 2)
        self.assertEqual(len(request.data['saved']), 0)

    def test_post_a_bad_cars_and_a_good_car(self):
        request = self.client.post(self.url, [{'name': 'newCar2003', "maxspeed": 180},
                                                 {'fullname': 'newCar2006', "maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 1)
        self.assertEqual(len(request.data['saved']), 1)

    def test_post_a_missed_field_car(self):
        request = self.client.post(self.url, [{"maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 1)
        self.assertEqual(len(request.data['saved']), 0)

    def test_delete_bad_car(self):
        request = self.client.delete(self.url + str(999))
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_bad_id(self):
        request = self.client.get(self.url + str(999))
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_bad_field_car(self):
        request = self.client.put(self.url + str(1), {'fullname': 'newCar2000', "maxspeed": 180}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_bad_methode(self):
        request = self.client.patch("/api/car/")
        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class WithIdentification(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = APIClient()
        user = self.client.post("/auth/users/create/", {"username": "userTester", "password": "test11234"})
        self.token = self.client.post("/auth/jwt/create/", {"username": "userTester",	"password": "test11234"}).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + self.token)


    def test_auh_get_all_cars(self):
        request = self.client.get('/api/carwithauth/')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), len(Car.objects.all()))


    # bad test
    def test_bad_auh_get_all_cars(self):
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + self.token + "bad")
        request = self.client.get('/api/carwithauth/', )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, request.status_code)


class LinkedToUser(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/caruser/'
        self.userId = self.client.post("/auth/users/create/", {"username": "userTester", "password": "test11234"}).data['id']
        self.token = self.client.post("/auth/jwt/create/", {"username": "userTester", "password": "test11234"}).data[
            'token']
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + self.token)

        self.client.post(self.url, [{'name': 'car1', "maxspeed": 180}], format='json')
        self.client.post(self.url, [{'name': 'newCar2000', "maxspeed": 180}], format='json')
        self.client.post(self.url, [{'name': 'newCar2005', "maxspeed": 220}], format='json')
        
    # Good tests
    def test_post_a_car(self):
        request = self.client.post(self.url, [{'name': 'newCar2000', "maxspeed": 180}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 1)

    def test_post_two_cars(self):
        request = self.client.post(self.url, [{'name': 'newCar2001', "maxspeed": 150},
                                              {'name': 'newCar2002', "maxspeed": 160}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 2)

    def test_post_a_cars_more_field_than_requierd(self):
        request = self.client.post(self.url, [{'name': 'newCar2003', "maxspeed": 150, "power": 50}], format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(len(request.data['fails']), 0)
        self.assertEqual(len(request.data['saved']), 1)

    def test_get_all_cars(self):
        request = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(len(request.data), len(CarUser.objects.filter(user_id=self.userId)))

    def test_put_car(self):
        car = self.client.get(self.url).data[0]
        id = car.pop('id')
        request = self.client.put(self.url + str(id), {"name": car['name'], "maxspeed": 20000}, format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(request.data['name'], car['name'])
        self.assertNotEqual(request.data['maxspeed'], car['maxspeed'])
        car = self.client.get(self.url + str(id)).data
        self.assertEqual(request.data['name'], car['name'])
        self.assertEqual(request.data['maxspeed'], 20000)

    def test_delete_car(self):
        car = CarUser.objects.filter(user_id=self.userId)[0].id
        request = self.client.get(self.url + str(car))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = self.client.delete(self.url + str(car))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = self.client.get(self.url + str(car))
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_more_field_car(self):
        car = CarUser.objects.filter(user_id=self.userId)[0].id
        request = self.client.put(self.url + str(car), {'name': 'newCar2000', "maxspeed": 180, "power": 10},
                                  format='json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_get_with_amount(self):
        request = self.client.get(self.url + '0/2')
        self.assertEqual(len(request.data), 2)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_with_big_amount(self):
        request = self.client.get(self.url + '0/9999999')
        self.assertEqual(len(request.data), len(CarUser.objects.filter(user_id=self.userId)))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_with_bad_cursor(self):
        request = self.client.get(self.url + '5555/2')
        self.assertEqual(len(request.data), 0)
        self.assertEqual(request.status_code, status.HTTP_200_OK)