from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Guestbook
from .serializers import GuestbookSerializer

class GuestbookListCreateAPIView(APIView):
    
    # 1. 전체 조회 (GET 요청이 들어왔을 때)
    def get(self, request):
        # DB에서 모든 방명록 데이터를 가져오기
        guestbooks = Guestbook.objects.all()
        serializer = GuestbookSerializer(guestbooks, many=True)
        return Response(serializer.data)

    # 2. 방명록 작성 (POST 요청이 들어왔을 때)
    def post(self, request):
        serializer = GuestbookSerializer(data=request.data)
        
        # 데이터가 유효한지 검증
        if serializer.is_valid():
            # 검증에 성공시 DB에 저장
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 검증에 실패시
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestbookDetailAPIView(APIView):
    
    # 특정 번호(pk)의 게시글을 DB에서 가져오기
    def get_object(self, pk):
        try:
            return Guestbook.objects.get(pk=pk)
        except Guestbook.DoesNotExist:
            return None

    # 1. 특정 방명록 상세 조회 (GET 요청)
    def get(self, request, pk):
        guestbook = self.get_object(pk)
        if guestbook is None:
            return Response({"message": "해당 방명록을 찾을 수 없습니다. 다시 시도해주세요."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GuestbookSerializer(guestbook)
        return Response(serializer.data)

    # 2. 비밀번호 확인 후 삭제 (DELETE 요청)
    def delete(self, request, pk):
        guestbook = self.get_object(pk)
        if guestbook is None:
            return Response({"message": "해당 방명록을 찾을 수 없습니다. 다시 시도해주세요."}, status=status.HTTP_404_NOT_FOUND)
        
        input_password = request.data.get('password')
        
        if input_password == guestbook.password:
            # 비밀번호 일치시 DB에서 이 글을 삭제
            guestbook.delete()
            return Response({"message": "방명록이 성공적으로 삭제되었습니다. 다른 방명록을 쓰러 가볼까요?"}, status=status.HTTP_204_NO_CONTENT)
        
        # 비밀번호가 틀렸을시
        return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)