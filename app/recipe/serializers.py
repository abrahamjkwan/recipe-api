from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    # define model, fields and extra kwargs
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient object"""
    # after we finish creating this serializer, we implement the view

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
