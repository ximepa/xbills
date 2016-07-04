from core.models import Street, House, District
from rest_framework import serializers


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = Street
        fields = ('id', 'name',)


class StreetSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()

    class Meta:
        model = Street
        fields = ('id', 'name', 'district')


# class StreetFormSerializer(serializers.ModelSerializer):
#     district = serializers.StringRelatedField()
#
#     class Meta:
#         model = StreetInfo
#         fields = ('id', 'district', 'street', )


class HouseSerializer(serializers.ModelSerializer):
    street = serializers.StringRelatedField()

    class Meta:
        model = House
        fields = ('id', 'number', 'street')


class HouseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'number')


class StreetFormSerializer(serializers.ModelSerializer):
    houses = HouseFormSerializer(many=True)

    class Meta:
        model = Street
        fields = ('id', 'name', 'district', 'houses')


# class EntranceSerializer(serializers.ModelSerializer):
#     street = serializers.StringRelatedField()
#
#     class Meta:
#         model = Entrance
#         fields = ('id', 'street', 'entrance_number', 'code', 'roof', 'first_flat', 'last_flat', 'key_roof', 'technical_floor', 'tubes', 'box', 'box_location', 'switch', 'uplink', 'box_power')
#
#
# class StreetInfoSerializer(serializers.ModelSerializer):
#
#
#     class Meta:
#         model = StreetInfo
#         fields = ('id', 'district', 'street', 'build', 'roof_type')

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('entrance')
    #     print profile_data
    #     street_info = StreetInfo.objects.create(**validated_data)
    #     Entrance.objects.create(street=street_info, **profile_data)
    #     return street_info