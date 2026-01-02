import json
import redis
import time
import os
from dotenv import load_dotenv
import json

import threading
from queue import Queue
from color.print import prBlack,prBlue,prCyan,prGreen,prLightPurple,prPurple,prRed,prYellow
from dotenv import load_dotenv


class RedisConnection:
    def __init__(self,debug=False):
        load_dotenv(".env")

        # self._connection = redis.Redis(db=0,host=os.getenv("redis_database_name"),port=os.getenv("redis_database_port"),password=os.getenv("redis_database_password"))

        self.redis_host = os.getenv("redis_database_name")
        self.redis_port = os.getenv("redis_database_port")
        self.redis_password = os.getenv("redis_database_password")
        self._connection = None
        try:
            self._connection = redis.Redis(
                db=0,
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password
            )
        except redis.RedisError as e:
            print(f"Redis connection error: {e}")
            quit()


        self._shared_dictionary = {}
        self._queue = Queue()
        self._debug = debug
        self._subscriber_threads = {}
        self._running = True
        
        if self._debug: prBlue("Blue: __init()__ function")
        if self._debug: prRed("Red: _listen() function")
        if self._debug: prYellow("Yellow: subscribe() function")
        if self._debug: prGreen('Green: dictionary return')
        if self._debug: prPurple('Purple: processor')
        if self._debug: prCyan('Cyan: get_connection')


            # processor thread handles all subscribers data collection and puts it into a shared dictionary
        if self._debug: prBlue("creating the processor thread.")
        self.processor_thread = threading.Thread(target=self.processor, args=("begin", ))

        if self._debug: prBlue("starting the processor thread.")
        self.processor_thread.start()

    def connect(self):
        if self._connection.ping():
            prCyan(f"Redis is connected at {self.redis_host}:{self.redis_port}")
            return self._connection


    def return_dictionary(self):
        if self._debug: prGreen("returning dictionary")
        return self._shared_dictionary

    def processor(self,command):
        if self._debug: prPurple(f"processor will {command} now")
        while True:
            message_string = self._queue.get()
            if not self._running:
                break
            try:
                message_json = json.loads(message_string)
                stock = message_json["symbol"]
                self._shared_dictionary[stock] = message_json
                # if self._debug: prPurple (f'received message_string {message_string} for stock {stock} and updated prices_dictionary')
                if self._debug: prPurple (f'message updated for stock {stock}')
            except:
                if self._debug: prPurple (f'error processing {message_string}')
        if self._debug: prPurple("processor is out of while true loop.")

    def _listen(self, channel):
        pubsub = self._connection.pubsub()
        if self._debug: prRed(f"subscribing to {channel}.")
        pubsub.subscribe(channel)
        if self._debug: prRed(f"subscribed to {channel}.")

        for message in pubsub.listen():
            if not self._running:
                break
            if message['type'] == 'message':
                data = message['data']
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                if self._debug: prRed(f"Received from Redis, adding to queue: {data}")
                self._queue.put(data)
        if self._debug: prRed(f"listening on {channel} is ending.")

    def subscribe(self, channel):
        """
        Sets up the Redis pub/sub listener and runs it in a background thread.
        """
        if self._debug: prYellow("In the Redis subscribe thread...")
        # Create a pubsub instance
        
        # Subscribe to a channel and register the handler
        # pubsub.subscribe(**{channel: message_handler})
        if self._debug: prYellow(f'Subscribed to {channel} and waiting for messages')

        self._subscriber_threads[channel] = threading.Thread(target=self._listen, args=(channel,))
        self._subscriber_threads[channel].daemon = True
        self._subscriber_threads[channel].start()




        # Run the pubsub loop in a background thread
        # The 'sleep_time' argument allows the thread to briefly sleep, preventing a 100% CPU loop
        # thread = pubsub.run_in_thread(sleep_time=0.01)
        
        if self._debug: prYellow("Subscriber thread is running in the background.")
        # return thread, pubsub

    def return_details(self,key):
        My_details_string = self._connection.get(key)
        My_details = json.loads(My_details_string)
        with open("."+str(key)+".json", "w") as file:
            json.dump(My_details, file, indent=4)
        return My_details

    def return_orders(self, status = "open"):
        returnData = []
        orders_details = self.return_details("My_orders_details")
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
        return_data = set()
        position_details = self.return_details("My_position_details")
        for each in position_details["securitiesAccount"]["positions"]:
            if type == "all" or type == "option":
                if each["instrument"]["assetType"] == "OPTION":
                    return_data.add(each["instrument"]["underlyingSymbol"])
            if type == "all" or type == "stock":
                if each["instrument"]["assetType"] == "EQUITY":
                    return_data.add(each["instrument"]["symbol"])
        return return_data

    def all_dates(self, stock_option_dates):
        key = set()
        for each_stock in stock_option_dates:
            for each_date in stock_option_dates[each_stock]:
                key.add(each_date)
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

    def quit(self):
        # This sends None to get the processor to stop processing
        self._queue.put(None) 
        self._running = False

        # This waits for the processor to finish
        self.processor_thread.join()      
        if self._debug: prLightPurple("processor thread is also done")
        # other threads are not
