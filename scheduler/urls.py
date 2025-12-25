from django.urls import path
from . import views

urlpatterns = [
    path("workers/", views.worker_list, name="worker_list"),
    path("workers/add/", views.worker_create, name="worker_create"),
    path("schedule/", views.schedule_view, name="schedule_view"),
    path("schedule/generate/", views.generate_schedule_view, name="generate_schedule"),
    path("config/staffing/", views.staffing_config_view, name="staffing_config"),
    path("config/staffing/", views.staffing_config_view, name="staffing_config"),

]
