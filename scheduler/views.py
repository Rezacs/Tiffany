from django.shortcuts import render, redirect
from .models import Worker, StaffingRequirement
from .forms import WorkerForm

def worker_list(request):
    workers = Worker.objects.all()
    return render(request, "workers/list.html", {"workers": workers})

def worker_create(request):
    form = WorkerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("worker_list")
    return render(request, "workers/form.html", {"form": form})

def staffing_grid(request):
    days = range(7)
    hours = range(4, 20)  # dynamically later from BarConfig

    if request.method == "POST":
        StaffingRequirement.objects.all().delete()

        for day in days:
            for hour in hours:
                value = int(request.POST.get(f"d{day}_h{hour}", 1))
                StaffingRequirement.objects.create(
                    day_of_week=day,
                    hour=hour,
                    required_workers=value
                )
        return redirect("worker_list")

    return render(request, "staffing/grid.html", {
        "days": days,
        "hours": hours
    })

from .models import Shift
from .services.scheduler import generate_schedule

def generate_schedule_view(request):
    generate_schedule()
    return redirect("schedule_view")


def schedule_view(request):
    shifts = Shift.objects.all().order_by("day_of_week", "hour")

    # Build structure: schedule[day][hour] = [workers]
    schedule = {}
    for shift in shifts:
        schedule.setdefault(shift.day_of_week, {})
        schedule[shift.day_of_week].setdefault(shift.hour, [])
        schedule[shift.day_of_week][shift.hour].append(shift.worker.name)

    days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    hours = sorted({s.hour for s in shifts})

    return render(request, "schedule/view.html", {
        "schedule": schedule,
        "days": days,
        "hours": hours
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import StaffingRequirement, BarConfig


@csrf_exempt
def staffing_config_view(request):

    # ALWAYS get or create bar config first
    bar, _ = BarConfig.objects.get_or_create(
        id=1,
        defaults={
            "opening_hour": 0,
            "closing_hour": 24,
            "max_workers_per_hour": 4,
            "closed_days": []
        }
    )

    # -------------------------------
    # POST: SAVE CONFIGURATION
    # -------------------------------
    if request.method == "POST":
        data = json.loads(request.body)

        # Update bar config
        bar.opening_hour = data["opening_hour"]
        bar.closing_hour = data["closing_hour"]
        bar.max_workers_per_hour = data["max_workers"]
        bar.closed_days = data.get("closed_days", [])
        bar.save()

        # Save staffing grid
        StaffingRequirement.objects.all().delete()

        for cell in data["cells"]:
            StaffingRequirement.objects.create(
                day_of_week=cell["day"],
                hour=cell["hour"],
                required_workers=cell["workers"]
            )

        return JsonResponse({"status": "ok"})

    # -------------------------------
    # GET: RENDER PAGE
    # -------------------------------
    saved = {}
    for req in StaffingRequirement.objects.all():
        saved.setdefault(req.day_of_week, {})
        saved[req.day_of_week][req.hour] = req.required_workers

    context = {
        "hours": range(24),
        "days": range(7),
        "day_names": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "opening_hour": bar.opening_hour,
        "closing_hour": bar.closing_hour,
        "max_workers": bar.max_workers_per_hour,
        "closed_days": bar.closed_days,
        "saved": saved,
    }

    return render(request, "config/staffing.html", context)

