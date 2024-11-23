from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,related_name='brands')

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='cars')
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return self.name


class Comments(models.Model):
    email = models.EmailField(max_length=20)
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=300)

    def __str__(self):
        return self.comment
