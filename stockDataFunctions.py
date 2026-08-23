import redis
from dotenv import load_dotenv
import os
import json
import sys

class RedisConnection:
    stock_prices = {}

    def __init__(self):
        load_dotenv(".env")
        self.redis_host = os.getenv("redis_database_name")
        self.redis_port = os.getenv("redis_database_port")
        self.redis_password = os.getenv("redis_database_password")
        self._connection = None

    def connect(self):
        try:
            self._connection = redis.Redis(
                db=0,
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password
            )
            # Test the connection
            if self._connection.ping():
                print(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
                return self._connection
        except redis.RedisError as e:
            print(f"Redis connection error: {e}")
            return None
        

    def return_details(self,key):
        if self._connection.exists(key):
            My_details_string = self._connection.get(key)
        else:
            print()
            print(f'key: {key}')
            print(f'does not exist')
            print()
            if key == "My:orders_details":
                print('In the dirctory: stocks')
                print('execute: python functionDatabaseItem.py')
            if key == "My_quotes":
                print('In the dirctory: stocks')
                print('execute: python functionSchwabDataStreamer.py')
            sys.exit(0) 

        My_details = json.loads(My_details_string)
        with open("."+str(key)+".json", "w") as file:
            json.dump(My_details, file, indent=4)
        return My_details

    def return_orders(self, status = "open"):
        returnData = []
        orders_details = self.return_details("My:orders_details")
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
        position_details = self.return_details("My:position_details")
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
    
    def subscriber(self,subscribed_stock):
        pubsub = self._connection.pubsub()
        pubsub.subscribe(subscribed_stock)
        print(f"Subscribed to {subscribed_stock}. Waiting for messages...")

        for message in pubsub.listen():
            if message['type'] == 'message':
                print(f'Received message on: "{subscribed_stock}"')
                message_string = message['data']
                message_json = json.loads(message_string)

                print(message_json)
                # print(f"Received: {message['data']}")
                print(json.dumps(message_json, indent=4))
                print()
        self.stock_prices[subscribed_stock] = message_json
            # if message['data'] == 'quit':
            #     print("Unsubscribing and exiting...")
            #     pubsub.unsubscribe()
            #     break
    
    def get_sub_data(self):
        return self.stock_prices

