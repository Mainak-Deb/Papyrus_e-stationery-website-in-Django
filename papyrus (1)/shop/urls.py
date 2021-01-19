from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index,name='home'),
    path('home/', views.index,name='home'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('checkout/', views.checkout,name='checkout'),
    path("signup/", views.handleSignup, name="handleSignup"),
	path("login/", views.handleLogin, name="handleLogin"),
	path("logout/", views.handleLogout, name="handleLogout"),
    path("search/", views.search, name="Search"),
    path("catagory/<str:cats>/", views.catagory, name="catagory"),
    path("sales/", views.sales, name="sales"),
    path("tracker/", views.tracker, name="tracker"),
]
