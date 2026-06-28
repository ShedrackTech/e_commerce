# shop/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Return the authenticated user's profile."""
    return Response({
        'id':       request.user.id,
        'email':    request.user.email,
        'name':     request.user.get_full_name(),
        'profile':  request.user.has_complete_profile,
    })