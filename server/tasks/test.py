import requests

from shop.models import ProductPage as Product
from shop.models import CategoryPage as Node

ERRORS_FILE = 'ERRORS.txt'

def test_pages():
    # for node in Node.objects.all():
    #     url = 'https://presidentwatches.ru/shop/watches/{slug}'.format(
    #         slug=node.slug
    #     )
    #     response = requests.get(url)
    #     msg = "{url} {code}".format(
    #         url=url,
    #         code=response.status_code
    #     )
    #     print(msg)
    #     if response.status_code == 200:
    #         pass
    #     else:
    #         with open(ERRORS_FILE, 'w+') as fp:
    #             fp.write(msg)
    #     for i in range(1, 9999):
    #         page_url = url + '?page={i}'.format(i=i)
    #         response = requests.get(page_url)
    #         msg = "{url} {code}".format(
    #             url=page_url,
    #             code=response.status_code
    #         )
    #         print(msg)
    #         if response.status_code == 200:
    #             pass
    #         elif response.status_code == 404:
    #             break
    #         else:
    #             with open(ERRORS_FILE, 'w+') as fp:
    #                 fp.write(msg)

    for instance in Product.objects.all():
        url = 'https://presidentwatches.ru/watches/{slug}/'.format(
            slug=instance.slug
        )
        response = requests.get(url)
        msg = "{url} {code}\n".format(
            url=url,
            code=response.status_code
        )
        print(msg)
        if response.status_code == 200:
            pass
        else:
            with open(ERRORS_FILE, 'w+') as fp:
                fp.write(msg)