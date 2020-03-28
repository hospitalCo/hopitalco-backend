from rest_framework import serializers
from .models import User, HospitalProfile, VendorProfile, Item, Requirement, Stock, Category


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name',)

    def create(self, validated_data):

        category, created = Category.objects.get_or_create(**validated_data)

        return category, created


class ItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = Item
        fields = ('name', 'category',)
    
    def create(self, validated_data):

        category = validated_data.pop('category', None)
        if category is not None:

            category_serializer = CategorySerializer(data=category)
            category_serializer.is_valid()
            category_instance, created = category_serializer.save()

        item, created = Item.objects.get_or_create(category=category_instance,**validated_data)

        return item, created


class CreateStockSerializer(serializers.ModelSerializer):
    
    item = ItemSerializer()

    class Meta:
        model = Stock
        fields = ('units', 'item',)
        # depth = 1

    def create(self, validated_data):

        item = validated_data.pop('item')

        item_serializer = ItemSerializer(data=item)
        item_serializer.is_valid()
        item_instance, created = item_serializer.save()

        stock, created = Stock.objects.get_or_create(item=item_instance, vendor=self.context.get('user').vendor_profile, **validated_data)

        return stock


class VendorProfileSerializer(serializers.ModelSerializer):

    stock = CreateStockSerializer(read_only=True, many=True)

    class Meta:
        model = VendorProfile
        fields = ('id', 'name','gstin', 'address', 'stock')


class StockSerializer(serializers.ModelSerializer):

    vendor = serializers.StringRelatedField()
    item = ItemSerializer()

    class Meta:
        model = Stock
        fields = ('units', 'item', 'vendor')


class RequirementSerializer(serializers.ModelSerializer):

    hospital = serializers.StringRelatedField()
    item = ItemSerializer()

    class Meta:
        model = Stock
        fields = ('units', 'item', 'hospital')


class CreateRequirementSerializer(serializers.ModelSerializer):
    
    item = ItemSerializer()

    class Meta:
        model = Requirement
        fields = ('units', 'item',)

    def create(self, validated_data):

        item = validated_data.pop('item')

        item_serializer = ItemSerializer(data=item)
        item_serializer.is_valid()
        item_instance, created = item_serializer.save()

        requirement, created = Requirement.objects.get_or_create(item=item_instance, hospital=self.context.get('user').hospital_profile, **validated_data)

        return requirement


class HospitalProfileSerializer(serializers.ModelSerializer):

    requirement = CreateRequirementSerializer(read_only=True, many=True)
    class Meta:
        model = HospitalProfile
        fields = ('id', 'name', 'gstin', 'address', 'requirement')


class UserSerializer(serializers.ModelSerializer):

    hospital_profile = HospitalProfileSerializer()
    vendor_profile = VendorProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'hospital_profile', 'vendor_profile')


class CreateHospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = HospitalProfile
        fields = ['name','gstin', 'address']

    def create(self, validated_data):

        user = self.context.get('user')
        hospital_profile, created = HospitalProfile.objects.update_or_create(user=user,defaults=validated_data)
        return hospital_profile


class CreateVendorSerializer(serializers.ModelSerializer):

    class Meta:

        model = VendorProfile
        fields = ['name', 'gstin', 'address']

    def create(self, validated_data):
        
        user = self.context.get('user')
        vendor_profile, created = VendorProfile.objects.update_or_create(user=user, defaults=validated_data)
        return vendor_profile


class CreateUserSerializer(serializers.ModelSerializer):

    hospital_profile = HospitalProfileSerializer(read_only=True)
    vendor_profile = CreateVendorSerializer(read_only=True)

    class Meta:

        model = User
        fields = ('id', 'username', 'password', 'email','phone_number', 'first_name', \
            'last_name', 'hospital_profile', 'vendor_profile')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'hospital_profile' : {'read_only' : True}
        }

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)

        profiles = self.initial_data.pop('profiles', None)
        if profiles is not None:
            for profile in profiles:
                if profile.pop('type') == 'hospital':
                    serializer = CreateHospitalSerializer(data=profile, context={'user': user})
                else:
                    serializer = CreateVendorSerializer(data=profile, context={'user': user})

                if not serializer.is_valid():
                    raise Exception(serializer.errors)

                serializer.save()

        return user

