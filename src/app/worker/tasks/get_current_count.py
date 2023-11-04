from src.app.worker.init import get_faust_app
from src.app.worker.tables.count_table import count_table

faust_app = get_faust_app()

topic = faust_app.topic("get_current_count")


@faust_app.agent(topic)
async def agent(stream):
    async for _ in stream:
        print(_)
        yield count_table["count"]
