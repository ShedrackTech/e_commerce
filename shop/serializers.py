# shop/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class ShopTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email']      = user.email
        token['full_name']  = user.get_full_name()
        token['is_staff']   = user.is_staff
        token['has_profile']= user.has_complete_profile
        return token
class ShopTokenObtainPairView(TokenObtainPairView):
    serializer_class = ShopTokenObtainPairSerializer