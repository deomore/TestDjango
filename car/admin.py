from django.contrib import admin
from car.models import Country, Category, Publisher, Studio, Game, Comments, News

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded')

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'studio', 'publisher', 'release_year')
    filter_horizontal = ('categories',)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('email', 'game', 'created')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')