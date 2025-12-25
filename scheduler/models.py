from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)
    max_hours_per_week = models.IntegerField()

    def __str__(self):
        return self.name


class BarConfig(models.Model):
    opening_hour = models.IntegerField(default=4)  # 0–23
    closing_hour = models.IntegerField(default=23)  # 0–23
    max_workers_per_hour = models.IntegerField(default=4)
    closed_days = models.JSONField(default=list)  # [0, 6] = Mon & Sun closed



class StaffingRequirement(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    hour = models.IntegerField()  # 0–23
    required_workers = models.IntegerField()


class Shift(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    hour = models.IntegerField()

    def __str__(self):
        return f"{self.worker.name} - Day {self.day_of_week} @ {self.hour}:00"
