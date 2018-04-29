import time


class Timer(object):
    def __init__(self, name='', logger=None):
        self.name = name
        self.start = time.time()
        self.__last = self.start
        self.logger = logger

    @property
    def elapsed(self):
        return (time.time() - self.start) * 1000

    @property
    def last(self):
        return (time.time() - self.__last) * 1000

    def checkpoint(self, name=''):
        text = 'Timer - {timer} - {checkpoint} - {last:.2f}ms ({elapsed:.2f}ms elapsed)'.format(
                timer=self.name,
                checkpoint=name,
                last=self.last,
                elapsed=self.elapsed
        ).strip()
        self.__last = time.time()
        if self.logger:
            self.logger.debug(text)
        else:
            print(text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass
