#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 15:37:17 2021

@author: Celeste
"""


import asyncio
import time
from requests import post
#sys.path.append('../../../')

from bfxapi import Client

now = int(round(time.time() * 1000))
then = now - 60*60*12*1000

#LINE
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        'message': msg
    }
    r = post("https://notify-api.line.me/api/notify",
              headers=headers,
              params=payload)
    return r.status_code

token = 'TOKEN'

bfx = Client(
  API_KEY='API_KEY',
  API_SECRET='API_SECRET',
  logLevel='DEBUG'
)

#FRR
async def log_public_funding_stats():
  #得public_funding_stats資料
  usdt = await bfx.rest.get_public_funding_stats('fUST')
  usd = await bfx.rest.get_public_funding_stats('fUSD')
  #get FRR
  FRR_usdt = usdt[0][3]*365*365
  FRR_usd = usd[0][3]*365*365
  #推播訊息
  if (FRR_usdt>=0.2) | (FRR_usd>=0.2):
    string = "\n[Bitfinex]高利率通知：\nUSD：{}\nUSDT：{}".format(format(FRR_usd,'.2%'),format(FRR_usdt,'.2%'))
    lineNotifyMessage(token, string)

#HIGH APR
async def log_public_candles():
  #得public_candles資料
  usd = await bfx.rest.get_public_candles('fUSD:p7', start = then, end=now, tf='1h',limit=1)
  usdt = await bfx.rest.get_public_candles('fUST:p7', start = then, end=now, tf='1h',limit=1)
  #get high APR
  high_usd = usd[0][3]*365
  high_usdt = usdt[0][3]*365
  #推播訊息
  if (high_usd>=0.2) | (high_usdt>=0.2):
    string = "\n[Bitfinex]高利率通知：\nUSD：{}\nUSDT：{}".format(format(high_usd,'.2%'),format(high_usdt,'.2%'))
    lineNotifyMessage(token, string)
  
async def run():
  await log_public_candles()
  
t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)






