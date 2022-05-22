import asyncio

from listener.listener_container import ListenerContainer

if __name__ == '__main__':
    container = ListenerContainer()

    async def hero_test():
        example = {
            'address': '0x05f0d89931eb06d4596af209de4a9779cef73cde',
            'topics': [
                '0x27bae1fb91b142a2956e7482d5370a469a66deae9cc45d8b0ec35067a54a18ad',
                '0x0000000000000000000000000000000000000000000000000000000000000622',
            ],
            'data':
            '0x00000000000000000000000000000000000000000000007b6aa309b56efc0000',
            'blockNumber': 18025884,
            'transactionHash': '0x03f474e85c2bd6544d9e183a0c589f47e0437f60cdd276d6261214c7d178b973',
            'transactionIndex': 45,
            'logIndex': 203,
            'removed': False
        }

        listing = await container.listener_service.decode_market_listing(example)
        await container.listener_service.process_market_listing(listing)

    async def box_test():
        example = {
            'address': '0x2076626437c3Bb9273998A5E4F96438aBE467F1C',
            'topics': [
                '0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0',
                '0x00000000000000000000000000000000000000000000000000000000000000a4',
                '0x000000000000000000000000553a463f365c74eda00b7e5aaf080b066d4ca03c'
            ],
            'data':
            '0x00000000000000000000000000000000000000000000003c33c1937564800000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000084d5442482d505245000000000000000000000000000000000000000000000000',
            'blockNumber': 17937471,
            'transactionHash': '0xe4896e51f2508f1b817ea1e5a179e3cee61bdc2104f469443822db8cd75cb1ec',
            'transactionIndex': 45,
            'logIndex': 203,
            'removed': False
        }

        listing = await container.listener_service.decode_market_listing(example)
        await container.listener_service.process_market_listing(listing)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(hero_test())
    loop.run_until_complete(box_test())
