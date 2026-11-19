from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, DocumentSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
import os
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken
import hashlib
from rest_framework.parsers import MultiPartParser, FormParser
from rag.models import Document, DocumentVersion
from .services.document_processor import process_document_version
from api.services.retrieval_service import retrieve_chunks
from rest_framework.decorators import api_view, permission_classes
from api.services.rag_service import run_rag





def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "raglab-api",
    })


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Account created successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get("credential")

        if not credential:
            return Response(
                {"error": "Google credential is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            google_user = id_token.verify_oauth2_token(
                credential,
                requests.Request(),
                os.getenv("GOOGLE_CLIENT_ID"),
            )

        except ValueError:
            return Response(
                {"error": "Invalid Google credential."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = google_user.get("email")
        email_verified = google_user.get("email_verified", False)

        if not email or not email_verified:
            return Response(
                {"error": "Google email is not verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        if not user:
            username_base = email.split("@")[0]
            username = username_base
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{username_base}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
            )

            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        documents = (
            Document.objects
            .prefetch_related("versions__chunks")
            .order_by("-created_at")
        )

        serializer = DocumentSerializer(documents, many=True)

        return Response(serializer.data)


    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"detail": "No file was uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        filename = uploaded_file.name

        if "." not in filename:
            return Response(
                {"detail": "File must have an extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        extension = filename.rsplit(".", 1)[-1].lower()

        allowed_types = {
            "txt": "txt",
            "md": "md",
            "markdown": "md",
        }

        if extension not in allowed_types:
            return Response(
                {
                    "detail": (
                        "Unsupported file type. "
                        "Only TXT and Markdown files are supported."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_content = uploaded_file.read()

        content_hash = hashlib.sha256(file_content).hexdigest()
        source_type = allowed_types[extension]

        # Check whether this document already exists
        document = (
            Document.objects
            .filter(source_name=filename)
            .first()
        )

        if document:
            # Check whether this exact content already exists
            existing_version = (
                document.versions
                .filter(content_hash=content_hash)
                .first()
            )

            if existing_version:
                serializer = DocumentSerializer(document)

                return Response(
                    {
                        "detail": "Document already exists.",
                        "document": serializer.data,
                        "version_id": existing_version.id,
                    },
                    status=status.HTTP_200_OK,
                )

        # Create a new document if this filename has never been uploaded
        if not document:
            document = Document.objects.create(
                source_name=filename,
                source_type=source_type,
            )

        # New content for an existing document = new version
        document_version = DocumentVersion.objects.create(
            document=document,
            content_hash=content_hash,
            processing_status="pending",
        )

        try:
            process_document_version(
                document_version,
                file_content,
            )

        except UnicodeDecodeError:
            document_version.processing_status = "failed"
            document_version.save(update_fields=["processing_status"])

            return Response(
                {
                    "detail": (
                        "Could not decode the document. "
                        "Please use a UTF-8 encoded TXT or Markdown file."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            document_version.processing_status = "failed"
            document_version.save(update_fields=["processing_status"])

            return Response(
                {"detail": "Document processing failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = DocumentSerializer(document)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

class RetrievalView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get("query")
        top_k = request.data.get("top_k", 5)

        if not query or not query.strip():
            return Response(
                {"detail": "Query is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            top_k = int(top_k)

            if top_k < 1 or top_k > 50:
                return Response(
                    {"detail": "top_k must be between 1 and 50."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (TypeError, ValueError):
            return Response(
                {"detail": "top_k must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = retrieve_chunks(
            query=query,
            top_k=top_k,
        )

        response_results = []

        for index, result in enumerate(results, start=1):
            chunk = result["chunk"]

            response_results.append({
                "rank": index,
                "score": round(result["score"], 4),
                "document": chunk.document_version.document.source_name,
                "document_id": chunk.document_version.document.id,
                "chunk_id": chunk.id,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
            })

        return Response({
            "query": query,
            "top_k": top_k,
            "results": response_results,
        })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rag_view(request):
    query = request.data.get("query", "").strip()
    top_k = request.data.get("top_k", 5)
    strategy = request.data.get("strategy", "semantic")
    rerank = request.data.get("rerank", False)

    if not query:
        return Response(
            {"detail": "Query is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        top_k = int(top_k)

        if top_k <= 0:
            return Response(
                {"detail": "top_k must be greater than 0."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = run_rag(
            query,
            top_k=top_k,
            strategy=strategy,
            rerank=rerank,
        )

        return Response(result)

    except Exception as error:
        return Response(
            {"detail": str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )