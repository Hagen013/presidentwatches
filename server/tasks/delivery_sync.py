from datetime import datetime, timedelta

from django.conf import settings
from django.db import transaction
from django.utils.timezone import now, pytz

from config.celery import app
from celery.schedules import crontab

from cart.models import Order
from delivery.cdek import Client as ClientSDEK
from delivery.pickpoint import Client as ClientPickpoint
from delivery.rupost import Client as ClientRupost
from cart.serializers import OrderSerializer
from cart.utils import (pickpoint_to_cdek_code,
                        rupost_to_cdek_code,
                        rupost_msg_to_code)


@app.task
def sync_sdek_orders(pks):
    qs = Order.objects.filter(public_id__in=pks)
    pks = [order.public_id for order in qs]

    errors = []
    invalid = []

    qs = Order.objects.filter(public_id__in=pks)
    client = ClientSDEK(settings.SDEK_USER, settings.SDEK_PASSWORD)
    serializer = OrderSerializer(qs, many=True)
    results_tracking = client.get_orders_statuses(serializer.data)['Order']
    results_info = client.get_orders_information(serializer.data)['Order']

    mapping = {}
    for result in results_info:
        mapping[result['DispatchNumber']] = result

    for order in results_tracking:
        error_code = order.get('ErrorCode', None)
        if error_code is not None:
            pass
        else:
            dispatch_number = order['DispatchNumber']
            order_id = order['Number']
            status_description = order['Status']['Description']
            cdek_status_code = int(order['Status']['Code'])
            status_date = order['Status']['Date']

            instance = Order.objects.get(public_id=order_id)

            instance.tracking['service'] = 'sdek'
            instance.tracking['change_date'] = status_date
            instance.tracking['state_description'] = status_description
            instance.tracking['service_status_code'] = cdek_status_code
            instance.tracking['dispatch_number'] = dispatch_number
            instance.tracking['history'] = []

            information_result = mapping.get(dispatch_number, None)
            if information_result is not None:
                invoice_price = information_result.get('CashOnDelivFact', None)
            else:
                invoice_price = None

            if invoice_price is not None:
                instance.tracking['sum'] = invoice_price

            for snapshot in order['Status']['State']:
                item = {
                    "change_date": snapshot['Date'],
                    "state_description": snapshot['Description'],
                    "service_status_code": snapshot['Code'],
                    "city_code": snapshot['CityCode']
                }
                instance.tracking['history'].append(item)
            if cdek_status_code == 4:
                instance.state = OrderState.HandedOver
            elif cdek_status_code == 5:
                instance.state = OrderState.Rejected
            instance.save()
    
    return errors


@app.task
def sync_pickpoint_orders(pks):
    
    qs = Order.objects.filter(public_id__in=pks)
    pks = [order.public_id for order in qs]
    client = ClientPickpoint(settings.PICKPOINT_USER, settings.PICKPOINT_PASSWORD)
    client.login()
    response = client.track_sendings(pks)
    data = response.json()
    invoices = data['Invoices']

    success = []
    count = 0

    with transaction.atomic():
        for invoice in invoices:
            public_id = invoice['SenderInvoiceNumber']
            invoice_number = invoice['InvoiceNumber']
            invoice_sum = float(invoice['RefundInfo']['Sum'])
            states = invoice['States']
            last_status = states[-1]
            change_date = last_status['ChangeDT']
            state_message = last_status['StateMessage']
            status_code = int(last_status['State'])
            item = {
                "service": "pickpoint",
                "change_date": change_date,
                "dispatch_number": invoice_number,
                "state_description": state_message,
                "service_status_code": status_code,
                "status_code": pickpoint_to_cdek_code(str(status_code)),
                "sum": invoice_sum,
                "history": []
            }
            for state in states:
                history_state = {
                    "change_date": state['ChangeDT'],
                    "state_description": state['StateMessage'],
                    "service_status_code": state['State'],
                }
                item['history'].append(history_state)
            instance = Order.objects.get(public_id=public_id)
            instance.tracking = item
            if instance.tracking['service_status_code'] == 111:
                instance.state = OrderState.HandedOver
            elif instance.tracking['status_code'] == 5:
                instance.state = OrderState.Rejected
            instance.save()
            success.append(public_id)
            count += 1
            
    return {
        'count': count,
        'success': success
    }


def sync_postal_orders(pks):
    qs = Order.objects.filter(public_id__in=pks)
    client = ClientRupost(settings.RUPOST_USER, settings.RUPOST_PASSWORD)
    
    
    for instance in qs:
        
        dispatch_number = str(instance.tracking['dispatch_number'])
        if len(dispatch_number) > 0:
            tracking_history = client.get_operation_history(dispatch_number)

            finance_parameters_list = list(map(lambda x: x['FinanceParameters'], tracking_history))
            finance_parameters_list = list(filter(lambda x: x['Payment'] is not None, finance_parameters_list))
            invoice_sum = finance_parameters_list[0]['Payment']
            if int(invoice_sum) != 0:
                invoice_sum = float(str(invoice_sum)[:-2])

            last_state = tracking_history[-1]
            operation_parameters = last_state['OperationParameters']
            oper_type = operation_parameters['OperType']
            oper_attribute = operation_parameters['OperAttr']
            oper_date = str(operation_parameters['OperDate'])
            state_description = "{0} ({1})".format(
                oper_type['Name'],
                oper_attribute['Name']
            )
            instance.tracking['state_description'] = state_description
            code = rupost_msg_to_code(oper_attribute['Name'])
            instance.tracking['service_status_code'] = code
            instance.tracking['status_code'] = rupost_to_cdek_code(str(code))
            instance.tracking['change_date'] = oper_date
            instance.tracking['sum'] = invoice_sum

            history = []
            for item in tracking_history:
                history_state_description = "{0} ({1})".format(
                    item['OperationParameters']['OperType']['Name'],
                    item['OperationParameters']['OperAttr']['Name']
                )
                history_log_item = {
                    "state_description": history_state_description,
                    "change_date": str(item['OperationParameters']['OperDate']),
                    "service_status_code": item['OperationParameters']['OperType']['Id']
                }
                history.append(history_log_item)
            instance.delivery_status['history'] = history

            if instance.delivery_status['status_code'] == 4:
                instance.state = 'вручен'
            elif instance.delivery_status['status_code'] == 5:
                instance.state = 'отказ'

            instance.save()