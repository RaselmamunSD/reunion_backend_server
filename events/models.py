from django.db import models
from django.contrib.auth.models import User
from django.db.models import Case, When, IntegerField

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.event}'

class Registration(models.Model):
    PAYMENT_METHODS = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('cash', 'Cash'),
    ]

    name = models.CharField(max_length=255)
    batch = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    family_members = models.IntegerField(default=0)
    special_requests = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Contact from {self.name}'

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FinancialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Financial Categories"

    def __str__(self):
        return self.name

class Income(models.Model):
    category = models.ForeignKey(FinancialCategory, related_name='incomes', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Income: {self.amount} ({self.date})'

class Expense(models.Model):
    category = models.ForeignKey(FinancialCategory, related_name='expenses', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Expense: {self.amount} ({self.date})'

class OrganizingCommitteeMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='organizing_committee/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.role}'

class Guest(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='guests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            Case(
                When(role='প্রধান অতিথি', then=0),
                When(role='বিশেষ অতিথি', then=1),
                When(role='সভাপতিত্ব', then=2),
                When(role='সার্বিক ত্বত্তবধান', then=3),
                default=4,
                output_field=IntegerField(),
            ),
            'name'
        ]

    def __str__(self):
        return self.name

class ProfileFrameSubmission(models.Model):
    picture = models.ImageField(upload_to='profile_frames/', null=True, blank=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Create Frames"

    def __str__(self):
        return self.name

class Student(models.Model):
    """Model to store student information."""
    batch = models.IntegerField() # Batch year, e.g., 1996
    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['batch', 'name'] # Order by batch then name

    def __str__(self):
        return f'{self.name} (Batch {self.batch})' 