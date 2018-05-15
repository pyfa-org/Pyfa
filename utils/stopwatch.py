# coding: utf-8

import time
import os


class Stopwatch(object):
    """
 --- on python console ---
import re
from utils.stopwatch import Stopwatch

# measurementor
stpw = Stopwatch("test")
# measurement re.sub
def m_re_sub(t, set_count, executes, texts):
    t.reset()
    while set_count:
        set_count -= 1
        with t:
            while executes:
                executes -= 1
                ret = re.sub("[a|s]+", "-", texts)
    # stat string
    return str(t)

# statistics loop: 1000(exec re.sub: 100000)
m_re_sub(stpw, 1000, 100000, "asdfadsasdaasdfadsasda")

----------- records -----------
 text: "asdfadsasda"
    'elapsed record(ms): min=0.000602411446948, max=220.85578571'
    'elapsed record(ms): min=0.000602411446948, max=217.331377504'

 text: "asdfadsasdaasdfadsasda"
    'elapsed record(ms): min=0.000602411446948, max=287.784902967'
    'elapsed record(ms): min=0.000602411432737, max=283.653264016'

    NOTE: about max
      The value is large only at the first execution,
      Will it be optimized, after that it will be significantly smaller
    """

    # time.clock() is μs? 1/1000ms
    # https://docs.python.jp/2.7/library/time.html#time.clock
    _tfunc = time.clock if os.name == "nt" else time.time

    def __init__(self, name='', logger=None):
        self.name = name
        self.start = Stopwatch._tfunc()
        self.__last = self.start
        # __last field is means last checkpoint system clock value?
        self.logger = logger
        self.min = 0.0
        self.max = 0.0
        self.__first = True

    @property
    def stat(self):
        # :return: (float, float)
        return self.min, self.max

    @property
    def elapsed(self):
        # :return: time as ms
        return (Stopwatch._tfunc() - self.start) * 1000

    @property
    def last(self):
        return self.__last * 1000

    def __update_stat(self, v):
        # :param v: float unit of ms
        if self.__first:
            self.__first = False
            return
        if self.min == 0.0 or self.min > v:
            self.min = v
        if self.max < v:
            self.max = v

    def checkpoint(self, name=''):
        span = self.elapsed
        self.__update_stat(span)
        text = 'Stopwatch("{tname}") - {checkpoint} - {last:.6f}ms ({elapsed:.12f}ms elapsed)'.format(
                tname=self.name,
                checkpoint=str(name, "utf-8"),
                last=self.last,
                elapsed=span
        ).strip()
        self.__last = Stopwatch._tfunc()
        if self.logger:
            self.logger.debug(text)
        else:
            print(text)

    @staticmethod
    def CpuClock():
        start = Stopwatch._tfunc()
        time.sleep(1)
        return Stopwatch._tfunc() - start

    def reset(self):
        # clear stat
        self.min = 0.0
        self.max = 0.0
        self.__first = True

    def __enter__(self):
        self.start = Stopwatch._tfunc()
        return self

    def __exit__(self, type_, value, traceback):
        # https://docs.python.org/2.7/reference/datamodel.html?highlight=__enter__#object.__exit__
        # If the context was exited without an exception, all three arguments will be None
        self.checkpoint('finished')
        # ex: "type=None, value=None, traceback=None"
        # print "type=%s, value=%s, traceback=%s" % (type, value, traceback)
        return True

    def __repr__(self):
        return "elapsed record(ms): min=%s, max=%s" % self.stat
