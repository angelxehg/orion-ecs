from rest_framework import serializers
from . import models


class OrganizationSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Organization
        fields = ('id', 'title', 'description', 'admin')


class WorkspaceSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    parent = serializers.HiddenField(
        default=3,
    )

    def create(self, validated_data):
        parent = models.Organization.objects.get(pk=self.context["view"].kwargs["organization_pk"])
        validated_data["parent"] = parent
        return models.Workspace.objects.create(**validated_data)

    class Meta:
        model = models.Workspace
        fields = ('id', 'title', 'description', 'admin', 'parent')
