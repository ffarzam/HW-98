from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"
    status_choice = [
        (TODO, 'Todo'),
        (DOING, 'Doing'),
        (DONE, 'Done'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=status_choice)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)

    def get_tags(self):
        task = Task.objects.get(id=self.id)
        tags = task.tag.all()
        return list(tags)

    def __str__(self):
        return f"{self.title}"