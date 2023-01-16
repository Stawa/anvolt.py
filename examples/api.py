from anvolt import AnVoltClient

client = AnVoltClient()


def simple_example() -> None:
    bite = client.sfw.bite()
    return bite.url, bite.original_response


print(simple_example())


def example_produce(produce: int) -> list:
    hug = client.sfw.hug(produce=produce)
    return hug.url  # Return list if produce


print(example_produce(produce=5))
