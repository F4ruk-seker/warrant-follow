from discord_logger import DiscordLogger
import os

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
options = {
    "application_name": "Finance Tracking",
    "service_name": "Finance API",
    # "service_icon_url": "your icon url",
    "service_environment": "Production",
    "display_hostname": True,
    "default_level": "info",
}

logger = DiscordLogger(webhook_url=WEBHOOK_URL, **options)


