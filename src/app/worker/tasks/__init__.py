# from containers import BrokerContainer
import faust
import asyncio

faust_app = faust.App(
    "worker",
    broker="kafka://localhost:9092",
    autodiscover=True,
    origin="src.app",
    loop=asyncio.get_running_loop(),
    reply_create_topic=True,
)
