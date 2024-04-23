import threading
from math import floor
import time
import random


num_threads = [2, 4, 8, 16, 32, 64]
num_points = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]

def insideSum(beg, end, threadNum, lock, in_arr):
    local_inside = 0
    random.seed(time.localtime().tm_sec + threadNum)
    for i in range(beg, end):
       x =  random.uniform(0, 1)
       y =  random.uniform(0, 1)

       if(x*x + y*y < 1):
           local_inside += 1

    with lock:
        in_arr.append(local_inside)


def main():
    for thread in num_threads:
        for point in num_points:

            slice = floor(point / thread)
            ind_start = 0
            inside_total = 0

            time_start = time.perf_counter()
            thread_arr = []
            in_arr = []
            lock = threading.Lock()

            for i in range(thread):
                ind_end = point if i == thread - 1 else ind_start + slice - 1
                t = threading.Thread(target=insideSum, args=[ind_start, ind_end, i, lock, in_arr])
                t.start()
                thread_arr.append(t)
                ind_start += slice

            for t in thread_arr:
                t.join()

            time_end = time.perf_counter()
            # num points, num threads, pi, time
            print(f'{point} {thread} {float(sum(in_arr) * 4) / point} {time_end - time_start}')


if __name__ == "__main__":
    main()
