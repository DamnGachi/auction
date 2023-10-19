import logging

LOG_FILENAME = "app.log"

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILENAME, encoding="utf-8", mode="w")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Привязка форматтера к обработчику
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Привязка обработчика к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)