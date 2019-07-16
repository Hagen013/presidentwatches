from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserSerializer

User = get_user_model()


class SessionBasedLoginApiView(APIView):

    serializer_clas = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print('matsoy')
        print(username)
        print(password)
        print('tsoy')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            serializer = self.serializer_clas(
                user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            

class SessionBaseLogouApiView(APIView):

    def get(self, request):
        
        return Response({
        })
