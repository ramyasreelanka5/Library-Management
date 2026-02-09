"""
Core Views for Enhanced Library System
Handles authentication, dashboard, books, issues, and student features
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta, date
from .models import (
    Book, Issue, Fine, UserProfile, Category, Author, 
    Publisher, Reservation, Notification
)
from .utils import role_required, librarian_required, log_audit, create_notification


# ============= Authentication =============

def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            log_audit(user, 'LOGIN', 'User', description=f'User {username} logged in', request=request)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """User logout"""
    log_audit(request.user, 'LOGOUT', 'User', description=f'User {request.user.username} logged out', request=request)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def register_view(request):
    """Student registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        year = request.POST.get('year')
        phone = request.POST.get('phone')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            UserProfile.objects.create(
                user=user,
                role='STUDENT',
                student_id=student_id,
                department=department,
                year=year,
                phone=phone
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    
    return render(request, 'register.html')


# ============= Dashboard =============

@login_required
def dashboard(request):
    """Role-based dashboard"""
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else None
    
    context = {
        'user_role': user_role,
    }
    
    if user_role in ['ADMIN', 'LIBRARIAN']:
        # Admin/Librarian Dashboard
        context.update({
            'total_books': Book.objects.count(),
            'available_books': Book.objects.filter(available_quantity__gt=0).count(),
            'total_students': UserProfile.objects.filter(role='STUDENT').count(),
            'active_issues': Issue.objects.filter(return_date__isnull=True).count(),
            'overdue_issues': Issue.objects.filter(return_date__isnull=True, due_date__lt=date.today()).count(),
            'pending_fines': Fine.objects.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or 0,
            'recent_issues': Issue.objects.select_related('book', 'user').order_by('-issue_date')[:5],
            'overdue_books': Issue.objects.filter(return_date__isnull=True, due_date__lt=date.today()).select_related('book', 'user')[:5],
        })
        return render(request, 'dashboard_librarian.html', context)
    else:
        # Student Dashboard
        my_issues = Issue.objects.filter(user=request.user, return_date__isnull=True)
        my_fines = Fine.objects.filter(issue__user=request.user, status='PENDING')
        
        context.update({
            'my_active_issues': my_issues.count(),
            'my_overdue': my_issues.filter(due_date__lt=date.today()).count(),
            'my_pending_fines': my_fines.aggregate(total=Sum('amount'))['total'] or 0,
            'my_issues': my_issues.select_related('book')[:5],
            'my_fines': my_fines.select_related('issue__book')[:5],
            'available_books_count': Book.objects.filter(available_quantity__gt=0).count(),
        })
        return render(request, 'dashboard_student.html', context)


# ============= Books =============

@login_required
def book_list(request):
    """List and search books"""
    books = Book.objects.filter(is_active=True).select_related('author', 'category', 'publisher')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(isbn__icontains=search) |
            Q(author__name__icontains=search)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Filter by availability
    available_only = request.GET.get('available')
    if available_only:
        books = books.filter(available_quantity__gt=0)
    
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
        'search': search,
    }
    return render(request, 'books/book_list.html', context)


@login_required
def book_detail(request, book_id):
    """Book details"""
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request, 'books/book_detail.html', context)


@librarian_required
def book_add(request):
    """Add new book (Admin/Librarian only)"""
    if request.method == 'POST':
        # Get form data
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        category_id = request.POST.get('category')
        publisher_id = request.POST.get('publisher')
        total_quantity = request.POST.get('total_quantity', 1)
        
        book = Book.objects.create(
            isbn=isbn,
            title=title,
            author_id=author_id,
            category_id=category_id,
            publisher_id=publisher_id,
            total_quantity=total_quantity,
            available_quantity=total_quantity,
        )
        
        log_audit(request.user, 'CREATE', 'Book', book.id, f'Added book: {book.title}', request)
        messages.success(request, f'Book "{book.title}" added successfully!')
        return redirect('book_list')
    
    context = {
        'categories': Category.objects.all(),
        'authors': Author.objects.all(),
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'books/book_add.html', context)


# ============= Issues =============

@librarian_required
def issue_list(request):
    """List all issues (Admin/Librarian only)"""
    issues = Issue.objects.select_related('book', 'user').order_by('-issue_date')
    
    # Filter active/returned
    status = request.GET.get('status')
    if status == 'active':
        issues = issues.filter(return_date__isnull=True)
    elif status == 'returned':
        issues = issues.filter(return_date__isnull=False)
    elif status == 'overdue':
        issues = issues.filter(return_date__isnull=True, due_date__lt=date.today())
    
    context = {'issues': issues}
    return render(request, 'issues/issue_list.html', context)


@librarian_required
def issue_create(request):
    """Create new issue (Admin/Librarian only)"""
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        user_id = request.POST.get('user_id')
        days = int(request.POST.get('days', 14))
        
        book = Book.objects.get(id=book_id)
        user = User.objects.get(id=user_id)
        
        if book.available_quantity <= 0:
            messages.error(request, 'Book is not available!')
        else:
            issue = Issue.objects.create(
                book=book,
                user=user,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=days),
                issued_by=request.user
            )
            
            # Update book quantity
            book.available_quantity -= 1
            book.save()
            
            # Create notification
            create_notification(
                user,
                'GENERAL',
                'Book Issued',
                f'You have been issued "{book.title}". Due date: {issue.due_date}'
            )
            
            log_audit(request.user, 'ISSUE', 'Issue', issue.id, f'Issued {book.title} to {user.username}', request)
            messages.success(request, f'Book issued successfully to {user.username}!')
            return redirect('issue_list')
    
    context = {
        'books': Book.objects.filter(available_quantity__gt=0).select_related('author', 'category'),
        'students': User.objects.filter(profile__role='STUDENT').select_related('profile'),
    }
    return render(request, 'issues/issue_create.html', context)


@librarian_required
def issue_return(request, issue_id):
    """Return book (Admin/Librarian only)"""
    issue = get_object_or_404(Issue, id=issue_id)
    
    if issue.return_date:
        messages.warning(request, 'Book already returned!')
    else:
        issue.return_date = date.today()
        issue.returned_to = request.user
        issue.save()
        
        # Update book quantity
        issue.book.available_quantity += 1
        issue.book.save()
        
        # Calculate fine if overdue
        if issue.is_overdue:
            fine_amount = issue.calculate_fine()
            Fine.objects.create(
                issue=issue,
                amount=fine_amount,
                status='PENDING'
            )
            messages.warning(request, f'Book returned with fine: Rs {fine_amount}')
        else:
            messages.success(request, 'Book returned successfully!')
        
        log_audit(request.user, 'RETURN', 'Issue', issue.id, f'Returned {issue.book.title}', request)
    
    return redirect('issue_list')


@login_required
def issue_renew(request, issue_id):
    """Renew book"""
    issue = get_object_or_404(Issue, id=issue_id)
    
    if issue.user != request.user and not hasattr(request.user.profile, 'role') or request.user.profile.role not in ['ADMIN', 'LIBRARIAN']:
        messages.error(request, 'You do not have permission to renew this book.')
    elif issue.return_date:
        messages.error(request, 'Book already returned!')
    elif issue.renewal_count >= issue.max_renewals:
        messages.error(request, f'Maximum renewals ({issue.max_renewals}) reached!')
    else:
        issue.due_date += timedelta(days=7)
        issue.renewal_count += 1
        issue.save()
        
        messages.success(request, f'Book renewed! New due date: {issue.due_date}')
        log_audit(request.user, 'RENEW', 'Issue', issue.id, f'Renewed {issue.book.title}', request)
    
    return redirect('my_books' if issue.user == request.user else 'issue_list')


# ============= Fines =============

@librarian_required
def fine_list(request):
    """List all fines"""
    fines = Fine.objects.select_related('issue__book', 'issue__user').order_by('-created_at')
    
    status = request.GET.get('status')
    if status:
        fines = fines.filter(status=status.upper())
    
    context = {'fines': fines}
    return render(request, 'fines/fine_list.html', context)


@librarian_required
def fine_pay(request, fine_id):
    """Process fine payment"""
    fine = get_object_or_404(Fine, id=fine_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'CASH')
        
        fine.status = 'PAID'
        fine.payment_date = date.today()
        fine.payment_method = payment_method
        fine.save()
        
        messages.success(request, f'Fine of Rs {fine.amount} paid successfully!')
        log_audit(request.user, 'PAYMENT', 'Fine', fine.id, f'Fine paid: Rs {fine.amount}', request)
        return redirect('fine_list')
    
    return render(request, 'fines/fine_pay.html', {'fine': fine})


# ============= Student Portal =============

@login_required
def my_books(request):
    """Student's issued books"""
    issues = Issue.objects.filter(user=request.user).select_related('book').order_by('-issue_date')
    context = {'issues': issues}
    return render(request, 'student/my_books.html', context)


@login_required
def my_fines(request):
    """Student's fines"""
    fines = Fine.objects.filter(issue__user=request.user).select_related('issue__book').order_by('-created_at')
    context = {'fines': fines}
    return render(request, 'student/my_fines.html', context)


@login_required
def my_reservations(request):
    """Student's reservations"""
    reservations = Reservation.objects.filter(user=request.user).select_related('book').order_by('-reserved_date')
    context = {'reservations': reservations}
    return render(request, 'student/my_reservations.html', context)


@login_required
def profile(request):
    """User profile"""
    if request.method == 'POST':
        # Update profile
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        if hasattr(request.user, 'profile'):
            request.user.profile.phone = request.POST.get('phone', '')
            request.user.profile.department = request.POST.get('department', '')
            request.user.profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html')


# ============= Lists for Admin/Librarian =============

@librarian_required
def student_list(request):
    """List all students"""
    students = User.objects.filter(profile__role='STUDENT').select_related('profile')
    context = {'students': students}
    return render(request, 'students/student_list.html', context)


@librarian_required
def student_detail(request, student_id):
    """Student details and history"""
    student = get_object_or_404(User, id=student_id)
    issues = Issue.objects.filter(user=student).select_related('book').order_by('-issue_date')[:10]
    fines = Fine.objects.filter(issue__user=student).select_related('issue__book').order_by('-created_at')[:10]
    
    context = {
        'student': student,
        'issues': issues,
        'fines': fines,
    }
    return render(request, 'students/student_detail.html', context)


@librarian_required
def category_list(request):
    """List categories"""
    categories = Category.objects.annotate(book_count=Count('books'))
    context = {'categories': categories}
    return render(request, 'categories/category_list.html', context)


@librarian_required
def author_list(request):
    """List authors"""
    authors = Author.objects.annotate(book_count=Count('books'))
    context = {'authors': authors}
    return render(request, 'authors/author_list.html', context)


@librarian_required
def publisher_list(request):
    """List publishers"""
    publishers = Publisher.objects.annotate(book_count=Count('books'))
    context = {'publishers': publishers}
    return render(request, 'publishers/publisher_list.html', context)


# ============= Reports =============

@librarian_required
def reports(request):
    """Reports dashboard"""
    return render(request, 'reports/reports.html')


@librarian_required
def report_overdue(request):
    """Overdue books report"""
    overdue = Issue.objects.filter(return_date__isnull=True, due_date__lt=date.today()).select_related('book', 'user')
    context = {'overdue_issues': overdue}
    return render(request, 'reports/overdue.html', context)


@librarian_required
def report_popular(request):
    """Popular books report"""
    popular = Book.objects.annotate(issue_count=Count('issues')).order_by('-issue_count')[:20]
    context = {'popular_books': popular}
    return render(request, 'reports/popular.html', context)
