from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse

# --- Slaytlar için Carousel modeli (opsiyonel kullanabilirsin) ---
class Carousel(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField()  
    images = models.ImageField(upload_to='carousel_images/')  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.title  


# --- Kategoriler ---
class Category(models.Model):
    name = models.CharField(max_length=50)  # Kategori adı
    slug = models.SlugField(editable=False, unique=True)  # URL uyumlu slug
    parent = models.ForeignKey(
        'self',                     # Kendisine referans (alt kategori için)
        on_delete=models.CASCADE,   
        related_name='subcategories',  # Alt kategorilere ulaşım
        null=True, blank=True        # Boş olursa ana kategori olur
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # İsme göre slug üret
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        # Admin panelinde AnaKategori > AltKategori şeklinde görünmesi için
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


# --- Etiketler (örn: Python, Django, Blog) ---
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# --- Blog Gönderileri ---
class Post(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')  
    tags = models.ManyToManyField('Tag', blank=True)  
    active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts',
        null=True, blank=True
    )
    slug = models.SlugField(editable=False, unique=True, max_length=220, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base
            n = 2
            while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{n}"
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # Post detay sayfasına yönlendirme
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
