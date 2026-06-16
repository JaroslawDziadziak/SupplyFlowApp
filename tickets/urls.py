# URL routing for the tickets API endpoints
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router automatically generates URL patterns for ViewSets
router = DefaultRouter()

router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'comments', views.TicketCommentViewSet, basename='ticketcomment')

urlpatterns = [
    path('', include(router.urls)),
    # Registration endpoint — handled manually (not a ViewSet, so router can't auto-generate it)
    path('register/', views.RegisterView.as_view(), name='register'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('me/', views.CurrentUserView.as_view(), name='me'),
]
