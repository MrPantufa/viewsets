from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tag, Technology

class TagViewSetTests(APITestCase):
    def test_tag_crud_flow(self):
        url = reverse("tag-list")
        resp = self.client.post(url, {"name": "Django"}, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        tag_id = resp.data["id"]

        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        detail = reverse("tag-detail", args=[tag_id])
        resp = self.client.get(detail)
        assert resp.status_code == status.HTTP_200_OK

        resp = self.client.patch(detail, {"name": "Django REST"}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == "Django REST"

        resp = self.client.delete(detail)
        assert resp.status_code == status.HTTP_204_NO_CONTENT

class TechnologyViewSetTests(APITestCase):
    def test_technology_crud_flow(self):
        url = reverse("technology-list")
        resp = self.client.post(url, {"name": "Python"}, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        tech_id = resp.data["id"]

        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        detail = reverse("technology-detail", args=[tech_id])
        resp = self.client.get(detail)
        assert resp.status_code == status.HTTP_200_OK

        resp = self.client.put(detail, {"name": "Python 3"}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == "Python 3"

class ProjectViewSetTests(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Web")
        self.tag2 = Tag.objects.create(name="API")
        self.tech1 = Technology.objects.create(name="Django")
        self.tech2 = Technology.objects.create(name="DRF")

    def test_project_create_with_links_and_relations(self):
        url = reverse("project-list")
        payload = {
            "title": "Meu Site",
            "slug": "meu-site",
            "description": "Exemplo",
            "started_at": "2024-01-01",
            "finished_at": "2024-01-10",
            "tags": [self.tag1.id, self.tag2.id],
            "technologies": [self.tech1.id, self.tech2.id],
            "links": [
                {"label": "Repo", "url": "https://github.com/x"},
                {"label": "Demo", "url": "https://exemplo.com"},
            ],
        }
        resp = self.client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        detail = reverse("project-detail", args=[resp.data["id"]])
        resp = self.client.get(detail)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data.get("links", [])) == 2

    def test_project_date_validation_via_api(self):
        url = reverse("project-list")
        payload = {
            "title": "Datas ruins",
            "slug": "datas-ruins",
            "started_at": "2024-02-05",
            "finished_at": "2024-02-01",
        }
        resp = self.client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "finished_at" in resp.data


class ExperienceEducationAPITests(APITestCase):
    def test_experience_date_validation_via_api(self):
        url = reverse("experience-list")
        payload = {
            "company": "ACME",
            "role": "Dev",
            "started_at": "2024-06-05",
            "finished_at": "2024-06-01",
        }
        resp = self.client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "finished_at" in resp.data

    def test_education_date_validation_via_api(self):
        url = reverse("education-list")
        payload = {
            "institution": "Uni",
            "course": "CS",
            "started_at": "2024-06-05",
            "finished_at": "2024-06-01",
        }
        resp = self.client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "finished_at" in resp.data

