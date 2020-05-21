from httpclient import HttpClient
from db import DBManager
from data import *

import logging 


def init_logging():
    # TODO logging format
    FORMAT = '[%(levelname)s][%(name)-15s] %(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT,filename=log_file,level=log_level)

def update():
    # Start logging
    init_logging()
    # Create dbmanager and httpclient
    db_client = DBManager(db_file, db_logger_name)
    http_client = HttpClient(host, url_paths, http_logger_name)
    
    # Create db if not existing
    if db_client.is_empty():
        db_client.create_db()

    #print(db_client.fetch_products_from_db())
    
    for product_group, url_path in url_paths.items():
        html_file = http_client.fetch_html_file(host, url_path)
        json_file = http_client.parse_html_file(html_file)
        
        db_client.add_products(product_group, json_file)


if __name__ == "__main__":
    update()

