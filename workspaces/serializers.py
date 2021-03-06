from djoser.conf import User
from rest_framework import serializers
from workspaces.models import SearchResult, Organization, Workspace, Channel, Message


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchResult
        fields = ('type', 'content',)


class OrganizationSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    people = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    admin_flag = serializers.SerializerMethodField(
        method_name='get_admin_flag')

    def get_admin_flag(self, instance):
        admin = instance.admin
        user = self.context['request'].user
        return user == admin

    def create(self, validated_data):
        people = []
        if "people" in validated_data:
            people = validated_data["people"]
            del validated_data["people"]
        organization = Organization.objects.create(**validated_data)
        for user in people:
            organization.people.add(user)
        admin = organization.admin
        if admin not in organization.people.all():
            organization.people.add(admin)
        return organization

    class Meta:
        model = Organization
        fields = ('id', 'title', 'description',
                  'admin', 'admin_flag', 'people')


class WorkspaceSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    organization = serializers.HiddenField(
        default=1,
    )
    people = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    admin_flag = serializers.SerializerMethodField(
        method_name='get_admin_flag')

    def get_admin_flag(self, instance):
        admin = instance.admin
        user = self.context['request'].user
        return user == admin

    def create(self, validated_data):
        organization = Organization.objects.get(
            pk=self.context["view"].kwargs["organization_pk"])
        validated_data["organization"] = organization
        people = []
        if "people" in validated_data:
            people = validated_data["people"]
            del validated_data["people"]
        workspace = Workspace.objects.create(**validated_data)
        for user in people:
            workspace.people.add(user)
        admin = workspace.admin
        if admin not in workspace.people.all():
            workspace.people.add(admin)
        return workspace

    class Meta:
        model = Workspace
        fields = ('id', 'title', 'description', 'organization',
                  'admin', 'admin_flag', 'people')


class ChannelSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    organization = serializers.HiddenField(
        default=1,
    )
    people = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    admin_flag = serializers.SerializerMethodField(
        method_name='get_admin_flag')

    def get_admin_flag(self, instance):
        admin = instance.admin
        user = self.context['request'].user
        return user == admin

    def create(self, validated_data):
        organization = Organization.objects.get(
            pk=self.context["view"].kwargs["organization_pk"])
        validated_data["organization"] = organization
        people = []
        if "people" in validated_data:
            people = validated_data["people"]
            del validated_data["people"]
        channel = Channel.objects.create(**validated_data)
        for user in people:
            channel.people.add(user)
        admin = channel.admin
        if admin not in channel.people.all():
            channel.people.add(admin)
        return channel

    class Meta:
        model = Channel
        fields = ('id', 'title', 'description', 'organization',
                  'admin', 'admin_flag', 'people')


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    channel = serializers.HiddenField(
        default=1,
    )
    author_name = serializers.SerializerMethodField(
        method_name='get_author_name')
    mine_flag = serializers.SerializerMethodField(
        method_name='get_mine_flag')

    def get_author_name(self, instance):
        return instance.author.username

    def get_mine_flag(self, instance):
        author = instance.author
        user = self.context['request'].user
        return user == author

    def create(self, validated_data):
        channel = Channel.objects.get(
            pk=self.context["view"].kwargs["channel_pk"])
        validated_data["channel"] = channel
        message = Message.objects.create(**validated_data)
        return message

    class Meta:
        model = Message
        fields = ('id', 'content', 'channel',
                  'author', 'author_name', 'mine_flag')
