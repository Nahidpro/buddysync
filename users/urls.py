from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,ProfileView,TestView,ProtectedView

urlpatterns = [
    path('', TestView.as_view(), name='testview'),
    path('protectedview', ProtectedView.as_view(), name='protecttedview'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
