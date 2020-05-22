from multiprocessing import Process

def execute_routine(function, args=None):
    process = Process(target=function, args=args)
    process.start()
    process.join()
