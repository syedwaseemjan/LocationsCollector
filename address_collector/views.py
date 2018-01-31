import copy
import logging

from django.conf import settings
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from address_collector.models import Address
from address_collector.serializers import AddressSerializer
from address_collector.utils import perform_query


logger = logging.getLogger(__name__)


def index(request):
    context = {'GOOGLE_MAPS_KEY': settings.GOOGLE_MAPS_KEY}
    return render(request, 'address_collector/index.html', context)


@api_view(['GET', 'POST', 'DELETE'])
def addresses(request):
    """
    List all addresses, create a new address or delete all addresses.
    """
    if request.method == 'GET':
        records = Address.objects.all()
        serializers = AddressSerializer(records, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            row = copy.copy(serializer.data)
            row["tableid"] = settings.GOOGLE_FUSION_TABLE_ID
            sql_string = "INSERT INTO {0} (DatabaseID, Address, Latitude, Longitude, CreatedOn, UpdatedOn) VALUES({1}, '{2}', {3}, {4}, '{5}', '{6}')".format(
                row["tableid"], row["id"], row["address"], row["longitude"], row["latitude"],
                row["created_on"], row["updated_on"])

            perform_query(sql_string)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ids = Address.objects.all().values_list('id', flat=True)
        ids_str = '(%s)' % ', '.join(map(repr, ids))
        sql_string = "DELETE FROM {0} WHERE DatabaseID in {1}".format(
            settings.GOOGLE_FUSION_TABLE_ID, ids_str)
        rows = perform_query(sql_string)["rows"]
        logger.info("Total Addresses: {0}. Deleted From FusionTable: {1}".format(len(list(ids)), rows[0]))
        Address.objects.all().delete()
        return Response([], status=status.HTTP_205_RESET_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
