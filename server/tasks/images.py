import os
import sys
import logging

import requests

from shop.utils import get_rows_from_file

MEDIA_PATH = '/1TB/presidentwatches-original'
SRC_URL = 'http://presidentwatches.ru'


class FileDownloader():
    
    src_filename = ''
    urls_total_count = 0
    urls_filtered_count = 0
    current_count = 0
    invalid_count = 0
    
    rows = []
    _urls = []
    existing_files = []
    files_to_download = []
    invalid_urls = []
    
    def __init__(self, filename, target, media_path):
        self.src_filename = filename
        self.target = target
        self.media_path = media_path
    
    def get_rows_from_file(self, filename):
        data = get_rows_from_file(filename)
        return data['products']
    
    def extract_urls(self, rows):
        urls = []
        for row in rows:
            fields = row.get('fields')
            pictures = row.get('pictures')
            manual = fields.get('manual', None)
            pictures = row.get('pictures', None)
            if manual is not None:
                urls.append(manual)
            if pictures is not None:
                for picture in pictures:
                    url = picture.get('url', None)
                    if url is not None:
                        urls.append(url)
        return urls
    
    def file_doesnt_exist(self, url):
        filepath = self.media_path + url
        return not os.path.isfile(filepath)
    
    def _filter_urls(self, urls):
        return [url for url in urls if self.file_doesnt_exist(url)]
    
    def get_file(self, url):
        absolute_url = self.target + url
        response = requests.get(absolute_url, stream=True)
        status_code = response.status_code
        if status_code == 200:
            self.save_file(response, url)
        else:
            pass
        return status_code
    
    def save_file(self, response, url):
        path = self.media_path + url
        dirname = '/'.join(path.split('/')[:-1])
        if not os.path.exists(dirname):
            new_path = ''
            slugs = dirname.split('/')
            for slug in slugs:
                new_path = new_path + '/' + slug
                if not os.path.exists(new_path):
                    os.mkdir(new_path)

        with open(path, 'wb') as fp:
            for chunk in response.iter_content(1024):
                fp.write(chunk)
    
    def process_urls(self, urls):
        for url in urls:
            status_code = self.get_file(url)
            if status_code == 200:
                self.current_count += 1
            else:
                self.invalid_urls.append(url)
                self.invalid_count += 1
                with open("INVALID", "a") as fp:
                    line = url + '\n'
                    fp.write(line)

            msg = '[*] DOWNLOADING: {count}/{total} INVALID: {invalid}'.format(
                count=self.current_count,
                total=self.urls_total_count,
                invalid=self.invalid_count
            )
            sys.stdout.write("\r {:<70}".format(msg))
            sys.stdout.flush()
    
    def run(self):
        self.rows = self.get_rows_from_file(self.src_filename)
        self._urls = self.extract_urls(self.rows)
        self.urls_total_count = len(self._urls)
        self.urls = self._filter_urls(self._urls)
        self.urls_filtered_count = len(self.urls)
        self.current_count = self.urls_total_count - self.urls_filtered_count
        self.process_urls(urls=self.urls)



def main():
    filename = 'data/pw_pages_190803.json'
    downloader = FileDownloader(
        filename=filename,
        target=SRC_URL,
        media_path=MEDIA_PATH
    )
    downloader.run()
