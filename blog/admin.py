# blog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count']
    search_fields = ['name', 'description']
    fields = ['name', 'description']  # slug est exclu volontairement
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = "Nombre d'articles"
    
    def save_model(self, request, obj, form, change):
        from django.utils.text import slugify
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'is_published', 'views']
    list_filter = ['is_published', 'category', 'author', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    date_hierarchy = 'created_at'
    list_editable = ['is_published']
    list_per_page = 20
    
    fields = ['title', 'category', 'author', 'featured_image', 'excerpt', 'content', 'is_published']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        from django.utils.text import slugify
        if not obj.slug:
            obj.slug = slugify(obj.title)
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['publish_posts', 'unpublish_posts']
    
    def publish_posts(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} article(s) publié(s).')
    publish_posts.short_description = 'Publier les articles sélectionnés'
    
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} article(s) dépublié(s).')
    unpublish_posts.short_description = 'Dépublier les articles sélectionnés'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__username', 'content', 'post__title']
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fields = ['post', 'user', 'content', 'is_approved']
    readonly_fields = ['created_at']