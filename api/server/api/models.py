from djongo import models

# Create your models here.

class Item(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    status = models.NullBooleanField()


class Line(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    items = models.ArrayField(
        model_container = Item,
    )


class Schedule(models.Model):
    _id = models.ObjectIdField()
    date = models.DateTimeField()
    shift = models.TextField()
    timestamp = models.FloatField()
    terminal = models.TextField()
    lines = models.ArrayField(
        model_container = Line
    )

    objects = models.DjongoManager()

    class Meta:
        ordering = ['date']