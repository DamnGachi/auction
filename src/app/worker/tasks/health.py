from . import faust_app

topic = faust_app.topic("health")


@faust_app.agent(topic)
async def health_check(stream):
    async for value in stream:
        yield value
