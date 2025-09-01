from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name

class Technology(models.Model):
    name = models.CharField(max_length=60, unique=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name

class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', related_name="projects", blank=True)
    technologies = models.ManyToManyField('Technology', related_name="projects", blank=True)
    class Meta: ordering = ["title"]
    def __str__(self): return self.title

class ProjectLink(models.Model):
    project = models.ForeignKey(Project, related_name="links", on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    class Meta:
        ordering = ["label"]
        unique_together = (("project", "label"),)
    def __str__(self): return f"{self.project} :: {self.label}"

class Experience(models.Model):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    started_at = models.DateField()
    finished_at = models.DateField(null=True, blank=True)
    technologies = models.ManyToManyField('Technology', related_name="experiences", blank=True)
    class Meta: ordering = ["-started_at"]
    def __str__(self): return f"{self.role} - {self.company}"

class Education(models.Model):
    institution = models.CharField(max_length=120)
    course = models.CharField(max_length=120)
    started_at = models.DateField()
    finished_at = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    class Meta: ordering = ["-started_at"]
    def __str__(self): return f"{self.institution} - {self.course}"
