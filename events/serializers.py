from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Comment, Registration, Contact, Notice, FinancialCategory, Income, Expense, OrganizingCommitteeMember, Guest, ProfileFrameSubmission, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'image',
                 'created_at', 'updated_at', 'organizer', 'attendees',
                 'comments', 'is_attending']
        read_only_fields = ['organizer', 'attendees']

    def get_is_attending(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attendees.filter(id=request.user.id).exists()
        return False

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'name', 'batch', 'profession', 'mobile', 'email',
                 'family_members', 'special_requests', 'payment_method',
                 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validate mobile number format
        mobile = data.get('mobile', '')
        if not mobile.isdigit() or len(mobile) < 10:
            raise serializers.ValidationError({'mobile': 'অবৈধ মোবাইল নম্বর'})

        # Validate email format
        email = data.get('email', '')
        if '@' not in email or '.' not in email:
            raise serializers.ValidationError({'email': 'অবৈধ ইমেইল ঠিকানা'})

        # Validate transaction ID for non-cash payments
        payment_method = data.get('payment_method')
        transaction_id = data.get('transaction_id')
        if payment_method != 'cash' and not transaction_id:
            raise serializers.ValidationError({'transaction_id': 'লেনদেন আইডি প্রয়োজন'})

        return data

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'mobile', 'subject', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class FinancialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCategory
        fields = ['id', 'name', 'description']

class IncomeSerializer(serializers.ModelSerializer):
    category = FinancialCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all(), source='category', write_only=True)

    class Meta:
        model = Income
        fields = ['id', 'category', 'category_id', 'amount', 'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ExpenseSerializer(serializers.ModelSerializer):
    category = FinancialCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all(), source='category', write_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'category', 'category_id', 'amount', 'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class OrganizingCommitteeMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizingCommitteeMember
        fields = ['id', 'name', 'role', 'profession', 'contact', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'role', 'profession', 'contact', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProfileFrameSubmissionSerializer(serializers.ModelSerializer):
    bloodType = serializers.CharField(source='blood_type', required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = ProfileFrameSubmission
        fields = ['id', 'picture', 'name', 'mobile', 'address', 'batch', 'bloodType', 'created_at']
        read_only_fields = ['created_at']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__' 