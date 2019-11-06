from django.contrib.auth import get_user_model
from django.core.mail import mail_admins
from rest_framework import serializers
from main.models import Subject, Note, Link, NoteLike, LinkLike
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

UserModel = get_user_model()


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


class NoteLikeSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "NoteLike"
        model = NoteLike
        fields = (
            'id',
            'note',
            'user',
        )


class LinkLikeSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "LinkLike"
        model = LinkLike
        fields = (
            'id',
            'link',
            'user',
        )


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "Subject"
        model = Subject
        fields = (
            'id',
            'name',
        )


class NoteListSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

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


class NoteSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Subject.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=UserModel.objects.all())

    class Meta:
        ref_name = "Note"
        model = Note
        fields = (
            'id',
            'title',
            'body',
            'subjects',
            'user',
            'private',
            'date_created',
            'date_modified'
        )


class LinkListSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

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


class LinkSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Subject.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=UserModel.objects.all())

    class Meta:
        ref_name = "Link"
        model = Link
        fields = (
            'id',
            'title',
            'link',
            'subjects',
            'user',
            'private',
            'date_created',
            'date_modified'
        )


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


class SuggestionsSerializer(serializers.BaseSerializer):
    def to_representation(self, value: list):
        result = {'suggestions': []}
        if value:
            result['suggestions'] = [option.text for option in value]
        return result
