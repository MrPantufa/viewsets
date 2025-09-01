from rest_framework import serializers
from .models import Tag, Technology, Project, ProjectLink, Experience, Education

class TagSerializer(serializers.ModelSerializer):
    class Meta: model = Tag; fields = ["id", "name"]

class TechnologySerializer(serializers.ModelSerializer):
    class Meta: model = Technology; fields = ["id", "name"]

class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta: model = ProjectLink; fields = ["id", "label", "url"]

class ProjectSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    technologies = serializers.PrimaryKeyRelatedField(queryset=Technology.objects.all(), many=True, required=False)
    links = ProjectLinkSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ["id","title","slug","description","started_at","finished_at",
                  "is_active","tags","technologies","links"]

    def validate(self, attrs):
        s = attrs.get("started_at", getattr(self.instance, "started_at", None))
        e = attrs.get("finished_at", getattr(self.instance, "finished_at", None))
        if s and e and e < s:
            raise serializers.ValidationError({"finished_at":"finished_at must be after started_at."})
        return attrs

    def create(self, validated_data):
        links_data = validated_data.pop("links", [])
        tags = validated_data.pop("tags", [])
        techs = validated_data.pop("technologies", [])
        project = Project.objects.create(**validated_data)
        if tags: project.tags.set(tags)
        if techs: project.technologies.set(techs)
        for ld in links_data:
            ProjectLink.objects.create(project=project, **ld)
        return project

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta: model = Experience; fields = ["id","company","role","description",
                                              "started_at","finished_at","technologies"]

    def validate(self, attrs):
        s = attrs.get("started_at", getattr(self.instance, "started_at", None))
        e = attrs.get("finished_at", getattr(self.instance, "finished_at", None))
        if s and e and e < s:
            raise serializers.ValidationError({"finished_at":"finished_at must be after started_at."})
        return attrs

class EducationSerializer(serializers.ModelSerializer):
    class Meta: model = Education; fields = ["id","institution","course","description",
                                             "started_at","finished_at"]

    def validate(self, attrs):
        s = attrs.get("started_at", getattr(self.instance, "started_at", None))
        e = attrs.get("finished_at", getattr(self.instance, "finished_at", None))
        if s and e and e < s:
            raise serializers.ValidationError({"finished_at":"finished_at must be after started_at."})
        return attrs
