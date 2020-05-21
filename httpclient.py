from hyper import HTTPConnection
from bs4 import BeautifulSoup as BS
import requests
import json
import re
import logging

class HttpClient():
   def __init__(self, host, paths, logger_name):
      self.host = host
      self.paths = paths
      self.logger = logging.getLogger(logger_name)

   def fetch_paths(self, file):
      self.logger.info('Fetching url paths')
      with open(file, "r") as f:
         s = f.read()
      return json.loads(s)

   def fetch_html_file(self, host, path):
      self.logger.info('Fetching html file')
      conn = HTTPConnection(host + ':443')
      conn.request('GET', path)
      resp = conn.get_response()
      return resp.read().decode('utf-8')

   def fetch_and_store_html_file(self, host, path, file):
      with open(file, "w") as f:
         f.write(self.fetch_html_file(host, path))

   def parse_html_file(self, html):
      self.logger.info('Parsing html file')
      doc = BS(html, 'html.parser')
      # Stringify the <script> containing products json
      products_script = doc.head.find_all('script')[2].string
      # Isolate json from js code (json is pushed on array in js code)
      products_string = '{' + ''.join(products_script.split('\n')[3:-2]).strip(';') + '}'
      # Remove whitespace and change ' to " in string
      pretty_products_string = (re.sub('[\s+]', '', products_string)).replace("'", '"')
      # Transform json to python dict and browse to products
      products = json.loads(pretty_products_string)['ecommerce']['impressions']
      self.logger.debug(products)

      return products

 


#client = HttpClient(host, paths)
#html_file = client.fetch_html_file(p2)
#json_file = client.parse_html_file(html_file)
#client.parse_products_json_to_db_format(json_file, "Tents")
#uri = 'https://' + host
#print(uri)
#r = requests.get(uri)
#print(r.status_code)