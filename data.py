import logging
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DB
db_file = os.path.join(BASE_DIR, "products.db")
db_table_structure = [ "name", "price", "id", "pk", "timestamp"]
update_time_threshold = -6  # How many hours between updates

# HTTP Requests
host = 'www.xxl.fi'
url_paths = {
    # Trekking equipment
    "tents": "/retkeily-metsastys/telttailu/c/200200",
    "fishing": "/retkeily-metsastys/kalastus/c/220000",
    "camping_equipment": "/retkeily-metsastys/retkeilyvalineet/c/200600",
    "sleeping_gear": "/retkeily-metsastys/makuupussit-ja-makuualustat/c/201000",
    "drinking_bags": "/urheilu-ja-pallopelit/reput-ja-kassit/juomareput/c/100606",
    # Clothes
    "trekking_shoes": "/retkeily-metsastys/vaelluskengat-ja-metsastyskengat/c/200800"
}


# Logging
log_level = logging.INFO
log_file = os.path.join(BASE_DIR, 'sniffer.log')
log_file_mode = "w"
db_logger_name = 'DBManager'
http_logger_name = 'HttpClient'