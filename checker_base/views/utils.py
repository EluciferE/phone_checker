from rest_framework import serializers
from rest_framework.response import Response


def api_error_response(data: dict, key: str = 'data') -> Response:
    response = {
        'status': 'error',
        key: data,
    }

    return Response(response)


def api_ok_response(data: dict, key: str = 'data') -> Response:
    response = {
        'status': 'OK',
        key: data,
    }

    return Response(response)


def assert_valid_serializer(request, cls: type[serializers.Serializer]) -> dict:
    if request.method == 'GET':
        data = request.query_params
    elif request.method == 'POST':
        data = request.data
    else:
        raise ValueError(request.method)

    serializer = cls(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
