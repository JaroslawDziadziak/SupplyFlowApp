from django.conf import settings
from django.db import models 

#Models
class Ticket(models.Model):
    #Class Constants Priority 
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'
    
    #List of avalilable options for Priority Field
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Niski'),
        (PRIORITY_MEDIUM, 'Średni'),
        (PRIORITY_HIGH, 'Wysoki'),
        (PRIORITY_URGENT, 'Pilny'),
    ]
    
    #Class Constrants Status 
    STATUS_NEW = 'New'
    STATUS_IN_PROGRESS = 'In_progress'
    STATUS_WAITING = 'Waiting'
    STATUS_RESOLVED = 'Resolved'
    STATUS_CLOSED = 'Closed'
    
    #List of avalilable options for Status Fields
    STATUS_CHOICES = [
        (STATUS_NEW, 'Nowe'),
        (STATUS_IN_PROGRESS, 'W trakcie'),
        (STATUS_WAITING, 'Oczekujące'),
        (STATUS_RESOLVED, 'Rozwiązane'),
        (STATUS_CLOSED, 'Zamknięte'),
    ]
    #Fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets',
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Function returns Title of the ticket
    def __str__(self):
        return self.title

class TicketComment(models.Model):
    #Comment to one ticket
    ticket = models.ForeignKey(
       Ticket,
       on_delete=models.CASCADE,
       related_name='comments',
    )
    #Autor of the ticket
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_comments',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.ticket}'
    
class UserProfile(models.Model):
    # Role choices available during registration
    ROLE_LOGISTICS = 'logistics'
    ROLE_PROJECT_MANAGER = 'project_manager'
    ROLE_ENGINEER = 'engineer'
    ROLE_OTHER = 'other'

    ROLE_CHOICES = [
        (ROLE_LOGISTICS, 'Logistics'),
        (ROLE_PROJECT_MANAGER, 'Project Manager'),
        (ROLE_ENGINEER, 'Engineer'),
        (ROLE_OTHER, 'Other'),
    ]
    
    # OneToOneField means: one User has exactly one UserProfile
    # This is the standard Django pattern for extending the User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # delete profile when user is deleted
        related_name='profile',
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_OTHER,
    )
    
    def __str__(self):
        return f'{self.user.username} — {self.role}'
 
    
    