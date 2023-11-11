from src.app.worker.init import get_faust_app

faust_app = get_faust_app()

topic = faust_app.topic("users")


@faust_app.agent(topic)
async def agent_users(stream):
    async for user in stream:
        print(f"Received user_id: {user_id}")
        user_id = user["id"]
        yield user_id
