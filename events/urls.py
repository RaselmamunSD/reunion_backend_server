from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import StudentListByBatchView

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'comments', views.CommentViewSet, basename='event-comments')
router.register(r'registrations', views.RegistrationViewSet)
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'notices', views.NoticeViewSet, basename='notice')
router.register(r'financial-categories', views.FinancialCategoryViewSet, basename='financial-category')
router.register(r'incomes', views.IncomeViewSet, basename='income')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
router.register(r'organizing-committee', views.OrganizingCommitteeMemberViewSet, basename='organizing-committee')
router.register(r'guests', views.GuestViewSet, basename='guest')
router.register(r'profile-frame-submissions', views.ProfileFrameSubmissionViewSet, basename='profile-frame-submission')

urlpatterns = [
    path('', include(router.urls)),
    path('students/', StudentListByBatchView.as_view(), name='student-list'),
] 