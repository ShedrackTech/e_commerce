"""config URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.serializers import ShopTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('shop.urls', namespace='shop')),
    path('api/token/', ShopTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)