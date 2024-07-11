import asyncio

class events:
    def __init__(self):
        self._events = {}

    def event(self, func):
        self.on(func.__name__, func)
        return func

    def on(self, event, listener):
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(listener)

    async def emit(self, event, *args, **kwargs):
        if event in self._events:
            for listener in self._events[event]:
                if asyncio.iscoroutinefunction(listener):
                    await listener(*args, **kwargs)
                else:
                    listener(*args, **kwargs)
