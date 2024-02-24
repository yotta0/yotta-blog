from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status


def RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data

            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': 'Some error occurred',
                    },
                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(
                {
                    'data': serializer.data,
                    'message': 'User registered successfully',
                },
                status=status.HTTP_201_CREATED
            )

        except Exception:
            return Response({
                'data': None,
                'message': 'Some error occurred',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)