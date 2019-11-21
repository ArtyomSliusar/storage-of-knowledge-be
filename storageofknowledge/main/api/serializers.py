import json
import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import mail_admins
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from main.models import Subject, Note, Link, NoteLike, LinkLike, NoteComment, UserConfirmationType
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

UserModel = get_user_model()
logger = logging.getLogger('app')


def _validate_recaptcha(value):
    """
    Validate recaptcha response
    """
    r = requests.post(settings.RECAPTCHA_URL, {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': value
    })
    if r.ok:
        decoded_r = json.loads(r.content.decode())
        if decoded_r['success']:
            return value
        else:
            r_error = decoded_r['error-codes']
    else:
        r_error = r.reason
    logger.error("recaptcha validation failed: {status} - {error}".format(
        status=r.status_code,
        error=r_error
    ))
    raise serializers.ValidationError("recaptcha validation error")


def _get_item_author(item):
    return {
        "id": item.user.id,
        "username": item.user.username,
    }


class UsernameEmail(serializers.Field):
    """
    """
    def to_internal_value(self, data):
        return UserModel.objects.get_by_username_or_email(data)


class ConfirmationType(serializers.Field):
    """
    """
    def to_internal_value(self, data):
        try:
            return UserConfirmationType.__getattr__(data.upper())
        except AttributeError:
            raise serializers.ValidationError()


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField()
    recaptcha = serializers.CharField()

    def validate_recaptcha(self, value):
        return _validate_recaptcha(value)

    def save(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        message = self.validated_data['message']
        mail_admins(
            subject=f"Feedback from: {name} ({email})",
            message=f"{message}"
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['time_zone'] = user.time_zone
        return token


class UserActivateSerializer(serializers.Serializer):
    username_email = UsernameEmail()
    activation_code = serializers.CharField()

    default_error_messages = {
        'incorrect_user_code': _('User not found or invalid/expired code provided'),
    }

    def save(self):
        user = self.validated_data['username_email']
        activation_code = self.validated_data['activation_code']
        if not user or user.activate(activation_code) is False:
            self.fail('incorrect_user_code')


class UserPasswordResetSerializer(serializers.Serializer):
    username_email = UsernameEmail()
    new_password = serializers.CharField(write_only=True)
    reset_password_code = serializers.CharField()

    default_error_messages = {
        'incorrect_user_code': _('User not found or invalid/expired code provided'),
    }

    def save(self):
        user = self.validated_data['username_email']
        new_password = self.validated_data['new_password']
        reset_password_code = self.validated_data['reset_password_code']
        if not user or user.reset_password(new_password, reset_password_code) is False:
            self.fail('incorrect_user_code')


class UserConfirmationSerializer(serializers.Serializer):
    username_email = UsernameEmail()
    type = ConfirmationType()
    recaptcha = serializers.CharField()

    def validate_recaptcha(self, value):
        return _validate_recaptcha(value)

    def save(self):
        user = self.validated_data['username_email']
        confirmation_type = self.validated_data['type']
        if user:
            user.send_confirmation(confirmation_type)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Refresh token is invalid or expired')
    }

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError:
            self.fail('bad_token')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class NoteCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # get current authenticated user
    username = serializers.CharField(source='user.username', read_only=True)
    reply_set = RecursiveField(many=True, read_only=True)

    class Meta:
        ref_name = "NoteComment"
        model = NoteComment
        fields = (
            'id',
            'parent',
            'user',
            'username',
            'note',
            'body',
            'reply_set',
            'date_created',
            'date_modified'
        )


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
    subjects = SubjectSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        ref_name = "NoteList"
        model = Note
        fields = (
            'id',
            'title',
            'subjects',
            'author',
            'private',
            'likes_count',
            'date_modified'
        )

    def get_author(self, obj):
        return _get_item_author(obj)


class NoteSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, source='subjects', queryset=Subject.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # get current authenticated user
    author = serializers.SerializerMethodField()

    class Meta:
        ref_name = "Note"
        model = Note
        fields = (
            'id',
            'title',
            'body',
            'subjects',
            'subjects_ids',
            'user',
            'author',
            'private',
            'date_created',
            'date_modified'
        )

    def get_author(self, obj):
        return _get_item_author(obj)


class LinkListSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        ref_name = "LinkList"
        model = Link
        fields = (
            'id',
            'title',
            'subjects',
            'author',
            'private',
            'likes_count',
            'date_modified'
        )

    def get_author(self, obj):
        return _get_item_author(obj)


class LinkSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, source='subjects', queryset=Subject.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # get current authenticated user
    author = serializers.SerializerMethodField()

    class Meta:
        ref_name = "Link"
        model = Link
        fields = (
            'id',
            'title',
            'link',
            'subjects',
            'subjects_ids',
            'user',
            'author',
            'private',
            'date_created',
            'date_modified'
        )

    def get_author(self, obj):
        return _get_item_author(obj)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    recaptcha = serializers.CharField(write_only=True)

    def validate_recaptcha(self, value):
        return _validate_recaptcha(value)

    def create(self, validated_data):
        validated_data.pop("recaptcha")
        user = UserModel.objects.create_user(**validated_data, is_active=False)
        user.send_confirmation(UserConfirmationType.ACTIVATION)
        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
            "password",
            "time_zone",
            "recaptcha"
        )


class SuggestionsSerializer(serializers.BaseSerializer):
    def to_representation(self, value: list):
        result = {'suggestions': []}
        if value:
            result['suggestions'] = [option.text for option in value]
        return result
