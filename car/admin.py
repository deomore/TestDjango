from django.contrib import admin
from car.models import Country, Category, Publisher, Studio, Game, Comments, News


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)  # Добавили поиск, чтобы работало автодополнение (если понадобится)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded')
    # search_fields нужен, если мы захотим использовать автокомплит в Игре для выбора издателя
    search_fields = ('name',)
    autocomplete_fields = ('country',)  # Пример: выбор страны через поиск


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    autocomplete_fields = ('country',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'studio', 'publisher', 'release_year')
    search_fields = ('name',)

    # ВОТ ЭТО РЕШАЕТ ПРОБЛЕМУ С КАТЕГОРИЯМИ:
    # filter_horizontal создает удобный интерфейс с двумя колонками для ManyToMany
    filter_horizontal = ('categories',)

    # Для внешних ключей (ForeignKey), если элементов много (например, студий),
    # лучше использовать autocomplete_fields вместо выпадающего списка:
    autocomplete_fields = ('studio', 'publisher')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('email', 'game', 'created')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')