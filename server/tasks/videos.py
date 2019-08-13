import requests
from bs4 import BeautifulSoup

from django.core.exceptions import ObjectDoesNotExist

from shop.models import ProductPage as Product
from shop.utils import get_rows_from_file
from shop.models import ProductVideo as Video

FILENAME = 'videos.txt'


def parse_videos():
    rows = get_rows_from_file('./data/pw_pages_181204.json')['products']

    for row in rows:
        slug = row.get('slug', None)
        model = row['fields'].get('model', None)
        #print(slug)
        
        with open(FILENAME, 'w') as fp:
            if model is not None and slug is not None:
                try:
                    instance = Product.objects.get(
                        model=model
                    )
                    
                    url = 'http://presidentwatches.ru/watches/' + slug
                    response = requests.get(url)
                    content = response.content
                    status_code = response.status_code

                    if status_code == 200:
                        output = '[SUCCESS]'
                    else:
                        output = '[ERROR]'
                    output = '{url} {status}'.format(
                        url=url,
                        status=output
                    )

                    fp.write(output+'\n')
                    print(output)
                    
                    try:
                        soup = BeautifulSoup(content, 'html.parser')
                        element = soup.findAll("div", {"class": "product-tabs__content"})[0]
                        videos = element.findAll("iframe")
                    except:
                        videos = None
                        
                    if videos is not None:
                        for video in videos:
                            video_slug = video.attrs['src'].split('?')[0].split('/')[-1]
                            try:
                                video = Video.objects.get(
                                    product=instance,
                                    slug=video_slug
                                )
                            except ObjectDoesNotExist:
                                video = Video(
                                    product=instance,
                                    slug=video_slug
                                )
                                try:
                                    video.full_clean()
                                    video.save()
                                except:
                                    pass
                    
                except ObjectDoesNotExist:
                    pass