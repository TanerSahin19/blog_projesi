from django.shortcuts import render, get_object_or_404
from .models import Post, Carousel, Category

# --- Ana Sayfa ---
def home(request):
    posts = Post.objects.filter(active=True).order_by('-created_at')[:3]  # Son 3 post
    carousels = Carousel.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'carousels': carousels,
    })

# --- Tüm Postlar ---
def post_list(request):
    posts = Post.objects.filter(active=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
    })

# --- Tekil Post ---
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, active=True)
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'categories': categories,
    })

# --- Kategoriye Göre Filtrelenmiş Postlar ---
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, active=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/category_detail.html', {
        'category': category,
        'category_posts': posts,
        'categories': categories,  # Sidebar için
    })
