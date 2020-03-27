from rest_framework import serializers
from .models import User, HospitalProfile, VendorProfile

class HospitalProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = HospitalProfile
        fields = ('id', 'name', 'gstin', 'address')

class VendorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        fields = ('id', 'name','gstin', 'address')

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
        vendor_profile = VendorProfile.objects.update_or_create(user=user, defaults=validated_data)
        return vendor_profile

class CreateUserSerializer(serializers.ModelSerializer):

    hospital_profile = HospitalProfileSerializer(read_only=True)
    vendor_profile = VendorProfileSerializer(read_only=True)

    class Meta:

        model = User
        fields = ('id', 'username', 'password', 'email','phone_number', 'hospital_profile', 'vendor_profile')
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
