from django import template
from blog.models import Category

register = template.Library()

# Tüm ana kategorileri ve alt kategorilerini getir
@register.simple_tag
def get_categories():
    return Category.objects.filter(parent__isnull=True)  # sadece ana kategoriler
