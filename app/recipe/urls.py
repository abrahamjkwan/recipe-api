from django.urls import path, include
from rest_framework.routers import DefaultRouter

# pulling in view allows us to render viewset
from recipe import views

# the Default Router registers all the appropriate URLs
# for the actions in our viewset

router = DefaultRouter()

# register our viewset with the router
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

# define the app name for the reverse function
app_name = 'recipe'

# paths that matches our recipe app pass requests through router urls
urlpatterns = [
    path('', include(router.urls))
]
