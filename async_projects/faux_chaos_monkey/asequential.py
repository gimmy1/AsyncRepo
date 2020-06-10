#!/usr/bin/env python3.7
"""
Tasks that monitor other tasks using `asyncio`'s `Event` object.
Notice! This requires:
 - attrs==19.1.0
"""

import asyncio
import functools
import logging
import random
import string
import signal
import uuid

import attr


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id    = attr.ib(repr=False)
    hostname      = attr.ib(repr=False, init=False)
    restarted     = attr.ib(repr=False, default=False)
    saved         = attr.ib(repr=False, default=False)
    acked         = attr.ib(repr=False, default=False)
    extended_cnt  = attr.ib(repr=False, default=0)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


async def shutdown(loop, signal=None):
    """ Cleanup tasks tied to the service's shutdown. """
    if signal:
        logging.info(f"Received exit signal {signal.name}...")

    logging.info(f"Closing database connections.")
    logging.info("Nacking outside messages")
    tasks = [t for t in asyncio.all_tasks() if t is not 
             asyncio.current_task()]
    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True) # when running pkill -TERM the code will just hang because gather does not return exceptions. Update with return_exceptions=True
    logging.info(f"Flushing metrics")
    loop.stop()


async def publish(queue):
    """Simulates an external publisher of messages.
    Args:
        queue (asyncio.Queue): Queue to publish messages to.
    """
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(message_id=msg_id, instance_name=instance_name)
        # publish an item
        asyncio.create_task(queue.put(msg))
        logging.debug(f"Published message {msg}")
        # simulate randomness of publishing messages
        await asyncio.sleep(random.random())


async def restart_host(msg):
    """Restart a given host.
    Args:
        msg (PubSubMessage): consumed event message for a particular
            host to be restarted.
    """
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    
    # example exception
    if random.randrange(1,5) == 3:
        raise RestartFailed(f"Could not restart {msg.hostname}")
    
    msg.restart = True
    logging.info(f"Restarted {msg.hostname}")


async def save(msg):
    """Save message to a database.
    Args:
        msg (PubSubMessage): consumed event message to be saved.
    """
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())

    # example exception
    if random.randrange(1, 5) == 3:
        raise Exception(f"Could not save {msg}")
    
    msg.save = True
    logging.info(f"Saved {msg} into database")

def handle_results(results, msg):
    for result in results:
        if isinstance(result, RestartFailed):
            logging.error(f"Retrying ffor failure to restart: {msg.hostname}")
        elif isinstance(result, Exception):
            logging.error(f"Handling general error: {result}")

async def handle_exception(loop, context):
    msg = context.get("Exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down..")
    asyncio.create_task(shutdown(loop))

async def cleanup(msg):
    """Cleanup tasks related to completing work on a message.
    Args:
        msg (PubSubMessage): consumed event message that is done being
            processed.
    """
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    msg.acked = True
    logging.info(f"Done. Acked {msg}")


async def extend(msg, event):
    """Periodically extend the message acknowledgement deadline.
    Args:
        msg (PubSubMessage): consumed event message to extend.
        event (asyncio.Event): event to watch for message extention or
            cleaning up.
    """
    while not event.is_set():
        msg.extended_cnt += 1
        logging.info(f"Extended deadline by 3 seconds for {msg}")
        # want to sleep for less than the deadline amount
        await asyncio.sleep(2)
    else:
        await cleanup(msg)


async def handle_message(msg):
    """Kick off tasks for a given message.
    Args:
        msg (PubSubMessage): consumed message to process.
    """
    event = asyncio.Event()
    asyncio.create_task(extend(msg, event))
    asyncio.create_task(cleanup(msg, event))

    results = await asyncio.gather(save(msg), restart_host(msg), return_exceptions=True)
    handle_results(results, msg)
    event.set()


async def consume(queue):
    """Consumer client to simulate subscribing to a publisher.
    Args:
        queue (asyncio.Queue): Queue from which to consume messages.
    """
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))

class RestartFailed(Exception):
    pass

def main():
    loop = asyncio.get_event_loop()

    SIGNALS = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in SIGNALS:
        loop.add_signal_handler( 
            s, lambda s=s: asyncio.create_task(shutdown(loop, signal=s)) # late bindings gotcha in python
        )
    
    loop.set_exception_handler(handle_exception)
    
    queue = asyncio.Queue()
    try:
        loop.create_task(publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")


if __name__ == "__main__":
    main()