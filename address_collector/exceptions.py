from rest_framework.exceptions import APIException


class FusionTableConnectonError(APIException):
    status_code = 503
    default_detail = 'NBT is unable to create connection to the Fusion Table. Kindly make sure you are connected to the internet'
    default_code = 'service_unavailable'


class FusionTablePermissionError(APIException):
    status_code = 403
    default_detail = 'NBT does not have write permissions to the provided table. Please add your service email address to fusion table access list.'
    default_code = '403 Forbidden'
