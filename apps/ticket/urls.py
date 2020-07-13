from django.urls import path
from . import views


urlpatterns = [
    path('ticket/template', views.TicketTemplateApiView.as_view(), name='ticket_template'),

]

