# # posts/views.py
# from django.shortcuts import render
# from django.http import JsonResponse 
# from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_http_methods
# from .models import *

# def hello_world(request):
#     if request.method == "GET":
#         return JsonResponse({
#             'status' : 200,
#             'data' : "Hello likelion-14th!"
#         })
    
# def index(request):
#     return render(request, 'index.html')

# # 게시글 단일조회(GET), 수정(PATCH), 삭제(DELETE) 로직
# @require_http_methods(["GET", "PATCH", "DELETE"])
# def post_detail(request, post_id):

#     if request.method == "GET":
#         post = get_object_or_404(Post, pk=post_id) # post_id에 해당하는 Post 객체를 가져오거나, 없으면 404 에러 반환

#         post_detail_json = {
#             "id" : post.id,
#             "title" : post.title,
#             "content" : post.content,
#             "status" : post.status,
#             "writer" : post.writer.username
#         }
#         return JsonResponse({
#             "status" : 200,
#             'message' : '게시글 단일 조회 성공',
#             "data": post_detail_json})
    
#     if request.method == "PATCH":
#         body = json.loads(request.body.decode('utf-8'))

#         post_update = get_object_or_404(Post, pk=post_id)

#         if 'title' in body:
#             post_update.title = body['title']
#         if 'content' in body:
#             post_update.content = body['content']
#         if 'status' in body:
#             post_update.status = body['status']
        
#         post_update.save()

#         post_update_json = {
#             "id" : post_update.id,
#             "title" : post_update.title,
#             "content" : post_update.content,
#             "status" : post_update.status,
#             "writer" : post_update.writer.username
#         }

#         return JsonResponse({
#             'status': 200,
#             'message' : '게시글 수정 성공',
#             'data' : post_update_json
#         })
    
#     if request.method == "DELETE":
#         post_delete = get_object_or_404(Post, pk=post_id)
#         post_delete.delete()

#         return JsonResponse({
#             'status' : 200,
#             'message' : '게시글 삭제 성공',
#             'data' : None
#         })


# # 게시글 리스트 조회
# import json

# # 게시글을 Post(Create), Get(Read) 하는 뷰 로직
# @require_http_methods(["POST", "GET"])   #함수 데코레이터, 특정 http method 만 허용합니다
# def post_list(request):

#     # 게시글 생성(POST)
#     if request.method == "POST":

#         # request.body의 byte -> 문자열 -> python 딕셔너리
#         body = json.loads(request.body.decode('utf-8'))

#         # 프론트에게서 user id를 넘겨받는다고 가정.
# 				# 외래키 필드의 경우, 객체 자체를 전달해줘야하기 때문에
#         # id를 기반으로 user 객체를 조회해서 가져옵니다 !
#         user_id = body.get('user')
#         user = get_object_or_404(User, pk=user_id)

#         # 새로운 데이터를 DB에 생성
#         new_post = Post.objects.create(
#             title = body['title'],
#             content = body['content'],
#             status = body['status'],
#             writer = user
#         )

#         # Json 형태 반환 데이터 생성
#         new_post_json = {
#             "id" : new_post.id,
#             "title" : new_post.title,
#             "content" : new_post.content,
#             "status" : new_post.status,
#             "writer" : new_post.writer.username
#         }

#         return JsonResponse({
#             'status' : 200,
#             'message' : '게시글 생성 성공',
#             'data' : new_post_json
#         })

#     # 게시글 리스트 조회(GET)
#     if request.method == "GET":
#         category_id = request.GET.get('category')

#         posts = Post.objects.all()

#         # 카테고리 필터
#         if category_id:
#             posts = posts.filter(categories__id=category_id)

#         # 최신순 정렬
#         posts = posts.order_by('-created_at')

#         post_all_json = []

#         for post in posts: 
#             post_json = {
#                 "id": post.id,
#                 "title": post.title,
#                 "content": post.content,
#                 "status": post.status,
#                 "writer": post.writer.username
#             }
#             post_all_json.append(post_json)

#         return JsonResponse({
#             'status': 200,
#             'message': '게시글 목록 조회 성공',
#             'data': post_all_json
#         })

# # 특정 게시글의 댓글 리스트 조회
# def comment_list(request, post_id):
#     comments = Comment.objects.filter(post_id=post_id)

#     data = []
#     for comment in comments:
#         data.append({
#             "id": comment.id,
#             "content": comment.content,
#             "writer": comment.writer.username if comment.writer else None,
#             "created_at": comment.created_at
#         })

#     return JsonResponse({
#         "status": 200,
#         "message": "댓글 조회 성공",
#         "data": data
#     }

### DRF 관련 import - APIView 사용

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Image

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly # jwt 세션
from datetime import datetime
from rest_framework import permissions
from config.permissions import IsNotCurfewTime, IsOwnerOrReadOnly
    
from django.core.files.storage import default_storage  
from .serializers import ImageSerializer
from django.conf import settings
import boto3
import uuid
import os

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]   # ← 추가

    @swagger_auto_schema(
        operation_summary="이미지 업로드",
        operation_description="이미지 파일을 S3에 업로드하고, 업로드된 URL을 DB에 저장합니다.",
        manual_parameters=[
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="업로드할 이미지 파일",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={201: ImageSerializer, 400: "이미지 파일 없음"}
    )
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        ext = os.path.splitext(image_file.name)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = f"uploads/{unique_filename}"

        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
        
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostList(APIView):
    permission_classes = [IsNotCurfewTime, IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="새로운 게시글을 생성합니다.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "잘못된 요청"},
    )
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="모든 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    permission_classes = [IsNotCurfewTime, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시글 상세 조회",
        operation_description="post_id에 해당하는 게시글 하나를 조회합니다.",
        responses={200: PostSerializer, 404: "게시글을 찾을 수 없음"}
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="게시글 수정",
        operation_description="post_id에 해당하는 게시글을 수정합니다. (작성자만 가능)",
        request_body=PostSerializer,
        responses={200: PostSerializer, 400: "잘못된 요청", 403: "권한 없음", 404: "게시글을 찾을 수 없음"}
    )
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        operation_description="post_id에 해당하는 게시글을 삭제합니다. (작성자만 가능)",
        responses={200: "삭제 성공", 403: "권한 없음", 404: "게시글을 찾을 수 없음"}
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(
            {"message": "게시글이 성공적으로 삭제되었습니다.", "post_id": post_id},
            status=status.HTTP_200_OK
        )

class CommentList(APIView):
    permission_classes = [IsNotCurfewTime]

    @swagger_auto_schema(
        operation_summary="댓글 목록 조회",
        operation_description="post_id에 해당하는 게시글의 모든 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="댓글 작성",
        operation_description="post_id에 해당하는 게시글에 새 댓글을 작성합니다.",
        request_body=CommentSerializer,
        responses={201: CommentSerializer, 400: "잘못된 요청"}
    )
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id=post_id) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [IsNotCurfewTime, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="댓글 삭제",
        operation_description="comment_id에 해당하는 댓글을 삭제합니다. (작성자만 가능)",
        responses={200: "삭제 성공", 403: "권한 없음", 404: "댓글을 찾을 수 없음"}
    )
    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(
            {"message": "댓글이 성공적으로 삭제되었습니다.",
             "post_id": post_id,
             "comment_id": comment_id
            },
            status=status.HTTP_200_OK
        )

from config.custom_exceptions import PostNotFoundException # 추가 - 커스텀 예외처리 실습용

@require_http_methods(["GET"])
def get_post_detail(reqeust, id):
    try:
        post = Post.objects.get(id=id)
        post_detail_json = {
            "id" : post.id,
            "title" : post.title,
            "content" : post.content,
            "status" : post.status,
            "user" : post.user.username
        }
        return JsonResponse({
            "status" : 200,
            "data": post_detail_json})
    except Post.DoesNotExist:
        raise PostNotFoundException