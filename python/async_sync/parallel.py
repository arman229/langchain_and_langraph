from multiprocessing import Process
import time

def task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} done")

if __name__ == "__main__":
    p1 = Process(target=task, args=("A",))
    p2 = Process(target=task, args=("B",))
    p3 = Process(target=task, args=("C",))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
