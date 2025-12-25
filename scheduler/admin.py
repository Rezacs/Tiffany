from django.contrib import admin
from .models import Worker, BarConfig, StaffingRequirement, Shift

admin.site.register(Worker)
admin.site.register(BarConfig)
admin.site.register(StaffingRequirement)
admin.site.register(Shift)
