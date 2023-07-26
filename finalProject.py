print (" with Adafruit IO")
import sys
import time

from Adafruit_IO import MQTTClient
import requests

AIO_USERNAME = "OrangeJuice0101"
AIO_KEY = "aio_eSdN21ia0wj39eN2WRGE1XVxD1sG"
global_equation = "x1 + x2 + x3"

def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/OrangeJuice0101/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

mathScore=""
def init_global_math():
    global mathScore
    headers = {}
    aio_url="https://io.adafruit.com/api/v2/OrangeJuice0101/feeds/math-score"
    y=requests.get(url=aio_url, headers=headers, verify=False)
    data = y.json()
    mathScore = data["last_value"]
    print("Get lastest value:", mathScore)


engScore=""
def init_global_eng():
    global engScore
    headers = {}
    aio_url="https://io.adafruit.com/api/v2/OrangeJuice0101/feeds/english-score"
    y=requests.get(url=aio_url, headers=headers, verify=False)
    data = y.json()
    engScore = data["last_value"]
    print("Get lastest value:", engScore)

literScore=""
def init_global_liter():
    global literScore
    headers = {}
    aio_url="https://io.adafruit.com/api/v2/OrangeJuice0101/feeds/literature-score"
    y=requests.get(url=aio_url, headers=headers, verify=False)
    data = y.json()
    literScore = data["last_value"]
    print("Get lastest value:", literScore)

def modify_value(x1, x2, x3):
    print("Equation", global_equation)
    result = eval(global_equation)
    return result

def connected(client):
    print("Server connected ...")
    
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribeb!!!")

def disconnected(client):
    print("Disconnected from the server!!!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: topic " + feed_id + " " + payload)
    if (feed_id=="equation"):
        global global_equation
        global_equation = payload
        print(global_equation)


client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected  #function pointer call back
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()
init_global_math()
init_global_eng()
init_global_liter()


while True:
    time.sleep (60)
    print("Updating...")
    init_global_math()
    init_global_eng()
    init_global_liter()
    
    value4 = modify_value(int(mathScore), int(engScore), int(literScore))
    client.publish("entrance-exam-score", value4)
    pass