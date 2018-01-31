import logging

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError as GoogleHttpError
from httplib2 import ServerNotFoundError
from rest_framework import status
from rest_framework.exceptions import APIException
from address_collector.exceptions import FusionTablePermissionError
from address_collector.exceptions import FusionTableConnectonError

logger = logging.getLogger(__name__)


def fusion_service():
    '''
    Util method to get Google API connection and create service object
    '''
    credentials = service_account.Credentials.from_service_account_info(
        settings.GOOGLE_SERVICE_ACCOUNT, scopes=settings.GOOGLE_SCOPES)
    try:
        ft_service = discovery.build('fusiontables', 'v2', credentials=credentials)
    except ServerNotFoundError as e:
        logger.error(e)
        raise FusionTableConnectonError()
    query = ft_service.query()
    return query


def perform_query(sql_string):
    '''
    Util method to get perform actuall query
    sql_string: SQL query string
    '''
    logger.info("Fusion SQL:{}".format(sql_string))

    response = None
    request = fusion_service().sql(sql=sql_string)
    try:
        response = request.execute()
        logger.info("Fusion Query Executed:{0}. Response: {1}".format(sql_string, response))
    except GoogleHttpError as e:
        logger.error(e)
        if e.resp.status == status.HTTP_403_FORBIDDEN:
            raise FusionTablePermissionError()
        raise APIException(str(e))

    return response
