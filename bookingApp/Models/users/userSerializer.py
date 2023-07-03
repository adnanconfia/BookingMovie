from rest_framework import serializers
from .user import User

class UserSerializer(serializers.Serializer):
    Id = serializers.IntegerField()
    FirstName = serializers.CharField()
    LastName = serializers.CharField()
    CI = serializers.CharField()
    PhoneNumber = serializers.CharField()
    DOB = serializers.CharField()
    RoleType = serializers.IntegerField()
    UserName = serializers.CharField()
    Gender = serializers.CharField()
    RoleName = serializers.CharField()
    Email = serializers.EmailField()
    IsActive = serializers.BooleanField()
    IsDeleted = serializers.BooleanField()
    Creation_Time = serializers.DateTimeField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}