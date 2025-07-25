from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from inventory.models import Variant,SubVariant

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user:
            raise AuthenticationFailed("User not registered or invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("This account is disabled. Please contact support.")
        
        if not hasattr(user, 'userprofile') or not user.userprofile.is_admin:
            raise AuthenticationFailed("Only admins can log in here.")

        if user.is_superuser:
            raise AuthenticationFailed("Superusers are not allowed to login here.")

        data["user_id"] = user.id
        data["username"] = user.username
        data["email"] = user.email

        return data





class GetVariantsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Variant
        fields = ['id', 'name']


from rest_framework import serializers
from inventory.models import SubVariant

class GetSubVariantsSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    
    class Meta:
        model = SubVariant
        fields = ['id', 'value', 'variant', 'variant_name']


from rest_framework import serializers
from .models import Products, ProductVariantMap, ProductVariantCombination, SubVariant

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {
            'ProductImage': {'required': False},
            'TotalStock': {'required': False},
            'HSNCode': {'required': False},
        }

class VariantMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantMap
        fields = ['product', 'variant']

class VariantCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantCombination
        fields = ['product', 'combination_code', 'stock']

class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['id', 'variant', 'value']

from rest_framework import serializers

class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['value']

class VariantSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = Variant
        fields = ['name', 'options']
    
    def get_options(self, obj):
        subvariants = obj.options.all()
        return [sv.value for sv in subvariants]

class ProductVariantMapSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()
    
    class Meta:
        model = ProductVariantMap
        fields = ['variant'] 


class GetProductListsSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = ['ProductName', 'variants','ProductID','ProductCode','ProductImage','HSNCode','TotalStock']  # Add other fields if needed
    
    def get_variants(self, obj):
        variant_mappings = obj.variant_mappings.all()
        serializer = ProductVariantMapSerializer(variant_mappings, many=True)
        
        variants_data = [item['variant'] for item in serializer.data]
        return variants_data


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields = ['ProductName','ProductID','ProductCode','ProductImage'] 

from inventory.models import ProductVariantCombination
class GetStocksSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()  

    class Meta:
        model = ProductVariantCombination
        fields = ['id','stock', 'product']


from inventory.models import Products 



class ProductSerializer1(serializers.ModelSerializer):
    ProductID = serializers.IntegerField(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

    def validate_ProductCode(self, value):
        if Products.objects.filter(ProductCode=value).exists():
            raise serializers.ValidationError("This ProductCode already exists.")
        return value

    def create(self, validated_data):
        last_product = Products.objects.order_by('-ProductID').first()
        validated_data['ProductID'] = last_product.ProductID + 1 if last_product else 1
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductName']


from inventory.models import ProductVariantCombination

class ProductVariantCombinationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductVariantCombination
        fields = ['id', 'combination_code', 'product']


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


from inventory.models import StockTransaction

class GetStockTransactionSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantCombinationSerializer()
    user = UserSerializer()

    class Meta:
        model = StockTransaction
        fields = ['date', 'product_variant', 'transaction_type', 'quantity', 'user']
