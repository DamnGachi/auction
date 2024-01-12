from . import faust_app

topic = faust_app.topic("users")


@faust_app.agent(topic)
async def agent_users(stream):
    async for user in stream:
        user_id = user["id"]
        yield user_id
