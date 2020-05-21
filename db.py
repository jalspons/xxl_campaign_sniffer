import sqlite3
import logging
import datetime

from data import db_logger_name, db_table_structure, \
    url_paths, update_time_threshold

class DBManager():
    def __init__(self, db_file, logger_name):
        self.db_file = db_file
        self.logger = logging.getLogger(logger_name)

    # size -1 means db_table_structure length is used
    def create_fields(self, character, size=-1):
        if size > 0:
            return "{}".format(",".join([ character for i in range(0, size)]))
        else:
            return "{}".format(",".join([ character for i in db_table_structure]))

    def is_empty(self):
        self.logger.info("Checking if db is empty")

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        try:
            c.execute(f'SELECT * FROM {[*url_paths.keys()][0]}')
            products = c.fetchmany(size=10)
        except sqlite3.Error as e:
            self.logger.warning(f'Error checking is database empty: {e}')
            return True
        
        logging.debug(f'is_empty returns: {not bool(products)}')
        return not bool(products)

    def create_db(self):
        self.logger.info('Creating database...')
        db_create_script = ""
        for product_group in url_paths.keys():
            script = "CREATE TABLE {}({});\n".format(product_group, self.create_fields('{}'))
            db_create_script += script.format(*db_table_structure)
        
        self.logger.debug(db_create_script)

        conn = sqlite3.connect(self.db_file)
        try:
            with conn:
                conn.executescript(db_create_script)
            self.logger.info('Database created successfully')
        except sqlite3.Error as e:
            self.logger.error(f'Could not create database: {e}')

        conn.close()


    def add_products(self, product_group, products):
        self.logger.info(f'Adding {product_group} to database')
        prods = self.parse_products_dict_to_db_format(products)
        cmd = "INSERT INTO {} VALUES ({})".format(product_group, self.create_fields('?'))
        self.logger.debug(cmd)

        conn = sqlite3.connect(self.db_file)
        try:
            with conn:
                conn.executemany(cmd, prods)
            self.logger.info(f'Added {product_group} products to database successfully')
        except sqlite3.Error as e:
            self.logger.error(f'Could not add {product_group}: {e}')

        conn.close()

    def fetch_products_from_db(self, table=""):
        self.logger.info(f'Fetching products {table} from database')
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        products = []
        prod_group = table
        
        try:
            if table == "":
                for product_group in url_paths.keys():
                    prod_group = product_group
                    c.execute(f'SELECT * FROM {product_group}')
                    products += c.fetchall()
            else:
                c.execute('SELECT * FROM ?', table)
                products += c.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f'Could not fetch {prod_group}: {e}')

        conn.commit()
        conn.close()

        self.logger.debug(f'Fetched products: {products}')
        return products
    
    def parse_products_dict_to_db_format(self, products):
        self.logger.info('Parsing products dict to db format')
        prods = []
        for product in products:
            row = []
            for field in db_table_structure:
                if "timestamp" in field:
                    row.append(datetime.datetime.now())
                else:
                    row.append(product[field])
            prods.append(row)
        self.logger.debug(f'Parsed products dict: {prods}')
        return prods

    def remove_row(self, prod):
        pass

    def check_last_timestamp(self):
        self.logger.info('Checking last timestamp')

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        timestamps = [] 
        try:
            c.execute(f'SELECT timestamp FROM {[*url_paths.keys()]}')
            timestamps += c.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f'Could not fetch timestamps: {e}')
        conn.commit()
        conn.close()
        self.logger.debug(f'Fetched timestamps: {timestamps}')

        timestamps_in_datetime = sorted(map(datetime.datetime.strptime, timestamps), reverse=True)
        print(timestamps)

        return timestamps