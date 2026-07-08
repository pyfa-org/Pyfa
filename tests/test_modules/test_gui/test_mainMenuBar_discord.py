# Add root folder to python paths
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from gui.menu_utils import syncDiscordShareMenuVisibility


class FakeMenuItem:
    def __init__(self, item_id):
        self.item_id = item_id


class FakeMenu:
    def __init__(self):
        self.items = []

    def FindItemById(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def GetMenuItems(self):
        return list(self.items)

    def Insert(self, index, item_id, _text, _help):
        item = FakeMenuItem(item_id)
        self.items.insert(index, item)
        return item

    def Remove(self, item):
        self.items.remove(item)


def test_sync_discord_share_menu_visibility_adds_menu_item_when_enabled():
    fit_menu = FakeMenu()
    optimize_id = 10
    share_id = 20
    fit_menu.items = [FakeMenuItem(optimize_id)]

    syncDiscordShareMenuVisibility(fit_menu, share_id, optimize_id, True, 'Share', 'Help')

    assert fit_menu.FindItemById(share_id) is not None


def test_sync_discord_share_menu_visibility_removes_menu_item_when_disabled():
    fit_menu = FakeMenu()
    optimize_id = 10
    share_id = 20
    fit_menu.items = [FakeMenuItem(optimize_id), FakeMenuItem(share_id)]

    syncDiscordShareMenuVisibility(fit_menu, share_id, optimize_id, False, 'Share', 'Help')

    assert fit_menu.FindItemById(share_id) is None
