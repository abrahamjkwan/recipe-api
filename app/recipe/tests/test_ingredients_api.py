from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""
    # this is different than Tag test to show different approach
    # if we want to add more public API tests

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required to access endpoint"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123456',
            name='Test Name'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients as logged in user"""
        Ingredient.objects.create(
            user=self.user,
            name='Rice noodles'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Green onions'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test ingredient retrieval is limited by user ownership"""
        # After this function is written, create Ingredient Serializer
        test_user = get_user_model().objects.create_user(
            email='test1@gmail.com',
            password='testpw1234',
            name='Tester Person',
        )

        Ingredient.objects.create(
            user=self.user,
            name='Rice noodles'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Green onions'
        )
        Ingredient.objects.create(
            user=test_user,
            name='Round steak'
        )
        Ingredient.objects.create(
            user=test_user,
            name='Oyster sauce'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().filter(user=self.user)
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    # def test_create_ingredient_success(self):
    #     """Test creation of an ingredient by a user"""
    #     payload = {'name': 'Bean sprouts'}
    #     res = self.client.post(INGREDIENTS_URL, payload)

    #     exists = Ingredient.objects.filter(
    #         user=self.user,
    #         name=payload['name']
    #     ).exists()
    #     self.AssertTrue(exists)

    # def create_ingredient_invalid(self):
    #     """Test creating an ingredient with an invalid payload"""
    #     payload = {'name': ''}
    #     res = self.client.post(INGREDIENTS_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
