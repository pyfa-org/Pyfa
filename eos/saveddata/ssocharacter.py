# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

from sqlalchemy.orm import reconstructor
import datetime
import time

# from tomorrow import threads


class SsoCharacter(object):
    def __init__(self, charID, name, client, accessToken=None, refreshToken=None):
        self.characterID = charID
        self.characterName = name
        self.client = client
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.esi_client = None

    @reconstructor
    def init(self):
        self.esi_client = None

    def get_sso_data(self):
        """ Little "helper" function to get formated data for esipy security
        """
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken,
            'expires_in': (
                self.accessTokenExpires - datetime.datetime.utcnow()
            ).total_seconds()
        }

    def update_token(self, tokenResponse):
        """ helper function to update token data from SSO response """
        self.accessToken = tokenResponse['access_token']
        self.accessTokenExpires = datetime.datetime.fromtimestamp(
            time.time() + tokenResponse['expires_in'],
        )
        if 'refresh_token' in tokenResponse:
            self.refreshToken = tokenResponse['refresh_token']
        if self.esi_client is not None:
            self.esi_client.security.update_token(tokenResponse)