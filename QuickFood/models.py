from django.db import models

class Pantry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    total_time = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.JSONField()  # Use JSONField for ingredients!
    directions = models.TextField()   # still plain text, will need parsing in view if dot-separated
    image = models.URLField(blank=True, null=True)
    rating = models.FloatField()
    url = models.URLField()
    cuisine_path = models.CharField(max_length=255, blank=True, null=True)
    nutrition = models.JSONField(blank=True, null=True)
    timing = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.recipe_name