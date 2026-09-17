from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def fetch_page(url: str):
    server_params = StdioServerParameters(
        command="uvx",
        args=["--system-certs", "mcp-server-fetch"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "fetch",
                {"url": url}
            )

            return result.content[0].text