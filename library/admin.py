"""
Django Admin Configuration for Enhanced Library System
Provides comprehensive admin interface for all models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Author, Publisher, Book, Issue, Fine,
    Reservation, Notification, AuditLog, BookReview
)


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


# Extended User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'N/A'
    get_role.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'student_id', 'department', 'year', 'phone')
    list_filter = ('role', 'department', 'year')
    search_fields = ('user__username', 'user__email', 'student_id', 'phone')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')
    list_filter = ('country',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'category', 'publisher', 'total_quantity', 'available_quantity', 'is_active')
    list_filter = ('category', 'author', 'publisher', 'is_active', 'language')
    search_fields = ('title', 'isbn', 'author__name')
    readonly_fields = ('rating', 'total_ratings', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('isbn', 'title', 'category', 'author', 'publisher')
        }),
        ('Publication Details', {
            'fields': ('publication_year', 'edition', 'language', 'pages')
        }),
        ('Inventory', {
            'fields': ('total_quantity', 'available_quantity', 'rack_number', 'price')
        }),
        ('Additional Information', {
            'fields': ('description', 'cover_image', 'rating', 'total_ratings')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issue_date', 'due_date', 'return_date', 'renewal_count', 'is_overdue')
    list_filter = ('issue_date', 'due_date', 'return_date')
    search_fields = ('book__title', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'issue_date'
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('issue', 'amount', 'status', 'payment_date', 'payment_method')
    list_filter = ('status', 'payment_date')
    search_fields = ('issue__user__username', 'issue__book__title', 'payment_reference')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'reserved_date', 'expiry_date')
    list_filter = ('status', 'reserved_date')
    search_fields = ('book__title', 'user__username')
    date_hierarchy = 'reserved_date'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'description')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('book__title', 'user__username', 'review_text')
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"


# Customize admin site header
admin.site.site_header = "Library Management System - Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Management System"
