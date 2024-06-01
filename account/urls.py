from django.urls import path

from .views import *

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("forgot", ForgotPass.as_view(), name="forgot-pass"),
    path("reset/verify", VerifyResetCode.as_view(), name="forgot-pass"),
    path("setpass", setPass.as_view(), name="forgot-pass"),
    path("signup", Signup.as_view(), name="signup"),
    path("logout", logout_view, name="logout"),
    path("phone/verify/<secret>", PhoneVerify.as_view(), name="phone-verify"),
    path("email/verify/<secret>", EmailVerify.as_view(), name="email-verify"),
    path("verify/<secret>", VerifyView.as_view(), name="verify"),
    path("user/profile", UserProfile, name="profile"),
    path("admin/user/profile/<int:id>", UserProfileDetails, name="profile-details"),
    path("user/session/signout/<str:key>", removeSessions, name="signout-session"),
    path("users", UserList.as_view(), name="userlist"),
    path("user/last-join", LastJoinUserList.as_view(), name="lastjoin-userlist"),
    path("user/search", UserSearch.as_view()),
]
