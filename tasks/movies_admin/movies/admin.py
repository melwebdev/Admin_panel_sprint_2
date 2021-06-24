from django.contrib import admin
from .models import *


class PersonRoleInline(admin.TabularInline):
    model = PersonRole
    extra = 0
    autocomplete_fields = ('person', 'filmwork')

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'age_rating')
    fields = (
        'title', 'type', 'description', 'creation_date',
        'file_path', 'rating', 'genres', 'age_rating',
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    inlines = [
        PersonRoleInline
    ]
    autocomplete_fields = ('genres',)


@admin.register(Genre)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ('name', 'description')
    search_fields = ('name',)


@admin.register(Person)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    search_fields = ('name',)
    inlines = [
        PersonRoleInline
    ]


@admin.register(AgeRating)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description']


@admin.register(PersonRole)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('person', 'filmwork','role',)
    fields = ('role', 'person', 'filmwork')
    list_filter = ('role',)