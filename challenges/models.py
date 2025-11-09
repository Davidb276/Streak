from django.db import models
from django.utils import timezone
from users.models import User

class Challenge(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def mark_completed(self):
        if not self.completed:
            self.completed = True
            self.score = self.challenge.points
            self.completed_at = timezone.now()
            self.save()
