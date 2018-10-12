# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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


from abc import ABCMeta, abstractmethod


class UserCancelException(Exception):
    """when user cancel on port processing."""
    pass


class IPortUser(metaclass=ABCMeta):

    ID_PULSE = 1
    # Pulse the progress bar
    ID_UPDATE = ID_PULSE << 1
    # Replace message with data: update messate
    ID_DONE = ID_PULSE << 2
    # open fits: import process done
    ID_ERROR = ID_PULSE << 3
    # display error: raise some error

    PROCESS_IMPORT = ID_PULSE << 4
    # means import process.
    PROCESS_EXPORT = ID_PULSE << 5
    # means import process.

    @abstractmethod
    def on_port_processing(self, action, data=None):
        """
        While importing fits from file, the logic calls back to this function to
        update progress bar to show activity. XML files can contain multiple
        ships with multiple fits, whereas EFT cfg files contain many fits of
        a single ship. When iterating through the files, we update the message
        when we start a new file, and then Pulse the progress bar with every fit
        that is processed.

        action : a flag that lets us know how to deal with :data
                None: Pulse the progress bar
                1: Replace message with data
                other: Close dialog and handle based on :action (-1 open fits, -2 display error)
        """

        """return: True is continue process, False is cancel."""
        pass

    def on_port_process_start(self):
        pass


def processing_notify(iportuser, flag, data):
    if not iportuser.on_port_processing(flag, data):
        raise UserCancelException
