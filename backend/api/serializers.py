from django.contrib.auth.models import User
from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rag.models import Document, DocumentVersion




class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }

        return data



class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    chunks = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "source_name",
            "source_type",
            "source_uri",
            "status",
            "version",
            "chunks",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "version",
            "chunks",
            "created_at",
        ]

    def get_status(self, obj):
        latest_version = obj.versions.order_by("-created_at").first()

        if not latest_version:
            return "pending"

        return latest_version.processing_status

    def get_version(self, obj):
        return obj.versions.count()

    def get_chunks(self, obj):
        latest_version = obj.versions.order_by("-created_at").first()

        if not latest_version:
            return 0

        return latest_version.chunks.count()
    status = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    chunks = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "source_name",
            "source_type",
            "source_uri",
            "status",
            "version",
            "chunks",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "version",
            "chunks",
            "created_at",
        ]

    def get_status(self, obj):
        latest_version = obj.versions.order_by("-created_at").first()

        if not latest_version:
            return "pending"

        return latest_version.processing_status

    def get_version(self, obj):
        return obj.versions.count()

    def get_chunks(self, obj):
        latest_version = obj.versions.order_by("-created_at").first()

        if not latest_version:
            return 0

        return latest_version.chunks.count()