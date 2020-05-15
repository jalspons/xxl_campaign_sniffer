from hyper import HTTPConnection
from bs4 import BeautifulSoup as BS
import json
import re

host = 'www.xxl.fi'
p = '/retkeily-metsastys/vaelluskengat-ja-metsastyskengat/c/200800'
p2 = '/retkeily-metsastys/telttailu/c/200200'

example1 = 'example.html'

def fetch_html_file(path):
   conn = HTTPConnection(host + ':443')
   conn.request('GET', path)
   resp = conn.get_response()
   return resp.read().decode('utf-8')

def fetch_new_resource(path, file):
   with open(file, "w") as f:
      f.write(fetch_html_file(path))

def parse_html(html):
   doc = BS(html, 'html.parser')
   # Stringify the js script
   products_script = doc.head.find_all('script')[2].string
   # Isolate json from javascript
   products_string = '{' + ''.join(products_script.split('\n')[3:-2]).strip(';') + '}'
   # Remove whitespace and change ' to " in string
   pretty_products_string = (re.sub('[\s+]', '', products_string)).replace("'", '"')
   
   products_json = json.loads(pretty_products_string)['ecommerce']['impressions']
   print(len(products_json))

   for product in products_json:
      print(product)


html_file = fetch_html_file(p2)
parse_html(html_file)
