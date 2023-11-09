from src.app.worker.init import get_faust_app
from src.app.worker.tables.count_table import count_table

faust_app = get_faust_app()

topic = faust_app.topic("balance-history")