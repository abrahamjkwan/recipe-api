from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return a recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Cantonese'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Rice noodles'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Beef chow fun',
        'time_minutes': 30,
        'price': 18.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def sample_recipe_2(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Mapo Tofu',
        'time_minutes': 15,
        'price': 11.50,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test login is required to access endpoint"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test the private Recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123456',
            name='Test Name'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe_list(self):
        """Test retrieving list of recipes as logged in user"""
        sample_recipe(user=self.user)
        sample_recipe_2(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving user specific list"""
        user2 = get_user_model().objects.create_user(
            email='test1@gmail.com',
            password='test123456',
            name='Test2 Person'
        )
        sample_recipe(self.user)
        Recipe.objects.create(
            user=self.user,
            name='Barbecue Cheeseburger',
            time_minutes=25,
            price=14.50
        )
        sample_recipe_2(user2)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Beef chow fun',
            'time_minutes': 30,
            'price': 18.00,
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Cantonese')
        tag2 = sample_tag(user=self.user, name='Noodles')
        payload = {
            'name': 'Beef chow fun',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 18.00,
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Rice noodles')
        ingredient2 = sample_ingredient(user=self.user, name='Round steak')
        payload = {
            'name': 'Beef chow fun',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 30,
            'price': 18.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
