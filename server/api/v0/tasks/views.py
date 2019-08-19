import os
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from celery.result import AsyncResult
from config.celery import app
from tasks.warehouse import (
    process_warehouse_file,
    generate_warehouse_file
)


class StatusReportMixin():

    permissions_class = permissions.IsAdminUser

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


class UploadFile2TaskApiView(APIView, StatusReportMixin):

    """
    Базовый класс для работы с файлами из
    прилолежния администратора. Получает файл,
    отправляет таск на выполнение, возвращает
    uuid для мониторинга статуса и получения отчета
    """

    permissions_class = permissions.IsAdminUser
    task              = None

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


class Task2DonwloadFileApiView(APIView, StatusReportMixin):

    """
    Базовый класс для запуска задачи
    по формированию файла. Получает сигнал
    о начале формирования по POST-запросу,
    отдает отчет о состоянии task'a по GET
    """
    permissions_class = permissions.IsAdminUser

    def get_filename(self):
        raise NotImplementedError('Method must be implemented by a subclass')

    def post(self, request, *args, **kwargs):
        fs = FileSystemStorage
        fs = FileSystemStorage()
        filename = self.get_filename()
        filepath = settings.ADMIN_DOWNLOADS + filename
        result = self.task.delay(filepath)
        data = {
            'uuid': result.id,
            'filename':  filename
        }
        return Response(data)


class UploadWarehouseApiView(UploadFile2TaskApiView):

    task = process_warehouse_file
    permissions_class = permissions.IsAdminUser


class DonwloadWarehouseApiView(Task2DonwloadFileApiView):

    task = generate_warehouse_file

    def get_filename(self):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = 'ostatki-{time}.xlsx'.format(
            time=time
        )
        return filename


class DownloadFileApiView(APIView):

    permissions_class = permissions.IsAdminUser

    def get(self, request, *args, **kwargs):
        filename = request.GET.get('filename', None)
        if filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            filepath = settings.ADMIN_DOWNLOADS + filename
            if os.path.exists(filepath):
                with open(filepath, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                    return response
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)


class UserChangeEmailApiView(APIView):

    def post(self, request, *args, **kwargs):
        return Response({})


class UserChangePhoneApiView(APIView):

    def post(self, request, *args, **kwargs):
        return Response({})
