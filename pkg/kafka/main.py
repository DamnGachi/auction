import faust

app = faust.App(
    "main",
    broker="kafka://localhost:9092",
    value_serializer="raw",
    broker_max_poll_records=1000,
)

greetings_topic = app.topic("greetings")


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)
