"""For various reasons, it is imperative that a concurrency framework is able
to tell you whether an event loop is currently running and which one it
is. For instance, it might be essential for your code to assert that only one
certain loop implementation is running your task. Hence only one task
can alter some shared resource or to be sure that your callbacks will be
dispatched."""

import asyncio
def get_current_running_loop_solution1():
    try: # in >=3.7 two valid ways to get current running loop instance
        loop = asyncio.get_running_loop()
    except RuntimeError:
        print("No running loop")
        return
    return loop
    
def get_current_running_loop_solution2():
    loop = asyncio.get_event_loop()
    return loop

if __name__ == "__main__":
    print(get_current_running_loop_solution1())
    print(get_current_running_loop_solution2())
