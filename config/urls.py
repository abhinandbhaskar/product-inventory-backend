"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from inventory.views import AdminTokenObtainPairView,AdminLogout,AddVariant,GetVariants,Delete_variant,AddSubVariant,GetSubVariants,DeleteSubVariant
from inventory.views import AddProductView,AddVariantMappingView,AddVariantCombinationView,GetProductLists,GetStocks,UpdateStock,GetStockReports
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/', AdminTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('adminlogout/',AdminLogout.as_view(),name='adminlogout'),
    path('add_variant/',AddVariant.as_view(),name='add_variant'),
    path('get_variants/',GetVariants.as_view(),name="get_variants"),
    path('delete_variant/<uuid:id>/', Delete_variant.as_view(), name="delete_variant"),
    path('add_subvariant/',AddSubVariant.as_view(),name="add_subvariant"),
    path('get_subvariants/',GetSubVariants.as_view(),name='get_subvariants'),
    path('delete_subvariant/<uuid:id>/',DeleteSubVariant.as_view(),name=""),

    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('add_variant_mapping/', AddVariantMappingView.as_view(), name='add_variant_mapping'),
    path('add_variant_combination/', AddVariantCombinationView.as_view(), name='add_variant_combination'),

    path('get_productlist/',GetProductLists.as_view(),name="get_productlist"),
    path('get_stocks/',GetStocks.as_view(),name='get_stocks'),
    path('update_stock/<uuid:id>/',UpdateStock.as_view(),name="update_stock"),
    path('get_stock_reports/',GetStockReports.as_view(),name='get_stock_reports'),



]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
