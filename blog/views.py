# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from .forms import CommentForm  # Assurez-vous que forms.py existe

def blog_home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    recent_posts = posts[:5]
    
    return render(request, 'blog/blog_home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts
    })

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    post.increment_views()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Connectez-vous pour commenter')
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté !')
            return redirect('blog_detail', slug=slug)
    else:
        form = CommentForm()
    
    comments = post.comments.filter(is_approved=True)
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True)[:5]
    
    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'categories': categories,
        'recent_posts': recent_posts
    })

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/category_posts.html', {
        'page_obj': page_obj,
        'category': category
    })