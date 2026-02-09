"""
Django Forms for Library Management System
Provides form validation and handling for user inputs
"""

from django import forms
from django.contrib.auth.models import User
from .models import Book, Issue, UserProfile, Category, Author, Publisher


class StudentRegistrationForm(forms.ModelForm):
    """Form for student registration"""
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords don't match")
        return confirm
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class BookForm(forms.ModelForm):
    """Form for adding/editing books"""
    
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'category', 'publisher', 
                  'total_quantity', 'publication_year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        # Basic ISBN validation
        if isbn and len(isbn) < 10:
            raise forms.ValidationError("ISBN must be at least 10 characters")
        return isbn
    
    def clean_total_quantity(self):
        quantity = self.cleaned_data.get('total_quantity')
        if quantity and quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        return quantity


class IssueBookForm(forms.ModelForm):
    """Form for issuing books"""
    
    class Meta:
        model = Issue
        fields = ['book', 'user', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        user = cleaned_data.get('user')
        
        if book and book.available_quantity <= 0:
            raise forms.ValidationError("This book is not available")
        
        if user and book:
            # Check if user already has this book
            active_issue = Issue.objects.filter(
                user=user, 
                book=book, 
                return_date__isnull=True
            ).exists()
            if active_issue:
                raise forms.ValidationError(
                    f"{user.username} already has this book issued"
                )
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'department', 'year']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if phone and len(phone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits")
        return phone


class BookSearchForm(forms.Form):
    """Form for searching books"""
    search = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by title, ISBN, or author...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    available_only = forms.BooleanField(
        required=False,
        label='Available Only'
    )
