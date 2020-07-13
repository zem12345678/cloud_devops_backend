from rest_framework.routers import DefaultRouter
from .views import TicketDetailViewSet 



ticket_router = DefaultRouter()
#ticket_router.register(r'ticket/template', TicketTemplateViewSet)
ticket_router.register(r'ticket', TicketDetailViewSet)
