import time
import threading


def timer(seconds: float):
    current_seconds = 0

    start_time = time.time()

    while True:
        cur_time = time.time() - start_time
        
        if cur_time > 1 + current_seconds:
            current_seconds += 1
            print(current_seconds)
        
        if current_seconds == seconds:
            return


def main():
    timer_seconds = float(input('How much seconds to run the timer: '))
    t1 = threading.Thread(target=timer, args=[timer_seconds])
    t1.start()

    run = True
    for i in range(1_000_000):
        for j in range(1_000_000):
            if not t1.is_alive():
                run = False
                break
        if not run:
            break
    
    all_numbers = i * 1_000_000 + j
    print(f'Numbers on stop i: {i}, j: {j}')
    print(f'{all_numbers} numbers were passed')
    print(f'{all_numbers / timer_seconds:.2f} numbers in one second')
    print('End!')


if __name__ == '__main__':
    main()
