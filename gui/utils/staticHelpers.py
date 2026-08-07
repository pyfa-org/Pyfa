class DragDropHelper:
    data = None

    def __init__(self):
        pass

    @classmethod
    def consume(cls):
        """
        Take what the current drag carries, leaving nothing behind.
        """
        data, cls.data = cls.data, None
        return data
