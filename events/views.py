from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Event, Comment, Registration, Contact, Notice, FinancialCategory, Income, Expense, OrganizingCommitteeMember, Guest, ProfileFrameSubmission, Student
from .serializers import EventSerializer, CommentSerializer, RegistrationSerializer, ContactSerializer, NoticeSerializer, FinancialCategorySerializer, IncomeSerializer, ExpenseSerializer, OrganizingCommitteeMemberSerializer, GuestSerializer, ProfileFrameSubmissionSerializer, StudentSerializer
from rest_framework import generics

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def attend(self, request, pk=None):
        event = self.get_object()
        if request.user in event.attendees.all():
            event.attendees.remove(request.user)
            return Response({'status': 'removed from attendees'})
        else:
            event.attendees.add(request.user)
            return Response({'status': 'added to attendees'})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        event = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_pk')
        event = get_object_or_404(Event, pk=event_id)
        serializer.save(user=self.request.user, event=event)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all().order_by('-created_at')
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register 

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post'] # Only allow POST requests for contact form 

class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.all().order_by('-date') # Order by date descending
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to view notices 

class FinancialCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinancialCategory.objects.all()
    serializer_class = FinancialCategorySerializer
    permission_classes = [permissions.AllowAny]

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomeSerializer
    permission_classes = [permissions.AllowAny]

    # Optional: Add an action to get total income
    @action(detail=False, methods=['get'])
    def total(self, request):
        total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'total_income': total_income})

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]

    # Optional: Add an action to get total expenses
    @action(detail=False, methods=['get'])
    def total(self, request):
        total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'total_expenses': total_expenses})

class OrganizingCommitteeMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrganizingCommitteeMember.objects.all().order_by('name') # Order by name
    serializer_class = OrganizingCommitteeMemberSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to view members 

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all().order_by('name') # Order by name
    serializer_class = GuestSerializer
    permission_classes = [permissions.AllowAny] # Adjust permissions as needed 

class ProfileFrameSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ProfileFrameSubmission.objects.all().order_by('-created_at') # Order by creation date
    serializer_class = ProfileFrameSubmissionSerializer
    permission_classes = [permissions.AllowAny] # Allow submissions from anyone
    # You might want to restrict methods if only creation is needed, e.g., http_method_names = ['post'] 

class StudentListByBatchView(generics.ListAPIView):
    """API view to list students, optionally filtered by batch year."""
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset by batch year,
        which is passed in the URL.
        """
        queryset = Student.objects.all()
        batch_year = self.request.query_params.get('batch', None)
        if batch_year is not None:
            queryset = queryset.filter(batch=batch_year)
        return queryset 