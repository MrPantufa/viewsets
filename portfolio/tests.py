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

class ProjectSerializerTests(TestCase):
    def test_project_create_nested_links(self):
        data = {
            "title": "Portfolio",
            "slug": "portfolio",
            "description": "",
            "started_at": "2024-01-01",
            "finished_at": "2024-01-02",
            "links": [{"label": "Repo", "url": "https://github.com/me/proj"}],
        }
        ser = ProjectSerializer(data=data)
        assert ser.is_valid(), ser.errors
        obj = ser.save()
        assert obj.links.count() == 1

    def test_project_serializer_date_validation(self):
        data = {
            "title": "X",
            "slug": "x",
            "started_at": "2024-05-02",
            "finished_at": "2024-05-01",
        }
        ser = ProjectSerializer(data=data)
        assert not ser.is_valid()
        assert "finished_at" in ser.errors

class ExperienceEducationSerializersTests(TestCase):
    def test_experience_serializer_date_validation(self):
        data = {
            "company": "ACME",
            "role": "Dev",
            "started_at": "2024-05-02",
            "finished_at": "2024-05-01",
        }
        ser = ExperienceSerializer(data=data)
        assert not ser.is_valid()
        assert "finished_at" in ser.errors

    def test_education_serializer_date_validation(self):
        data = {
            "institution": "Uni",
            "course": "CS",
            "started_at": "2024-05-02",
            "finished_at": "2024-05-01",
        }
        ser = EducationSerializer(data=data)
        assert not ser.is_valid()
        assert "finished_at" in ser.errors

class ProjectLinkTests(TestCase):
    def test_unique_label_per_project(self):
        p = Project.objects.create(title="P", slug="p")
        ProjectLink.objects.create(project=p, label="Repo", url="https://x.com")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProjectLink.objects.create(project=p, label="Repo", url="https://y.com")
