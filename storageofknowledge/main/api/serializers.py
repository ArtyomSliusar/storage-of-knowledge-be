from django.contrib.auth import get_user_model
from django.core.mail import mail_admins
from rest_framework import serializers
from main.models import Subject, Note, Link
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

UserModel = get_user_model()


class SubjectsField(serializers.RelatedField):

    def to_representation(self, value):
        return value.name


class LikesField(serializers.RelatedField):

    def to_representation(self, value):
        return value.name


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        message = self.validated_data['message']
        mail_admins(
            subject=f"Feedback from: {name} ({email})",
            message=f"{message}"
        )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    # TODO: correspond to JWT package errors
    default_error_messages = {
        'bad_token': _('Refresh token is invalid or expired')
    }

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError:
            self.fail('bad_token')


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "Subject"
        model = Subject
        fields = (
            'id',
            'name',
        )


class NoteListSerializer(serializers.ModelSerializer):
    subjects = SubjectsField(many=True, read_only=True)
    user = serializers.StringRelatedField(source="user.username")
    likes_count = serializers.SerializerMethodField()

    class Meta:
        ref_name = "NoteList"
        model = Note
        fields = (
            'id',
            'title',
            'subjects',
            'user',
            'private',
            'likes_count',
            'date_modified'
        )

    def get_likes_count(self, obj):
        return obj.likes.count()


class LinkListSerializer(serializers.ModelSerializer):
    subjects = SubjectsField(many=True, read_only=True)
    user = serializers.StringRelatedField(source="user.username")
    likes_count = serializers.SerializerMethodField()

    class Meta:
        ref_name = "LinkList"
        model = Link
        fields = (
            'id',
            'title',
            'subjects',
            'user',
            'private',
            'likes_count',
            'date_modified'
        )

    def get_likes_count(self, obj):
        return obj.likes.count()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
