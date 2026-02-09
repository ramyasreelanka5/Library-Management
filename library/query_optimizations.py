"""
Database query optimizations for better performance
"""

from django.db.models import Prefetch, Count, Q, Exists, OuterRef
from .models import Book, Issue, Fine, UserProfile


class OptimizedQueryManager:
    """Manager class for optimized database queries"""
    
    @staticmethod
    def get_books_with_relations():
        """Get books with related author, category, publisher in single query"""
        return Book.objects.select_related(
            'author', 
            'category', 
            'publisher'
        ).filter(is_active=True)
    
    @staticmethod
    def get_issues_with_details():
        """Get issues with all related data"""
        return Issue.objects.select_related(
            'book',
            'book__author',
            'book__category',
            'user',
            'user__profile',
            'issued_by',
            'returned_to'
        )
    
    @staticmethod
    def get_students_with_stats():
        """Get students with their issue and fine statistics"""
        from django.db.models import Count, Sum
        
        return UserProfile.objects.filter(
            role='STUDENT'
        ).select_related('user').annotate(
            total_issues=Count('user__issues'),
            active_issues=Count(
                'user__issues',
                filter=Q(user__issues__return_date__isnull=True)
            ),
            total_fines=Sum(
                'user__issues__fines__amount',
                filter=Q(user__issues__fines__status='PENDING')
            )
        )
    
    @staticmethod
    def get_popular_books(limit=10):
        """Get most issued books"""
        return Book.objects.annotate(
            issue_count=Count('issues')
        ).filter(
            issue_count__gt=0
        ).order_by('-issue_count')[:limit]
    
    @staticmethod
    def get_overdue_issues():
        """Get all overdue issues efficiently"""
        from datetime import date
        
        return Issue.objects.filter(
            return_date__isnull=True,
            due_date__lt=date.today()
        ).select_related(
            'book',
            'book__author',
            'user',
            'user__profile'
        ).order_by('due_date')
    
    @staticmethod
    def search_books(query, category_id=None, available_only=False):
        """Optimized book search with filters"""
        queryset = Book.objects.select_related(
            'author', 'category', 'publisher'
        ).filter(is_active=True)
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(isbn__icontains=query) |
                Q(author__name__icontains=query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if available_only:
            queryset = queryset.filter(available_quantity__gt=0)
        
        return queryset.order_by('title')
