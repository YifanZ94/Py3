# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 18:26:59 2024

@author: Administrator
"""
# import nest_asyncio
# nest_asyncio.apply()

# import asyncio
# from bleak import BleakScanner

# async def main():
#     devices = await BleakScanner.discover()
#     for device in devices:
#         print(device)

# asyncio.run(main())



import asyncio
from bleak import discover

async def run():
    devices = await discover()
    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())