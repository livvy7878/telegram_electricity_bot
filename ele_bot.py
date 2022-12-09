import os
import sys
import asyncio
import requests
from collections import deque

class state:
    def __init__(self, value, message):
        self.value = value
        self.message = message


telegramBotToken = "5892763019:AAGEbvptS5kOnkOon-ksvIfWLhj9q4leqmo"
chatId = "-834737152"

hostname = sys.argv[1]
server_polling_interval = 1

state_values = {
    "Off": state(value="IsTurnedOff", message="Свет выключен:("),
    "On": state(value="IsRunning", message="Сейчас есть свет!")
}

state_buffer_length = 10
turned_on_theshold = state_buffer_length * 0.7

state_buffer = deque(maxlen=state_buffer_length)

current_signaled_state = state_values["Off"]


async def send_message_on_status_change():
    while True:
        current_state = retrieve_current_state()
        state_buffer.append(current_state)

        await do_state_change_on_threshold()
        
        await asyncio.sleep(server_polling_interval)

async def do_state_change_on_threshold():
    global current_signaled_state
    if (not state_values["On"] in state_buffer 
            and current_signaled_state is not state_values["Off"]):
        post_message_to_group(state_values["Off"].message)
        current_signaled_state = state_values["Off"]
    elif (count_of_on_states() >= int(turned_on_theshold)
            and current_signaled_state is not state_values["On"]):
        post_message_to_group(state_values["On"].message)
        current_signaled_state = state_values["On"]

def count_of_on_states():
    return state_buffer.count(state_values["On"])

def retrieve_current_state():
    response = not os.system("ping -c 1 " + hostname)

    if response == 0:
        return state_values["Off"]
    return state_values["On"]

def post_message_to_group(message):
    url = f"https://api.telegram.org/bot{telegramBotToken}/sendMessage?chat_id={chatId}&text={message}"
    requests.get(url)


async def main():
    global current_signaled_state
    global state_buffer
    for x in range(int(state_buffer_length / 2)):
        state_buffer.append(state_values["Off"])

    for x in range(int(state_buffer_length / 2)):
        state_buffer.append(state_values["On"])

    await send_message_on_status_change()

asyncio.run(main())