from gui.bitmapLoader import BitmapLoader
from pfSearchBox import PFSearchBox


class SearchBox(PFSearchBox):
    def __init__(self, parent, **kwargs):
        PFSearchBox.__init__(self, parent, **kwargs)
        cancelBitmap = BitmapLoader.getBitmap("fit_delete_small", "gui")
        searchBitmap = BitmapLoader.getBitmap("fsearch_small", "gui")
        self.SetSearchBitmap(searchBitmap)
        self.SetCancelBitmap(cancelBitmap)
        self.ShowSearchButton()
        self.ShowCancelButton()
