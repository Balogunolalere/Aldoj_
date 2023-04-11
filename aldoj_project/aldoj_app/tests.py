from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Property, Investment, Crop
from .serializers import PropertySerializer, InvestmentSerializer, CropSerializer
from django.contrib.auth.models import User


class PropertyTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpassword')
        self.property = Property.objects.create(title='Test Property', property_type='AG', description='Test property description', location='Test location', area=100, price=5000)

    def test_get_all_properties(self):
        """
        Ensure we can retrieve all properties.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('property_list_create'))
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_property(self):
        """
        Ensure we can create a new property.
        """
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'New Property',
            'property_type': 'RE',
            'description': 'New property description',
            'location': 'New location',
            'area': 50,
            'price': 10000
        }
        response = self.client.post(reverse('property_list_create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_property_detail(self):
        """
        Ensure we can retrieve a single property's details.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('property_detail', kwargs={'pk': self.property.pk}))
        property = Property.objects.get(pk=self.property.pk)
        serializer = PropertySerializer(property)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class InvestmentTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpassword')
        self.property = Property.objects.create(
            property_type='Agricultural',
            title='Test Property',
            description='Test Property Description',
            location='Test Location',
            area=100,
            price=100000
        )
        self.investment = Investment.objects.create(
            property=self.property,
            investor=self.user,
            amount=5000  # Add a value for the amount field here
        )


    def test_get_all_investments(self):
        """
        Ensure we can retrieve all investments.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('investment_list_create'))
        investments = Investment.objects.all()
        serializer = InvestmentSerializer(investments, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_investment(self):
        """
        Ensure we can create a new investment.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'property': self.property.pk,
            'investor': self.user.pk,
            'amount': 5000  # Add a value for the amount field here
        }
        response = self.client.post(reverse('investment_list_create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_investment_detail(self):
        """
        Ensure we can retrieve a single investment's details.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('investment_detail', kwargs={'pk': self.investment.pk}))
        investment = Investment.objects.get(pk=self.investment.pk)
        serializer = InvestmentSerializer(investment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CropTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpassword')
        self.property = Property.objects.create(
            property_type='Agricultural',
            title='Test Property',
            description='Test description',
            location='Test location',
            area=100,
            price=10000
        )
        self.crop = Crop.objects.create(
            property=self.property,
            name='Test Crop',
            yield_per_hectare=500
        )

    def test_get_all_crops(self):
        """
        Ensure we can retrieve all crops.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('crop_list_create'))
        crops = Crop.objects.all()
        serializer = CropSerializer(crops, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_crop(self):
        """
        Ensure we can create a new crop.
        """
        self.client.force_authenticate(user=self.admin)
        data = {
            'property': self.property.pk,
            'name': 'New Crop',
            'yield_per_hectare': 1000
        }
        response = self.client.post(reverse('crop_list_create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_crop_detail(self):
        """
        Ensure we can retrieve a single crop's details.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('crop_detail', kwargs={'pk': self.crop.pk}))
        crop = Crop.objects.get(pk=self.crop.pk)
        serializer = CropSerializer(crop)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RegistrationLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """
        Ensure we can register a new user.
        """
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_existing_username(self):
        """
        Ensure we cannot register a new user with an existing username.
        """
        User.objects.create_user('existinguser', password='existingpassword')
        data = {
            'username': 'existinguser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_login_user(self):
        """
        Ensure we can log in a user and get an access token.
        """
        User.objects.create_user('testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_user_invalid_credentials(self):
        """
        Ensure we cannot log in a user with invalid credentials.
        """
        User.objects.create_user('testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)