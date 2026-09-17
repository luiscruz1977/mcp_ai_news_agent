import asyncio
from mcp_client import fetch_page

async def main():
    url = "https://openai.com/news"
    #url = "https://www.anthropic.com/news"

    result = await fetch_page(url)

    print(result)

if __name__ == "__main__":
    asyncio.run(main())