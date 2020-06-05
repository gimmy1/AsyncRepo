import os
import time
from PIL import Image
from multiprocessing import Process

# Iterate over the directory -- see how long it takes
def iterate_over_directory(directory):
    for fn in os.listdir(directory):
        print(os.path.join(directory, fn))

if __name__ == "__main__":
    start = time.time()
    print(iterate_over_directory("images"))
    print(time.time() - start)
