
from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import Tag, Technology, Project, ProjectLink
from .serializers import ProjectSerializer, ExperienceSerializer, EducationSerializer

class TagModelTests(TestCase):
    def test_tag_unique_name(self):
        Tag.objects.create(name="Django")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Tag.objects.create(name="Django")

class TechnologyModelTests(TestCase):
    def test_technology_unique_name(self):
        Technology.objects.create(name="Python")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Technology.objects.create(name="Python")

class ProjectModelTests(TestCase):
    def test_project_slug_unique(self):
        Project.objects.create(title="A", slug="a")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Project.objects.create(title="B", slug="a")

    def test_project_str(self):
        p = Project.objects.create(title="My Project", slug="my-project")
        self.assertEqual(str(p), "My Project")

class SerializerTests(TestCase):
    def setUp(self):
        self.t1 = Tag.objects.create(name="Web")
        self.t2 = Tag.objects.create(name="API")
        self.tech1 = Technology.objects.create(name="Django")
        self.tech2 = Technology.objects.create(name="DRF")

    def test_project_serializer_create_with_nested_links(self):
        data = {
            "title": "Site",
            "slug": "site",
            "description": "Desc",
            "started_at": "2024-01-01",
            "finished_at": "2024-02-01",
            "tags": [self.t1.id, self.t2.id],
            "technologies": [self.tech1.id, self.tech2.id],
            "links": [{"label": "GitHub", "url": "https://github.com/x"}, {"label": "Demo", "url": "https://demo.com"}],
        }
        ser = ProjectSerializer(data=data); assert ser.is_valid(), ser.errors
        project = ser.save()
        assert project.tags.count() == 2
        assert project.technologies.count() == 2
        assert project.links.count() == 2

    def test_project_serializer_date_validation(self):
        data = {"title": "Bad", "slug": "bad", "started_at": "2024-05-02", "finished_at": "2024-05-01"}
        ser = ProjectSerializer(data=data); assert not ser.is_valid(); assert "finished_at" in ser.errors

    def test_experience_serializer_date_validation(self):
        data = {"company": "ACME", "role": "Dev", "started_at": "2024-05-02", "finished_at": "2024-05-01"}
        ser = ExperienceSerializer(data=data); assert not ser.is_valid(); assert "finished_at" in ser.errors

    def test_education_serializer_date_validation(self):
        data = {"institution": "Uni", "course": "CS", "started_at": "2024-05-02", "finished_at": "2024-05-01"}
        ser = EducationSerializer(data=data); assert not ser.is_valid(); assert "finished_at" in ser.errors

class ProjectLinkTests(TestCase):
    def test_unique_label_per_project(self):
        p = Project.objects.create(title="P", slug="p")
        ProjectLink.objects.create(project=p, label="Repo", url="https://x.com")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProjectLink.objects.create(project=p, label="Repo", url="https://y.com")
