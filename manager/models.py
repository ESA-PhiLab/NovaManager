from django.contrib.auth.models import User
from django.db import models


class Machine(models.Model):
    uuid = models.UUIDField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.name}:{self.uuid}"
