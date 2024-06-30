from django.urls import path
from .views import AddContactView, UpdateUserActivityView

urlpatterns = [
    path('contacts/add/', AddContactView.as_view(), name='add-contact'),
    path('user/activity/update/', UpdateUserActivityView.as_view(), name='update-user-activity'),
]
