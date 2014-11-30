import time

class Timer(object):
    """
    Generic timing class for simple profiling.

    Usage:

    with Timer(verbose=True) as t:
        # code to be timed
        time.sleep(5)

    Output:
    elapsed time: 5000.000 ms

    Can also access time with t.secs
    """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs