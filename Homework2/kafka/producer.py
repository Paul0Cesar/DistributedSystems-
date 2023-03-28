from confluent_kafka import Producer
import json
import time
import logging
import requests

TOPIC="BTC_CURRENCY"

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

p=Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer has been initiated...')

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

def run():
    while True:
        payload=requests.get("https://api.wazirx.com/sapi/v1/klines?symbol=btcinr&limit=1&interval=1m")
        data=payload.json()
        data={ #ohlc
           'at': data[0][0],
           'open':data[0][1],
            'high': data[0][2],
           'low':data[0][3],
           'close':data[0][4],
        }
        m=json.dumps(data)
        p.poll(1)
        p.produce(TOPIC, m.encode('utf-8'),callback=receipt)
        p.flush()
        time.sleep(60)   


run()

