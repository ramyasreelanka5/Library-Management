"""
Application Constants
Centralized location for all constant values used throughout the application
"""

# User Roles
class UserRoles:
    ADMIN = 'ADMIN'
    LIBRARIAN = 'LIBRARIAN'
    STUDENT = 'STUDENT'
    
    CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (STUDENT, 'Student'),
    ]


# Issue Settings
class IssueSettings:
    DEFAULT_ISSUE_DAYS = 14
    MAX_RENEWALS = 2
    RENEWAL_DAYS = 7


# Fine Settings
class FineSettings:
    FINE_PER_DAY = 10  # Rs 10 per day
    
    # Fine status
    STATUS_PENDING = 'PENDING'
    STATUS_PAID = 'PAID'
    STATUS_WAIVED = 'WAIVED'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_WAIVED, 'Waived'),
    ]
    
    # Payment methods
    PAYMENT_CASH = 'CASH'
    PAYMENT_CARD = 'CARD'
    PAYMENT_UPI = 'UPI'
    
    PAYMENT_CHOICES = [
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_CARD, 'Card'),
        (PAYMENT_UPI, 'UPI'),
    ]


# Notification Types
class NotificationTypes:
    GENERAL = 'GENERAL'
    DUE_SOON = 'DUE_SOON'
    OVERDUE = 'OVERDUE'
    FINE = 'FINE'
    AVAILABLE = 'AVAILABLE'
    
    CHOICES = [
        (GENERAL, 'General'),
        (DUE_SOON, 'Due Soon'),
        (OVERDUE, 'Overdue'),
        (FINE, 'Fine'),
        (AVAILABLE, 'Book Available'),
    ]


# Reservation Status
class ReservationStatus:
    PENDING = 'PENDING'
    FULFILLED = 'FULFILLED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    
    CHOICES = [
        (PENDING, 'Pending'),
        (FULFILLED, 'Fulfilled'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
    ]


# Audit Action Types
class AuditActions:
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    ISSUE = 'ISSUE'
    RETURN = 'RETURN'
    RENEW = 'RENEW'
    PAYMENT = 'PAYMENT'
    
    CHOICES = [
        (LOGIN, 'Login'),
        (LOGOUT, 'Logout'),
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (ISSUE, 'Issue Book'),
        (RETURN, 'Return Book'),
        (RENEW, 'Renew Book'),
        (PAYMENT, 'Payment'),
    ]


# Pagination
class Pagination:
    BOOKS_PER_PAGE = 12
    ISSUES_PER_PAGE = 20
    STUDENTS_PER_PAGE = 15
    FINES_PER_PAGE = 20
