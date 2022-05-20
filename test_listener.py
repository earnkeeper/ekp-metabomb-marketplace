import asyncio

from listener.listener_container import ListenerContainer

if __name__ == '__main__':
    container = ListenerContainer()

    print("🚀 Application Start")

    asyncio.run(container.listener_service.test())
