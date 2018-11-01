import sys
import time
import threading
import urllib3

class LoadHtml(object):

    def __init__(self, urls):
        self.urls = urls
        self.threads = []
        urllib3.disable_warnings()

    def download(self, url):
        http = urllib3.PoolManager()
        print(f"start download {url}")
        try:
            r = http.request('GET', f"http://{url}/")
        except (urllib3.exceptions.HTTPError, urllib3.exceptions.TimeoutError, urllib3.exceptions.ConnectTimeoutError):
            print(f"Error in download {url}")
        else:
            print(f"Downloading {url} completed. Start writing....")
            with open(f"resources/{url}.html", 'wb') as f:
                f.write(r.data)

    def http_get(self):
        for url in urls:
            self.download(url)


if __name__ == "__main__":
   #urls = sys.argv[1:]
    urls = ['python.org', 'google.com', '2v1k.com', 'vk.com', 'fa.ru']
    load_html = LoadHtml(urls)
    thr = threading.Thread(target=load_html.http_get)
    thr.start()
