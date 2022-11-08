from pathlib import Path

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

REDIS_IP = env.str("REDIS_IP")

QIWI_TOKEN = env.str("QIWI_TOKEN")
QIWI_WALLET = env.str("QIWI_WALLET")

# SERVER_IP = env.str("IP_SERVER")
# TOKEN = env.str("TOKEN")
# REDIS_IP = env.str("REDIS_IP")

# webhook settings
WEBHOOK_HOST = "https://observercrypto.me"
WEBHOOK_PORT = 8443
WEBHOOK_PATH = f"/bot"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 3001

# WEBHOOK_SSL_CERT = "webhook_cert.pem"
# WEBHOOK_SSL_PRIV = "webhook_pkey.pem"

I18N_DOMAIN = 'crypto_bot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
