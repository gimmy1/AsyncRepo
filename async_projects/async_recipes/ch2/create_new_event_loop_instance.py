import asyncio
import sys

loop = asyncio.new_event_loop()

print(loop)
asyncio.set_event_loop(loop) 

import pdb; pdb.set_trace()
if sys.platform != "win32":
    watcher = asyncio.get_child_watcher()
    # a gotcha --> must attach to the newly created loop to the event loop policy's watcher
    # to make sure that our event loop monitors the termination of newly spawned subprocesses on UNIX systems. 
    watcher.attach_loop(loop)