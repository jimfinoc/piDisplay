import redis
from dotenv import load_dotenv
import os
import json

class RedisConnection:
    def __init__(self):
        load_dotenv(".env")
        self.redis_host = os.getenv("redis_database_name")
        self.redis_port = os.getenv("redis_database_port")
        self.redis_password = os.getenv("redis_database_password")
        self.connection = None

    def connect(self):
        try:
            self.connection = redis.Redis(
                db=0,
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password
            )
            # Test the connection
            if self.connection.ping():
                print(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
                return self.connection
        except redis.RedisError as e:
            print(f"Redis connection error: {e}")
            return None
        

    def return_details(self,key):
        # try:
        load_dotenv(".env")
        # r = redis.Redis(db=0,host=os.getenv("redis_database_name"),port=os.getenv("redis_database_port"),password=os.getenv("redis_database_password"))
        My_details_string = self.connection.get(key)
        # My_details_string = r.get(key)
        My_details = json.loads(My_details_string)
        with open("."+str(key)+".json", "w") as file:
            json.dump(My_details, file, indent=4)

        # except:
            # pass
        return My_details

    def return_orders(status = "open"):
        returnData = []
        orders_details = return_details("My_orders_details")
        for each in orders_details:
            # print()
            # print(each)
            if status == "all":
                pass
            elif status == "open":
                if each['status'] == 'PENDING_ACTIVATION':
                    returnData.append(each)
                if each['status'] == 'WORKING':
                    returnData.append(each)
            elif status == "filled":
                if each['status'] == 'FILLED':
                    returnData.append(each)
        return returnData

    def return_positions(self, type = "all"):
        # returnData = []
        return_data = set()
        position_details = self.return_details("My_position_details")
        for each in position_details["securitiesAccount"]["positions"]:
            if type == "all" or type == "option":
                if each["instrument"]["assetType"] == "OPTION":
                    # print(each["instrument"]["underlyingSymbol"])
                    return_data.add(each["instrument"]["underlyingSymbol"])
            if type == "all" or type == "stock":
                if each["instrument"]["assetType"] == "EQUITY":
                    # print(each["instrument"]["symbol"])
                    return_data.add(each["instrument"]["symbol"])
        return return_data

    def all_dates(self, stock_option_dates):
        key = set()
        for each_stock in stock_option_dates:
            for each_date in stock_option_dates[each_stock]:
                key.add(each_date)
            # with open("."+str(key)+".json", "w") as file:
                # json.dump(My_details, file, indent=4)
        return key

    def total_calls_and_puts(self, My_position_details):
        total_calls = {}
        total_puts = {}
        for each in My_position_details["securitiesAccount"]["positions"]:
            if each["instrument"]["assetType"] == "OPTION":
                year = f'20{each["instrument"]["symbol"][6:8]}'
                month = f'{each["instrument"]["symbol"][8:10]}'
                day = f'{each["instrument"]["symbol"][10:12]}'
                special_date = f'{year}-{month}-{day}'
                quantity = each["shortQuantity"]
                    # print("special_date")
                    # print(special_date)
                if each["instrument"]["putCall"] == "CALL":
                    if special_date in total_calls:
                        total_calls[special_date] += quantity
                    else:
                        total_calls[special_date] = quantity
                elif each["instrument"]["putCall"] == "PUT":
                    if special_date in total_puts:
                        total_puts[special_date] += quantity
                    else:
                        total_puts[special_date] = quantity
        return total_calls, total_puts