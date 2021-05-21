from datetime import date

from django.db import models


class StatView(models.Model):
    date = models.DateField(default=date.today)
