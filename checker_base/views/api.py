from rest_framework import serializers
from rest_framework.decorators import api_view

from checker_base.views.utils import api_error_response, api_ok_response, assert_valid_serializer


class PhoneInfoRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        if not data['phone'].isdigit():
            raise serializers.ValidationError({'phone': 'Некорректный номер телефона'})
        if not len(data['phone']) == 11:
            raise serializers.ValidationError({'phone': 'Некорректная длинна номера'})

        return data


class PhoneInfoResponseSerializer(serializers.Serializer):
    phone = serializers.CharField()
    operator = serializers.CharField()
    region = serializers.CharField()


@api_view(['GET'])
def get_phone_info(request):
    try:
        data = assert_valid_serializer(request, PhoneInfoRequestSerializer)
    except serializers.ValidationError as error:
        return api_error_response(error.detail)

    return api_ok_response({
        'phone': data['phone'],
        'operator': 'МТС',
        'region': 'Тюмень',
    })
