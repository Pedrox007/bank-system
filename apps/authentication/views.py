from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer
from resources.permissions.permissions import IsTheUserOrReadOnly

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsTheUserOrReadOnly]
