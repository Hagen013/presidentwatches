import requests


@app.task
def process_media_url(urls):

    product = CubesProductCard.objects.get(id=product_id)
    for url in urls:
        file_name = url.split('/')[-1]
        download_path = '{0}original/{1}'.format(settings.MEDIA_BUFFER_PATH, file_name)
            response = requests.get(url, stream=True)
            status_code = response.status_code
            if status_code == 200:
                with open(download_path, 'wb') as fp:
                    for chunk in response.iter_content(1024):
                        fp.write(chunk)
                product.add_photo(download_path)
                record = CubesImagesRegisterRecord(
                    product=product,
                    url=url,
                )
                record.save()
                succeded += 1
            else:
                failed += 1
    return {
        "succeded": succeded,
        "failed": failed
    }