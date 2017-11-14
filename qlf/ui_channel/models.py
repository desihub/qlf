from django.db import models

# Create your models here.

class QlfState(models.Model):
    class Meta:
        abstract = True

    running = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(QlfState, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        try:
            obj = cls.objects.get(pk=1)
        except:
            obj = cls(pk=1)
        return obj
