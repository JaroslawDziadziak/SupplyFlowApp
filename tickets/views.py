# REST API Views using Django REST Framework
# ViewSets automatically create API endpoints for CRUD operations
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Ticket, TicketComment, UserProfile
from .serializers import TicketSerializer, TicketCommentSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Ticket management.
    
    Automatically provides:
    - GET    /api/tickets/                 → List all tickets
    - POST   /api/tickets/                 → Create new ticket
    - GET    /api/tickets/{id}/            → Get ticket details
    - PUT    /api/tickets/{id}/            → Update ticket
    - PATCH  /api/tickets/{id}/            → Partial update
    - DELETE /api/tickets/{id}/            → Delete ticket
    
    This is called "CRUD" (Create, Read, Update, Delete)
    """
    
    # Use TicketSerializer to convert model <-> JSON
    serializer_class = TicketSerializer
    
    # Only authenticated users can access this API
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return all tickets from database.
        In the future, we could filter by user (e.g., "only my tickets")
        """
        return Ticket.objects.all()
    
    def perform_create(self, serializer):
        """
        When a new ticket is created, automatically set created_by
        to the currently logged-in user.
        
        This ensures we never trust the user to set this field!
        """
        serializer.save(created_by=self.request.user)
    
    # Custom action: Mark ticket as resolved
    @action(detail=True, methods=['post'])
    def mark_resolved(self, request, pk=None):
        """
        Custom endpoint: POST /api/tickets/{id}/mark_resolved/
        
        Marks a ticket as resolved.
        """
        ticket = self.get_object()  # Get the specific ticket
        ticket.status = Ticket.STATUS_RESOLVED
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
    # Custom action: Get statistics
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Custom endpoint: GET /api/tickets/statistics/
        
        Returns ticket statistics (how many are pending, in progress, etc.)
        """
        stats = {
            'total': Ticket.objects.count(),
            'new': Ticket.objects.filter(status=Ticket.STATUS_NEW).count(),
            'in_progress': Ticket.objects.filter(status=Ticket.STATUS_IN_PROGRESS).count(),
            'waiting': Ticket.objects.filter(status=Ticket.STATUS_WAITING).count(),
            'resolved': Ticket.objects.filter(status=Ticket.STATUS_RESOLVED).count(),
            'closed': Ticket.objects.filter(status=Ticket.STATUS_CLOSED).count(),
        }
        return Response(stats)


class TicketCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Ticket Comments.
    
    Provides:
    - GET    /api/comments/                → List all comments
    - POST   /api/comments/                → Create new comment
    - GET    /api/comments/{id}/           → Get comment details
    - PUT    /api/comments/{id}/           → Update comment
    - DELETE /api/comments/{id}/           → Delete comment
    """
    
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return all comments from database."""
        return TicketComment.objects.all()
    
    def perform_create(self, serializer):
        """
        When a new comment is created, automatically set author
        to the currently logged-in user.
        """
        serializer.save(author=self.request.user)
        
class RegisterView(generics.CreateAPIView):
    # CreateAPIView automatically handles POST requests for creating objects
    # We only need to specify which serializer and permissions to use
    serializer_class = UserRegistrationSerializer
    
    # AllowAny — this endpoint must be public, anyone can register
    # Without this, only logged-in users could create accounts 
    permission_classes = [AllowAny]    
    
class UserListView(generics.ListAPIView):
    # Returns a list of all users — used to populate the "Assign to" dropdown
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Return only id and username — never expose passwords or emails in lists
        users = User.objects.values('id', 'username').order_by('username')
        return Response(list(users))
    
class CurrentUserView(generics.RetrieveAPIView):
    # Returns the currently logged-in user's data
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        #Getting role from UserProfile — using 'other' as fallback if profile missing
        try:
            role = user.profile.role
        except UserProfile.DoesNotExist:
            role = 'other'
            
        return Response({
            'id': user.id,
            'username': user.username,
            'role': role,
        })

