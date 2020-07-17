from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PrivateTagsApiTests(TestCase):
    """Test the private tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123456',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Cantonese')
        Tag.objects.create(user=self.user, name='Breakfast')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags are returned for the authenticated user"""
        test_user = get_user_model().objects.create_user(
            email='test1@gmail.com',
            password='test123456',
            name='Test2 Name2'
        )

        Tag.objects.create(user=self.user, name='Cantonese')
        Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=test_user, name='Dim Sum')

        res = self.client.get(TAGS_URL)

        # Create tags var that returns only auth user using filter()
        tags = Tag.objects.all().filter(user=self.user)

        # Create serializer var. Why exactly? Need to research.
        serializer = TagSerializer(tags, many=True)

        # Check that values match between res.data and serializer.data
        self.assertEqual(res.data, serializer.data)

    def test_create_tag_successful(self):
        """Test authenticated user can create tags successfully"""
        payload = {'name': 'Cantonese'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
