import os
import tempfile
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def ler_qr_code(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, 'rb') as img:
                files = {'imagem': img}
                response = requests.post('http://212.85.19.120:8001/api/ler-qrcode/', files=files)
                response.raise_for_status()  # se falhar, sobe exceção
                return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            os.remove(temp_file_path)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def ler_gabarito(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, 'rb') as img:
                files = {'imagem': img}
                response = requests.post('http://212.85.19.120:8002/api/leitor/', files=files)
                response.raise_for_status()  # força erro se status não for 2xx
                return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            os.remove(temp_file_path)

    return JsonResponse({'error': 'Invalid request'}, status=400)
