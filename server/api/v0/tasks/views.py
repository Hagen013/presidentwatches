from django.core.files.storage import FileSystemStorage
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from celery.result import AsyncResult
from config.celery import app
from tasks.warehouse import process_warehouse_file


class UploadFile2TaskApiView(APIView):

    """
    Базовый класс для работы с файлами из
    прилолежния администратора. Получает файл,
    отправляет таск на выполнение, возвращает
    uuid для мониторинга статуса и получения отчета
    """

    permissions_class = permissions.IsAdminUser
    task              = None

    def get(self, request, *args, **kwargs):
        uuid = request.GET.get('uuid')
        task = AsyncResult(uuid, app=app)
        is_ready = task.ready()
        if is_ready:
            results = task.get()
        else:
            results = {}
        data = {
            'is_ready': is_ready,
            'results': results
        }
        return Response(data)


    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filepath = settings.ADMIN_UPLOADS + uploaded_file.name
        filename = fs.save(filepath, uploaded_file)
        result = self.task.delay(filename)
        data = {
            'uuid': result.id
        }
        return Response(data)


class UploadWarehouseApiView(UploadFile2TaskApiView):

    task = process_warehouse_file