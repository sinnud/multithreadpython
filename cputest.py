import sys
import datetime # date and time
import os
from subprocess import call
import logzero
from multiprocessing import Pool
from logzero import logger
import traceback # Python error trace


def cputest(args_dict):
    i, n = args_dict['i'], args_dict['n']
    looplen = args_dict['looplen']
    # code from https://stackoverflow.com/questions/8326929/test-computer-processing-speed-with-a-simple-python-script
    test = "a test string"
    for i in range(looplen):  # it takes forever, so choose this value wisely!
        if len(test) < 200000000:  # somewhere above this limit I get errors
            test += test
        else:
            test = test[0:int(len(test) / 2)]  # if the string gets too long just cut it.
    return True

def main(looplen=None):
    n=10 # multithread number
    args_dict = {}
    args_dict['n']=n
    args_dict['looplen']=looplen
    logger.info("Before parallel processing")
    with Pool(n) as pool:
        arg_list = [dict(**args_dict, **{'i': i}) for i in range(n)]
        result = pool.map(cputest, arg_list)
        logger.debug(f"Pool result:{result}")
        if not all(result):
            return False

    logger.info("After parallel processing")

    # collect log files
    # if log_path is not None:
    #     for thread in range(n):
    #         threadlog = f"{log_path}/{os.path.basename(os.path.realpath(__file__)).replace('.py', f'_{thread}.log')}"
    #         with open(threadlog, 'r') as f:
    #             data = f.read()
    #         logger.info(f"Collected {thread} log file content from {threadlog}:\n{data}")
    #         os.remove(threadlog)
    return True

if __name__ == '__main__':
    mylog = os.path.realpath(__file__).replace('.py', '.log')
    if os.path.exists(mylog):
        os.remove(mylog)
    logzero.logfile(mylog)

    logger.info(f'start python code {__file__}.\n')
    looplen=100
    rst=main(looplen=looplen)
    logger.info(f'finish python code {__file__}.\n')
