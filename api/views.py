# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from core.models import Street, District, House
from .serializers import StreetSerializer, HouseSerializer, DistrictSerializer, StreetFormSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication,))
def district_view(request):
    if request.method == 'GET':
        district = District.objects.all()
        serializer_context = {'request': request}
        serializer = DistrictSerializer(district, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication,))
def street_view(request):
    if request.method == 'GET':
        district = request.GET.get('district', 1)
        street = Street.objects.all().filter(district=district)
        serializer_context = {'request': request}
        serializer = StreetSerializer(street, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication,))
def house_view(request):
    if request.method == 'GET':
        street = request.GET.get('street')
        house = House.objects.all().filter(street=street)
        serializer_context = {'request': request}
        serializer = HouseSerializer(house, context=serializer_context, many=True)
        return Response(serializer.data)