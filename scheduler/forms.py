from django import forms
from .models import BarConfig, Worker

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["name", "priority", "max_hours_per_week"]
        widgets = {
            "priority": forms.NumberInput(attrs={
                "type": "range",
                "min": 1,
                "max": 10,
                "step": 1
            })
        }



class BarConfigForm(forms.ModelForm):
    class Meta:
        model = BarConfig
        fields = ["opening_hour", "closing_hour"]
        widgets = {
            "opening_hour": forms.Select(choices=[(i, f"{i}:00") for i in range(24)]),
            "closing_hour": forms.Select(choices=[(i, f"{i}:00") for i in range(24)])
        }
