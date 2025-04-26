from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    founded = models.DateField(auto_now=False, auto_now_add=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='publishers')

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,related_name='studios')

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=50)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE,
                               related_name='games_studios')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  related_name='games_publishers')
    release_year = models.IntegerField()
    dls_count = models.IntegerField()
    preview = models.ImageField(upload_to='game_previews/')

    def __str__(self):
        return self.name


class Comments(models.Model):
    email = models.EmailField(max_length=20)
    game = models.ForeignKey(Game, on_delete=models.CASCADE,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=300)

    def __str__(self):
        return self.comment

