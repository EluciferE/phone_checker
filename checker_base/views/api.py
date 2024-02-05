import logging

from rest_framework import serializers
from rest_framework.decorators import api_view

from checker_base.models import PhoneGroup
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
    logger = logging.getLogger('get_phone_info')
    try:
        data = assert_valid_serializer(request, PhoneInfoRequestSerializer)
        logger.info(f'Received a phone request: {data}')
    except serializers.ValidationError as error:
        logger.info(f'Error while handling phone. {request.query_params = }, {error.detail}')
        return api_error_response(error.detail)

    phone = data['phone']
    prefix = int(phone[1:4])
    number = int(phone[4:])

    phone_group = PhoneGroup.objects.filter(
        prefix=prefix,
        start_range__lte=number,
        end_range__gte=number,
    ).select_related('region', 'operator').first()

    if phone_group is None:
        return api_error_response({'phone': ['Номер не найден в базе данных']})

    return api_ok_response({
        'phone': phone,
        'operator': phone_group.operator.name,
        'region': phone_group.region.name,
    })
