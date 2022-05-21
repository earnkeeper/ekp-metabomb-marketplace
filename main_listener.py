from listener.listener_container import ListenerContainer

if __name__ == '__main__':
    container = ListenerContainer()

    print("🚀 Application Start")

    container.listener_service.listen()
