from django.contrib import admin
from .models import Ticket, TicketComment

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1
    readonly_fields = ('created_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    exclude = (
        'created_by',
    )
    list_display = (
        'title',
        'priority',
        'status',
        'assigned_to',
        'created_by',
        'created_at',
    )
    list_filter = (
        'priority',
        'status',
        'created_at',
    )
    search_fields = (
        'title',
        'description',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    inlines = (
        TicketCommentInline,
    )
    
    #Automaticly setting the creator when creating a ticket
    def seve_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(self, request, obj, form, change)

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'author',
        'created_at',
    )
    list_filter = (
        'created_at',
    )
    search_fields = (
        'content',
        'ticket_title'
    )
    readonly_fields = (
        'created_at',
    )


