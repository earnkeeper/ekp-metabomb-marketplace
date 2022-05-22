import asyncio

from listener.listener_container import ListenerContainer

if __name__ == '__main__':
    container = ListenerContainer()

    async def test():
        example = {
            'address': '0x05f0d89931eb06d4596af209de4a9779cef73cde',
            'topics': ['0x27bae1fb91b142a2956e7482d5370a469a66deae9cc45d8b0ec35067a54a18ad',
                       '0x0000000000000000000000000000000000000000000000000000000000000622',
                       ],
            'data':
            '0x00000000000000000000000000000000000000000000017b6aa309b56efc0000',
            'blockNumber': 18025884,
            'transactionHash': '0x03f474e85c2bd6544d9e183a0c589f47e0437f60cdd276d6261214c7d178b973',
            'transactionIndex': 45,
            'blockHash': '0x2b6d3df7b0e0ce5d46814a684ad3a54a2bbf719cca6f2e272ae88ab3143aabf9',
            'logIndex': 203,
            'removed': False
        }

        listing = await container.listener_service.decode_market_listing(example)
        await container.notification_service.send_notification(listing, None)
        print(listing)
        
    asyncio.run(test())
