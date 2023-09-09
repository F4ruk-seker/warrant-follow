import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(
        headless=True,
        args=['--no-sandbox'],
        autoClose=False
    )
    page = await browser.newPage()
    await page.goto('https://borsa.doviz.com/hisseler')
    cdp = await page.target.createCDPSession()
    await cdp.send('Network.enable')
    await cdp.send('Page.enable')

    def printResponse(response):
        print(response)

    cdp.on('Network.webSocketFrameReceived', printResponse)  # Calls printResponse when a websocket is received
    cdp.on('Network.webSocketFrameSent', printResponse)  # Calls printResponse when a websocket is sent
    await asyncio.sleep(100)


asyncio.get_event_loop().run_until_complete(main())

