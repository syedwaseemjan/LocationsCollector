from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from address_collector.models import Address
from address_collector.serializers import AddressSerializer

import copy
import requests


def index(request):
    latest_address_list = Address.objects.order_by('-created_on')[:5]
    context = {'latest_address_list': latest_address_list,
               'GOOGLE_MAPS_KEY': settings.GOOGLE_MAPS_KEY}
    return render(request, 'address_collector/index.html', context)


@api_view(['GET', 'POST'])
def addresses(request):
    """
    List all addresses or create a new address
    """
    if request.method == 'GET':
        records = Address.objects.all()
        serializers = AddressSerializer(records, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            from google.oauth2 import service_account
            import googleapiclient.discovery

            credentials = service_account.Credentials.from_service_account_info(
                settings.GOOGLE_SERVICE_ACCOUNT, scopes=settings.GOOGLE_SCOPES)

            ft_service = googleapiclient.discovery.build(
                'fusiontables', 'v2', credentials=credentials)
            query = ft_service.query()

            row = copy.copy(serializer.data)
            row["tableid"] = settings.GOOGLE_FUSION_TABLE_ID
            sql_string = "INSERT INTO {0} (ID, Address, Latitude, Longitude, CreatedOn, UpdatedOn) VALUES({1}, '{2}', {3}, {4}, '{5}', '{6}')".format(
                row["tableid"], row["id"], row["address"], row["longitude"], row["latitude"], row["created_on"], row["updated_on"])
            print(sql_string)
            request = query.sql(sql=sql_string)
            try:
                response = request.execute()
            except Exception as e:
                Response(status=response.status_code)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_404_NOT_FOUND)
