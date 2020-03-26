from rest_framework import serializers
from .models import User, HospitalProfile, VendorProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','name','is_hospital','phoneNumber','address','auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}


class CreateHospitalSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()
    class Meta:
        model = HospitalProfile
        fields = ['user','hospitalId']
    def create(self, validated_data):
        userdata = validated_data.pop('user')
        userInstance = User.objects.create_user(**userdata)
        hospitalProfile = HospitalProfile.objects.create(user=userInstance,**validated_data)
        return hospitalProfile

class CreateVendorSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()
    class Meta:
        model = VendorProfile
        fields = ['user','gstin']
    def create(self, validated_data):
        userdata = validated_data.pop('user')
        userInstance = User.objects.create_user(**userdata)
        vendorProfile = VendorProfile.objects.create(user=userInstance,**validated_data)
        return vendorProfile


