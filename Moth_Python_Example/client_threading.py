import websockets
import asyncio
import cv2
import numpy as np
import time
from datetime import datetime
import threading

'''
connections = set()
connections.update([
    "ws://cobot.center:8286/pang/ws/sub?channel=instant&name=dGVzdA==&track=video",
    "ws://cobot.center:8286/pang/ws/sub?channel=instant&name=dGVzdA==&track=colink",
    "ws://cobot.center:8286/pang/ws/pub?channel=instant&name=dGVzdA==&track=metric"
]
)
'''

URI = "ws://cobot.center:8286/pang/ws/sub?channel=instant&name=dGVzdA==&track=video"

async def websockets_handler():
    async with websockets.connect(URI, ping_interval=None) as ws:
        print("Connected to", URI)
        track = URI.split("&track=", 1)[1]
        if track == "video":
            prev_frame_time = 0
            curr_frame_time = 0
            fps = 0

            while True:
                await asyncio.sleep(0.016)
                img_binary_data = await ws.recv()
                encoded_img = np.frombuffer(img_binary_data, dtype=np.uint8)
                img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
                curr_frame_time = time.time()
                fps = round(1/(curr_frame_time - prev_frame_time), 2)
                cv2.putText(img, str(fps), (20, 70), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 2)
                cv2.imshow('win', img)
                prev_frame_time = curr_frame_time
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

asyncio.get_event_loop().run_until_complete(websockets_handler())






