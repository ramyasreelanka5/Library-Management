"""
URL Configuration for Library System
Maps URLs to views
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/add/', views.book_add, name='book_add'),
    
    # Issues
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.issue_create, name='issue_create'),
    path('issues/<int:issue_id>/return/', views.issue_return, name='issue_return'),
    path('issues/<int:issue_id>/renew/', views.issue_renew, name='issue_renew'),
    
    # Fines
    path('fines/', views.fine_list, name='fine_list'),
    path('fines/<int:fine_id>/pay/', views.fine_pay, name='fine_pay'),
    
    # Students (for admin/librarian)
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Categories, Authors, Publishers
    path('categories/', views.category_list, name='category_list'),
    path('authors/', views.author_list, name='author_list'),
    path('publishers/', views.publisher_list, name='publisher_list'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/overdue/', views.report_overdue, name='report_overdue'),
    path('reports/popular/', views.report_popular, name='report_popular'),
    
    # Student Portal
    path('my-books/', views.my_books, name='my_books'),
    path('my-fines/', views.my_fines, name='my_fines'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('profile/', views.profile, name='profile'),
]
