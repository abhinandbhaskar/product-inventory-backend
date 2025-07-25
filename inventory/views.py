from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from inventory.serializers import AdminTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status




class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            print("access_token",access_token)
            print("refresh_token",refresh_token)
            
            if access_token and refresh_token:
                response.set_cookie(
                    'access_token',
                    access_token,
                    httponly=True,
                    samesite='Lax',
                    secure=False,
                    max_age=24 * 60 * 60,
                    path='/',
                )
                response.set_cookie(
                    'refresh_token',
                    refresh_token,
                    httponly=True,
                    samesite='Lax',
                    secure=False,
                    max_age=24 * 60 * 60,
                    path='/',
                )
                print("Cookies should be set!") 
            else:
                print("Tokens missing in response!") 
        
        return response


class AdminLogout(APIView):
    def post(self, request):
        try:
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            print("Access token in cookies:", access_token)
            print("Refresh token in cookies:", refresh_token)
            response = Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_200_OK
            )
            if access_token:
                response.delete_cookie('access_token')
            if refresh_token:
                response.delete_cookie('refresh_token')
            if hasattr(request, 'session'):
                request.session.flush()

            print("Logout successful. Cookies cleared.")
            return response

        except Exception as e:
            print("Logout error:", str(e))
            return Response(
                {"error": "Something went wrong during logout."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



from inventory.models import Variant
class AddVariant(APIView):
    def post(self,request):
        variant_name = request.data.get('variant')

        if not variant_name:
            return Response({"error":"Variant name is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            if Variant.objects.filter(name=variant_name).exists():
                return Response({"error":"Variant with this name already exists"},status=status.HTTP_400_BAD_REQUEST)
            variant=Variant.objects.create(name=variant_name)
            return Response({"message":"variant created successfully"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

from inventory.serializers import GetVariantsSerializer
class GetVariants(APIView):
    def get(self,request):
        variants=Variant.objects.all()
        serializer=GetVariantsSerializer(variants,many=True)
        return Response(serializer.data)

class Delete_variant(APIView):
    def post(self, request, id):
        try:
            variant = Variant.objects.get(id=id)
            variant.delete()
            return Response({"message": "Deleted Successfully..."}, status=status.HTTP_200_OK)
        except Variant.DoesNotExist:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from inventory.models import SubVariant

class AddSubVariant(APIView):
    def post(self, request):
        variant_id = request.data.get('variant_id')  
        value = request.data.get('value')

        if not value:
            return Response({"error": "SubVariant value is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not variant_id:
            return Response({"error": "Variant ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            variant = Variant.objects.get(id=variant_id)
            
            if SubVariant.objects.filter(variant=variant, value=value).exists():
                return Response({"error": "SubVariant with this value already exists for this variant"},status=status.HTTP_400_BAD_REQUEST)
            SubVariant.objects.create(variant=variant, value=value)
            return Response({"message": "SubVariant created successfully"},status=status.HTTP_201_CREATED)
        
        except Variant.DoesNotExist:
            return Response({"error": "Variant not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

from inventory.serializers import GetSubVariantsSerializer
class GetSubVariants(APIView):
    def get(self, request):
        try:
            variants = SubVariant.objects.all().select_related('variant')
            serializer = GetSubVariantsSerializer(variants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteSubVariant(APIView):
    def post(self, request, id):
        try:
            variant = SubVariant.objects.get(id=id)
            variant.delete()
            return Response({"message": "Deleted Successfully..."}, status=status.HTTP_200_OK)
        except SubVariant.DoesNotExist:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Products, Variant, ProductVariantMap, ProductVariantCombination, SubVariant
from .serializers import ProductSerializer, VariantMappingSerializer, VariantCombinationSerializer, SubVariantSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import AccessToken
from inventory.models import Products
from inventory.serializers import ProductSerializer,ProductSerializer1



class AddProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        data['CreatedUser'] = request.user.id
        if 'productCode' in data:
            data['ProductCode'] = data.pop('productCode')

        serializer = ProductSerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': serializer.data['id'],
                'message': 'Product added successfully!'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddVariantMappingView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')
        if ProductVariantMap.objects.filter(product_id=product_id, variant_id=variant_id).exists():
            return Response({'error': 'Mapping already exists'}, status=400)
        
        mapping = ProductVariantMap.objects.create(
            product_id=product_id,
            variant_id=variant_id
        )
        
        return Response({'message': 'Variant mapping added!'}, status=201)

class AddVariantCombinationView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        combination_code = request.data.get('combination_code')
        stock = request.data.get('stock')
        option_value = request.data.get('option_value')
        variant_id = request.data.get('variant_id')
        
        if ProductVariantCombination.objects.filter(
            product_id=product_id, 
            combination_code=combination_code
        ).exists():
            return Response({'error': 'Combination exists'}, status=400)
        
        combination = ProductVariantCombination.objects.create(
            product_id=product_id,
            combination_code=combination_code,
            stock=stock
        )
        
        if option_value and variant_id:
            variant = Variant.objects.get(id=variant_id)
            subvariant, created = SubVariant.objects.get_or_create(
                variant=variant,
                value=option_value
            )
            combination.subvariants.add(subvariant)
        
        return Response({'message': 'Variant combination added!'}, status=201)

from inventory.serializers import GetProductListsSerializer



import logging
from rest_framework.pagination import PageNumberPagination
from inventory.serializers import GetProductListsSerializer  
logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class GetProductLists(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        try:
            logger.info(f"GetProductLists API accessed by user: {request.user.username}")
            obj = Products.objects.all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(obj, request)
            serializer = GetProductListsSerializer(page, many=True)
            logger.debug(f"GetProductLists API successful response for user: {request.user.username}")
            
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error in GetProductLists API for user {request.user.username}: {str(e)}", 
                        exc_info=True)
            return Response({"error": "An error occurred while processing your request."}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from inventory.models import ProductVariantCombination,StockTransaction
from inventory.serializers import GetStocksSerializer
class GetStocks(APIView):
    def get(self,request):
        obj=ProductVariantCombination.objects.all()
        serializer=GetStocksSerializer(obj,many=True)
        return Response(serializer.data)
    


from decimal import Decimal, InvalidOperation



class UpdateStock(APIView):
    def post(self, request, id):
        user = request.user
        try:
            stock = request.data.get('stock')
            stock_type = request.data.get('stockType')

            if stock is None:
                return Response({"error": "Stock value is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stock = Decimal(stock)
            except (ValueError, InvalidOperation):
                return Response({"error": "Invalid stock value."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                obj = ProductVariantCombination.objects.get(id=id)
            except ProductVariantCombination.DoesNotExist:
                return Response({"error": "Product variant not found."}, status=status.HTTP_404_NOT_FOUND)

            product = obj.product  

            if stock_type == "IN":
                obj.stock += stock
                product.TotalStock = (product.TotalStock or Decimal(0)) + stock
            elif stock_type == "OUT":
                if obj.stock < stock:
                    return Response({"error": "Insufficient stock."}, status=status.HTTP_400_BAD_REQUEST)
                obj.stock -= stock
                product.TotalStock = (product.TotalStock or Decimal(0)) - stock
                if product.TotalStock < 0:
                    product.TotalStock = Decimal(0)
            else:
                return Response({"error": "Invalid stockType. Use 'IN' or 'OUT'."}, status=status.HTTP_400_BAD_REQUEST)

            obj.save()
            product.UpdatedDate = timezone.now() 
            product.save()

            StockTransaction.objects.create(
                product_variant=obj,
                transaction_type=stock_type,
                quantity=stock,
                user=user
            )

            return Response({"message": "Stock updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from inventory.models import StockTransaction
from inventory.serializers import GetStockTransactionSerializer

from datetime import date
from django.utils import timezone


from django.db import models

class GetStockReports(APIView):
    def get(self, request):
        all_transactions = StockTransaction.objects.all()
        serializer = GetStockTransactionSerializer(all_transactions, many=True)
        total_products = Products.objects.count()
        stock_sum = Products.objects.aggregate(total=models.Sum('TotalStock'))['total'] or 0
        today = date.today()
        today_transactions = StockTransaction.objects.filter(date__date=today)
        todaystockin = today_transactions.filter(transaction_type="IN").aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        todaystockout = today_transactions.filter(transaction_type="OUT").aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        context = {
            "data": serializer.data,
            "total_products": total_products,
            "totalstocks": float(f"{stock_sum:.2f}"),
            "todaystockin": float(f"{todaystockin:.2f}"),
            "todaystockout": float(f"{todaystockout:.2f}")
        }
        return Response(context)