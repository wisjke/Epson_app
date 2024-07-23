from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Upload
from .tools import SaleReader, MerchReader
from collections import Counter


def slicer(elem):
    return int(elem.split(' ')[1])


def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            return redirect('process_files', pk=upload.pk)
        else:
            print(form.errors)
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})


def process_files(request, pk):
    upload = Upload.objects.get(pk=pk)
    salers_path = upload.salers_file.path
    merch_path = upload.merch_file.path

    salers_dk = {}
    err_dk = {}
    error_message = ""

    try:
        saleReader = SaleReader(salers_path)
        salers_dk = saleReader.read()
    except Exception as e:
        error_message += f"Error reading 'salers.csv': {e}\n"

    try:
        merchReader = MerchReader(merch_path)
        err_dk = merchReader.read()
    except Exception as e:
        error_message += f"Error reading 'Merch.xlsx': {e}\n"

    results = []
    for err in err_dk:
        tasks_list = []
        for num in err_dk[err]:
            if num in salers_dk:
                tasks_list.extend(map(slicer, salers_dk[num]))
        tasks_list.sort()
        counts = Counter(tasks_list)
        results.append({'error': err, 'counts': dict(counts)})

    upload.salers_file.delete()
    upload.merch_file.delete()
    upload.delete()

    return render(request, 'results.html', {'results': results, 'error_message': error_message})
