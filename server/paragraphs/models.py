from django.db import models
from django.conf import settings


class Paragraph(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
# Create your models here.
