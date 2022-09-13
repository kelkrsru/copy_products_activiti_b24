import json
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist

from core.bitrix24.bitrix24 import ActivityB24, EnumerationB24
from core.models import Portals
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pybitrix24 import Bitrix24

from activities.models import Activity
from settings.models import SettingsPortal


@csrf_exempt
def install(request):
    """View for install application in portal."""
    member_id = request.POST.get('member_id')
    activity_code = request.POST.get('code')

    portal = get_object_or_404(Portals, member_id=member_id)
    portal.check_auth()

    activity = get_object_or_404(Activity, code=activity_code)
    try:
        activity_b24 = ActivityB24(portal, obj_id=None)
        result = activity_b24.install(activity.build_params())
    except RuntimeError as ex:
        return JsonResponse({
            'result': 'False',
            'error_name': ex.args[0],
            'error_description': ex.args[1]})
    return JsonResponse({'result': result})


@csrf_exempt
def uninstall(request):
    """View for uninstall application in portal."""
    member_id = request.POST.get('member_id')
    activity_code = request.POST.get('code')

    portal = get_object_or_404(Portals, member_id=member_id)
    portal.check_auth()

    try:
        activity_b24 = ActivityB24(portal, obj_id=None, code=activity_code)
        result = activity_b24.uninstall()
    except RuntimeError as ex:
        return JsonResponse({
            'result': 'False',
            'error_name': ex.args[0],
            'error_description': ex.args[1]})
    return JsonResponse({'result': result})


@csrf_exempt
def copy_products(request):
    """View for activity copy products."""
    with open('/root/test.log', 'w', encoding='utf-8') as file:
        file.write(json.dumps(request.POST))
    initial_data: dict[str, any] = _get_initial_data(request)
    portal, settings_portal = _create_portal(initial_data)
    smart_element_id, deal_id = _check_initial_data(portal, initial_data)
    smart_process_code = initial_smart_process(portal, initial_data)
    _response_for_bp(
        portal,
        initial_data['event_token'],
        'Успех. Товары скопированы.',
        return_values={'result': f'Ok: {smart_process_code = }'},
    )
    return HttpResponse(status=HTTPStatus.OK)


def _create_portal(initial_data):
    """Method for create portal."""
    try:
        portal = Portals.objects.get(member_id=initial_data['member_id'])
        portal.check_auth()
        settings_portal = SettingsPortal.objects.get(portal=portal)
        return portal, settings_portal
    except ObjectDoesNotExist:
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)


def _get_initial_data(request):
    """Method for get initial data from Post request."""
    if request.method != 'POST':
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    return {
        'member_id': request.POST.get('auth[member_id]'),
        'event_token': request.POST.get('event_token'),
        'smart_element_id': request.POST.get(
            'properties[smart_element_id]') or 0,
        'deal_id': request.POST.get('properties[deal_id]') or 0,
        'document_type': request.POST.get('document_type[2]'),
    }


def _check_initial_data(portal, initial_data):
    """Method for check initial data."""
    try:
        smart_element_id = int(initial_data['smart_element_id'])
        deal_id = int(initial_data['deal_id'])
        return smart_element_id, deal_id
    except Exception as ex:
        _response_for_bp(
            portal,
            initial_data['event_token'],
            'Ошибка. Проверьте входные данные.',
            return_values={'result': f'Error: {ex.args[0]}'},
        )
        return HttpResponse(status=HTTPStatus.OK)


def initial_smart_process(portal, initial_data):
    """Method for initial smart process."""
    try:
        enum = EnumerationB24(portal)
        owner_types = enum.get_ownertype()
        return next(x['SYMBOL_CODE_SHORT'] for x in owner_types
                    if x['SYMBOL_CODE'] == initial_data['document_type'])
    except Exception as ex:
        _response_for_bp(
            portal,
            initial_data['event_token'],
            'Ошибка. Невозможно получить данные о смарт процессе.',
            return_values={'result': f'Error: {ex.args[0]}'},
        )
        return HttpResponse(status=HTTPStatus.OK)


# def create_obj_and_get_all_products(
#         portal: Portals, obj_id: int, initial_data: dict[str, any],
#         logger) -> (DealB24 or QuoteB24) or HttpResponse:
#     """Функция создания сделки или предложения и получения всех товаров."""
#     try:
#         if initial_data['document_type'] == 'DEAL':
#             obj = DealB24(portal, obj_id)
#         else:
#             obj = QuoteB24(portal, obj_id)
#         obj.get_all_products()
#         if obj.products:
#             return obj
#         logger.error(MESSAGES_FOR_LOG['products_in_deal_null'])
#         logger.info(MESSAGES_FOR_LOG['stop_app'])
#         response_for_bp(portal, initial_data['event_token'],
#                         MESSAGES_FOR_BP['products_in_deal_null'])
#         return HttpResponse(status=200)
#     except RuntimeError as ex:
#         logger.error(MESSAGES_FOR_LOG['impossible_get_products'])
#         logger.info(MESSAGES_FOR_LOG['stop_app'])
#         response_for_bp(portal, initial_data['event_token'],
#                         MESSAGES_FOR_BP['impossible_get_products'] + ex.args[
#                             0])
#         return HttpResponse(status=200)


def _response_for_bp(portal, event_token, log_message, return_values=None):
    """Method for send parameters in bp."""
    bx24 = Bitrix24(portal.name)
    bx24._access_token = portal.auth_id
    method_rest = 'bizproc.event.send'
    params = {
        'event_token': event_token,
        'log_message': log_message,
        'return_values': return_values,
    }
    bx24.call(method_rest, params)
