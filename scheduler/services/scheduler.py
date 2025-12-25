from scheduler.models import Worker, StaffingRequirement, Shift

def generate_schedule():
    workers = list(Worker.objects.all())
    requirements = StaffingRequirement.objects.all().order_by(
        "day_of_week", "hour"
    )

    worker_hours = {w.id: 0 for w in workers}

    Shift.objects.all().delete()

    for req in requirements:
        candidates = sorted(
            workers,
            key=lambda w: (-w.priority, worker_hours[w.id])
        )

        assigned = 0
        for worker in candidates:
            if worker_hours[worker.id] < worker.max_hours_per_week:
                Shift.objects.create(
                    worker=worker,
                    day_of_week=req.day_of_week,
                    hour=req.hour
                )
                worker_hours[worker.id] += 1
                assigned += 1

            if assigned == req.required_workers:
                break

        if assigned < req.required_workers:
            raise Exception(
                f"Not enough workers for day {req.day_of_week}, hour {req.hour}"
            )
