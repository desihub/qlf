from django.db import models

# Create your models here.

class QlfState(models.Model):
    daemon_status = models.BooleanField(default=False)
    upstream_status = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        try:
            obj = cls.objects.get(pk=1)
        except:
            obj = cls(pk=1)
        return obj
