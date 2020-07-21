from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""
    # after we finish creating this serializer, we implement the view

    class Meta:
        model = Recipe

        # define primary-key related fields
        # need to define ingredients and tags as special fields since they are refs
        ingredients = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Ingredient.objects.all()
        )

        tags = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Ingredient.objects.all()
        )

        fields = ('id', 'name', 'time_minutes', 'price',
                  'link', 'tags', 'ingredients')
        read_only_fields = ('id',)
