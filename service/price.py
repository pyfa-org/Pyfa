# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import time
from xml.dom import minidom
import threading

from eos import db
from service.network import Network, TimeoutError
from service.fit import Fit
from logbook import Logger
from service.settings import NetworkSettings

pyfalog = Logger(__name__)


VALIDITY = 24 * 60 * 60  # Price validity period, 24 hours
REREQUEST = 4 * 60 * 60  # Re-request delay for failed fetches, 4 hours
TIMEOUT = 15 * 60  # Network timeout delay for connection issues, 15 minutes


class Price(object):
    instance = None

    systemsList = {
        "Jita": 30000142,
        "Amarr": 30002187,
        "Dodixie": 30002659,
        "Rens": 30002510,
        "Hek": 30002053
    }

    def __init__(self):
        # Start price fetcher
        self.priceWorkerThread = PriceWorkerThread()
        self.priceWorkerThread.daemon = True
        self.priceWorkerThread.start()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Price()
        return cls.instance

    @staticmethod
    def clearPriceCache():
        db.clearPrices()

    @classmethod
    def fetchItemPrice(cls, item):
        """Fetch price for a specific item"""

        if not item:
            return 0
        # Check if price is valid (within the time frame) or failed.
        elif item.price.isValid and item.price.failed is not True:
            return item.price.price

        try:
            return_items = Price.getMarketData([item])
            return return_items[0].price.price
        except:
            pyfalog.warning("Failed to get price for item: {0}", item.ID)
            return 0

    @classmethod
    def fetchItemPriceOLD(cls, item):
        """Fetch all prices passed to this method"""

        # Check if price is valid (within the time frame) or failed.
        if item.price.isValid and item.price.failed is not True:
            return item.price.price

        # We're not going to request items only with market group, as eve-central
        # doesn't provide any data for items not on the market
        if item is None or not item.marketGroupID:
            return 0

        network = Network.getInstance()
        settings = NetworkSettings.getInstance()

        if not settings.isEnabled(network.PRICES):
            # Network settings for fetching prices is disabled. Try and return the cache or return nothing.
            if item.price.price:
                return item.price.price
            else:
                return 0

        # This will store POST data for eve-central
        data = []

        sFit = Fit.getInstance()
        # Base request URL
        baseurl = "https://eve-central.com/api/marketstat"
        data.append(("usesystem", cls.systemsList[sFit.serviceFittingOptions["priceSystem"]]))  # Use Jita for market
        data.append(("typeid", item.ID))

        # Attempt to send request and process it
        try:
            data = network.request(baseurl, network.PRICES, data)
            xml = minidom.parse(data)
            types = xml.getElementsByTagName("marketstat").item(0).getElementsByTagName("type")
            # Cycle through all types we've got from request
            for type_ in types:
                # Get data out of each typeID details tree
                typeID = int(type_.getAttribute("id"))
                sell = type_.getElementsByTagName("sell").item(0)

                if item.ID != typeID:
                    pyfalog.warning("Type mismatch between passed in value ({0}) and returned value ({1}).", item.ID, typeID)
                    percprice = 0
                else:
                    # If price data wasn't there, set price to zero
                    try:
                        percprice = float(sell.getElementsByTagName("percentile").item(0).firstChild.data)
                    except (TypeError, ValueError):
                        pyfalog.warning("Failed to get price for: {0}", type_)
                        percprice = 0

                # Fill price data
                priceobj = item.price
                priceobj.price = percprice
                priceobj.time = time.time() + VALIDITY
                priceobj.failed = None

            return item.price.price

        # If getting or processing data returned any errors
        except TimeoutError:
            # Timeout error deserves special treatment
            pyfalog.warning("Price fetch timout")
            priceobj = item.price
            priceobj.time = time.time() + TIMEOUT
            priceobj.failed = True
            return 0
        except:
            # all other errors will pass and continue onward to the REREQUEST delay
            pyfalog.warning("Caught exception in fetchPrices")

        # if we get to this point, then we've got an error. Set to REREQUEST delay
        priceobj = item.price
        priceobj.time = time.time() + REREQUEST
        priceobj.failed = True
        return 0

    @classmethod
    def getMarketData(cls, items=None):
        if items is None:
            # No items passed in, so nothing to return
            # This is here to catch if we run out of items to update from our update price thread
            return []

        network = Network.getInstance()
        settings = NetworkSettings.getInstance()

        if not settings.isEnabled(network.PRICES):
            # Network settings for fetching prices is disabled.
                return None

        # This will store POST data for eve-central
        data = []

        sFit = Fit.getInstance()
        # Base request URL
        baseurl = "https://eve-central.com/api/marketstat"
        data.append(("usesystem", cls.systemsList[sFit.serviceFittingOptions["priceSystem"]]))

        for item in items:  # Add all typeID arguments
            data.append(("typeid", item.ID))

        return_items = []

        # Attempt to send request and process it
        try:
            data = network.request(baseurl, network.PRICES, data)
            xml = minidom.parse(data)
            types = xml.getElementsByTagName("marketstat").item(0).getElementsByTagName("type")

            # Cycle through all types we've got from request
            for type_ in types:
                try:
                    # Get data out of each typeID details tree
                    sell = type_.getElementsByTagName("sell").item(0)
                    typeID = int(type_.getAttribute("id"))

                    # If price data wasn't there, set price to zero
                    try:
                        percprice = float(sell.getElementsByTagName("percentile").item(0).firstChild.data)
                    except (TypeError, ValueError):
                        pyfalog.warning("Failed to get price for: {0}", type_)
                        percprice = 0

                    # Fill price data
                    priceobj = db.getItem(typeID)
                    priceobj.price.price = percprice
                    priceobj.price.time = time.time() + VALIDITY
                    priceobj.price.failed = False

                    # Append this item so we can return it and see what items were updated.
                    return_items.append(priceobj)
                except Exception as e:
                    try:
                        # if we get to this point, then we've got an error. Set to REREQUEST delay
                        # Try and handle this neatly.
                        typeID = int(type_.getAttribute("id"))
                        priceobj = db.getItem(typeID)
                        priceobj.time = time.time() + REREQUEST
                        priceobj.failed = True
                        pyfalog.warning("Failed to update price for item: {0}", typeID)
                    except:
                        # We critically failed, most likely a bad return or couldn't even get the item ID.
                        pyfalog.error("Critical failure on updating price.")
                        pyfalog.debug(type_)
                        pyfalog.debug(e)

        # If getting or processing data returned any errors
        except TimeoutError:
            # Timeout error deserves special treatment
            pyfalog.warning("Price fetch timout")
        except Exception as e:
            # all other errors will pass and continue onward to the REREQUEST delay
            pyfalog.warning("Caught exception in fetchPrices")
            pyfalog.warning(e)

        return return_items


class PriceWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "PriceWorker"
        pyfalog.debug("Initialize PriceWorkerThread.")

    def run(self):
        # Get all items
        all_items = db.getAllItems()

        # Filter out items that are:
        # -Unpublished
        # -Without a market group
        # -Without skills
        # This will filter out some valid items, but they'll be caught later if they're missing a price
        # TODO: Move the filtering to SQL so it can be done faster.  Not a big deal, but would get the thread moving quicker.
        all_items = [item for item in all_items if item.marketGroupID and item.published and item.requiredSkills]

        while True:
            pyfalog.debug("Price run start")

            # Make a copy of our list so we can fiddle with it
            # Filter out any items where they have a valid price, not marked as failed, and are still within our timeframe.
            shopping_list = [item for item in all_items if item.price.isValid is not True or item.price.failed is True or not item.price.price]

            # Truncate our list to 100.  This is an arbitrary number, but we don't want to try and grab _everything_ at once.
            # TODO: Add this as an option
            max_shopping_list = 333
            if len(shopping_list) > max_shopping_list:
                shopping_list = shopping_list[:max_shopping_list]

            return_items = Price.getMarketData(shopping_list)
            pyfalog.debug("Updated price on {0} items.", return_items.__len__())

            pyfalog.debug("Price run end")

            # Sleep for 60 seconds
            # TODO: Add this as an option
            time.sleep(60)
