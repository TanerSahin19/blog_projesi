# Register your models here.
from django.contrib import admin
from .models import Carousel, Category, Tag, Post

# Carousel modelini admin paneline ekle
# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag, Carousel

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Admin panelinde listede görünecek alanlar
    list_display = ('title', 'author', 'category', 'active')

    # Arama kutusunda aranacak alanlar
    search_fields = ('title', 'content')

    # Filtreleme için sağ tarafta çıkacak alanlar
    list_filter = ('active', 'category', 'author')

    # Post eklerken/düzenlerken formda gözükecek alanlar
    fields = ('title', 'content', 'image', 'category', 'tags', 'active', 'author')


# Diğer modelleri de kaydediyoruz
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

