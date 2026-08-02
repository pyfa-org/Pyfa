# Add root folder to python paths
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from service.discord import Discord
from service.settings import DiscordSettings


def test_discord_webhook_url_validation_accepts_valid_discord_url():
    assert Discord.isValidWebhookUrl('https://discord.com/api/webhooks/123456/token-value')


def test_discord_webhook_url_validation_rejects_invalid_urls():
    assert not Discord.isValidWebhookUrl('')
    assert not Discord.isValidWebhookUrl('http://discord.com/api/webhooks/123456/token-value')
    assert not Discord.isValidWebhookUrl('https://example.com/api/webhooks/123456/token-value')
    assert not Discord.isValidWebhookUrl('https://discord.com/api/webhooks/123456')


def test_discord_settings_get_redacted_masks_webhook_url():
    dsettings = DiscordSettings.__new__(DiscordSettings)
    dsettings.settings = {
        'enableDiscord': True,
        'webhookUrl': 'https://discord.com/api/webhooks/123456/token-value',
        'confirmBeforeSend': True
    }

    redacted = dsettings.getRedacted()

    assert redacted['enableDiscord'] is True
    assert redacted['webhookUrl'] == '<redacted>'
    assert redacted['confirmBeforeSend'] is True
