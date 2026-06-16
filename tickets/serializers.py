# Serializers convert Django models <-> JSON data
# They are "translators" between Python objects and JSON

from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Ticket, TicketComment, UserProfile

# Serializer for TicketComment model
class TicketCommentSerializer(serializers.ModelSerializer):
    """
    Converts TicketComment model to JSON.
    
    Example output:
    {
        "id": 1,
        "author": "john_doe",
        "content": "I've started working on this",
        "created_at": "2026-06-01T20:00:00Z",
        "ticket": 5
    }
    """
    # Shows the author's username instead of just ID
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = TicketComment
        
        # Which fields to include in the JSON response
        fields = ['id', 'ticket', 'author', 'content', 'created_at']
        
        # Read-only fields (user can't change these via API)
        read_only_fields = ['id', 'created_at', 'author']


# Serializer for Ticket model
class TicketSerializer(serializers.ModelSerializer):
    # Read-only field — shows assignee's username in responses
    assigned_to_name = serializers.SerializerMethodField(read_only=True)

    # Writable field — accepts user ID when creating/updating a ticket
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )

    # Shows creator's username (read-only)
    created_by = serializers.StringRelatedField(read_only=True)

    # Nested comments (read-only)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'status',
            'assigned_to',
            'assigned_to_name',
            'created_by',
            'created_at',
            'updated_at',
            'comments',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    # Required method for SerializerMethodField — name must be get_ + field name
    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.username
        return None

        
class UserRegistrationSerializer(serializers.ModelSerializer):
    # write_only=True — password is accepted in requests but NEVER returned in responses
    password = serializers.CharField(write_only=True, min_length=8)
        
    # role comes from UserProfile, not from User — we handle it manually in create()
    role = serializers.ChoiceField(choices=['logistics', 'project_manager', 'engineer', 'other'])
        
    class Meta:
        model = User
        # email is optional
        fields = ['username', 'email', 'password', 'role']
            
    def create(self, validated_data):
        # Extract role before creating User — User model has no role field
        role = validated_data.pop('role')

        # create_user() hashes the password automatically — never use plain create()!
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )

        # Create the linked UserProfile with the role
        UserProfile.objects.create(user=user, role=role)

        return user
                
