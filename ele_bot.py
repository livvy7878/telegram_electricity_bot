import os
import sys
import asyncio
import requests
<<<<<<< HEAD
import logging
=======
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
>>>>>>> b850b7b353b1ec564cc94d9c854b699b00468ee8
from collections import deque

class state:
    def __init__(self, value, message):
        self.value = value
        self.message = message


telegramBotToken = "5892763019:AAGEbvptS5kOnkOon-ksvIfWLhj9q4leqmo"
hostname = sys.argv[1]
chatId = "-1001713448987"

server_polling_interval = 30

state_values = {
    "Off": state(value="IsTurnedOff", message="Свет выключен:("),
    "On": state(value="IsRunning", message="Сейчас есть свет!")
}

state_buffer_length = 6

turned_on_theshold = state_buffer_length * 0.7

state_buffer = deque(maxlen=state_buffer_length)

current_signaled_state = state_values["Off"]

web_server: HTTPServer

state_lock = threading.Lock()

async def send_message_on_status_change():
    while True:
        insert_off_in_state_buffer()

        do_state_change_on_threshold()

        await asyncio.sleep(insert_off_interval)

def insert_off_in_state_buffer():
    state_lock.acquire()
    state_buffer.append(state_values["Off"])
    state_lock.release()

def do_state_change_on_threshold():
    global current_signaled_state
    if (not state_values["On"] in state_buffer 
            and current_signaled_state is not state_values["Off"]):
        post_message_to_group(state_values["Off"].message)
        current_signaled_state = state_values["Off"]
    elif (count_of_on_states() >= int(turned_on_theshold)
            and current_signaled_state is not state_values["On"]):
        post_message_to_group(state_values["On"].message)
        current_signaled_state = state_values["On"]

    logging.info(f'CURRENT COUNT OF ONs IN state_buffer: {count_of_on_states()}')

def count_of_on_states():
    return state_buffer.count(state_values["On"])

def post_message_to_group(message):
    global chatId
    global telegramBotToken
    url = f"https://api.telegram.org/bot{telegramBotToken}/sendMessage?chat_id={chatId}&text={message}"
    requests.get(url)

def run_server():
    global web_server
    web_server = HTTPServer(('localhost', 9123), Server)
    web_server.serve_forever()

async def main():
    global current_signaled_state
    global state_buffer

    logging.basicConfig(filename='/home/bot_execution.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    for x in range(int(state_buffer_length / 2)):
        state_buffer.append(state_values["Off"])

    for x in range(int(state_buffer_length / 2)):
        state_buffer.append(state_values["On"])

    await send_message_on_status_change()

asyncio.run(run_server())
asyncio.run(main())

class Server(BaseHTTPRequestHandler):
    def GET(self):
        state_lock.acquire()
        state_buffer.append(state_values["On"])
        state_lock.release()
        self.send_response(200)
