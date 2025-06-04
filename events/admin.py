from django.contrib import admin
from .models import Event, Comment, Registration, Contact, Notice, FinancialCategory, Income, Expense, OrganizingCommitteeMember, Guest, ProfileFrameSubmission, Student

@admin.register(FinancialCategory)
class FinancialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'created_at')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'created_at')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch', 'profession', 'mobile', 'email', 'family_members', 'payment_method', 'created_at')
    list_filter = ('batch', 'payment_method', 'created_at')
    search_fields = ('name', 'email', 'mobile', 'profession')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'batch', 'profession', 'mobile', 'email')
        }),
        ('Registration Details', {
            'fields': ('family_members', 'special_requests')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'content', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('content', 'user__username')

@admin.register(OrganizingCommitteeMember)
class OrganizingCommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'profession', 'contact', 'created_at', 'profile_picture_preview')
    list_filter = ('role', 'profession')
    search_fields = ('name', 'role', 'profession', 'contact')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview')
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No image"
    profile_picture_preview.short_description = 'Profile Picture'
    profile_picture_preview.allow_tags = True

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'profession', 'contact', 'created_at', 'profile_picture_preview')
    list_filter = ('role', 'profession')
    search_fields = ('name', 'profession', 'contact')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview')
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No image"
    profile_picture_preview.short_description = 'Profile Picture'
    profile_picture_preview.allow_tags = True

@admin.register(ProfileFrameSubmission)
class ProfileFrameSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'created_at')
    search_fields = ('name', 'mobile', 'address')
    readonly_fields = ('created_at',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch', 'created_at', 'profile_picture_preview')
    list_filter = ('batch',)
    search_fields = ('name', 'batch')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview')
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No image"
    profile_picture_preview.short_description = 'Profile Picture'
    profile_picture_preview.allow_tags = True 