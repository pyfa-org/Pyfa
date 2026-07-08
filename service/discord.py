# =============================================================================
# Copyright (C) 2026 Diego Duclos
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

import requests
from logbook import Logger

from service.const import PortEftOptions
from service.port.eft import exportEft
from service.settings import DiscordSettings, NetworkSettings


pyfalog = Logger(__name__)


class DiscordWebhookError(Exception):
    pass


class Discord:

    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Discord()
        return cls._instance

    def __init__(self):
        self.settings = DiscordSettings.getInstance()
        self.networkSettings = NetworkSettings.getInstance()

    def sendFit(self, fit):
        if not self.settings.get('enableDiscord'):
            raise DiscordWebhookError('Discord integration is disabled. Enable it in Preferences > Discord.')

        webhookUrl = (self.settings.get('webhookUrl') or '').strip()
        if not webhookUrl:
            raise DiscordWebhookError('Discord webhook URL is empty. Set it in Preferences > Discord.')

        payload = self._buildWebhookPayload(fit)
        proxies = self.networkSettings.getProxySettingsInRequestsFormat()

        try:
            response = requests.post(webhookUrl, json=payload, proxies=proxies, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            pyfalog.warning('Discord webhook request failed.')
            raise DiscordWebhookError('Failed to send fit to Discord webhook. Check webhook URL and network settings.')

    def _buildWebhookPayload(self, fit):
        shipTypeId = fit.ship.item.ID

        options = {
            PortEftOptions.LOADED_CHARGES: True,
            PortEftOptions.MUTATIONS: True,
            PortEftOptions.IMPLANTS: True,
            PortEftOptions.BOOSTERS: True,
            PortEftOptions.CARGO: True,
        }
        fitText = exportEft(fit, options, callback=None)
        shipTypeLine = 'Ship Type: {}\n'.format(fit.ship.item.typeName)
        maxCodeBlockLen = 4096 - len(shipTypeLine) - 1
        title = 'Pyfa Export'
        description = '{}\n{}'.format(shipTypeLine, self._wrapCodeBlock(fitText, maxCodeBlockLen))

        return {
            'embeds': [
                {
                    'title': title,
                    'description': description,
                    'thumbnail': {
                        'url': self._getShipImageUrl(shipTypeId)
                    }
                }
            ]
        }

    @staticmethod
    def _getShipImageUrl(typeId):
        return 'https://images.evetech.net/types/{}/render?size=64'.format(typeId)

    @staticmethod
    def _wrapCodeBlock(text, maxLength):
        maxContentLength = maxLength - len('```') - len('```')
        if len(text) > maxContentLength:
            text = '{}...'.format(text[:maxContentLength - 3])
        return '```{}\n```'.format(text)
