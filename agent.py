import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from mcp_client import fetch_page


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


NEWS_SOURCES = [
    "https://openai.com/news/",
    "https://www.anthropic.com/news",
    "https://blog.google/technology/ai/",
]


def get_fetch_tool():

    return types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="fetch",
                description="Fetch the content of a web page from a URL.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "url": types.Schema(
                            type="STRING",
                            description="The URL of the web page to fetch."
                        )
                    },
                    required=["url"]
                )
            )
        ]
    )


async def ask_agent(question: str):

    activity = []
    retrieved_content = []

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[get_fetch_tool()]
        )
    )

    if response.function_calls:

        for function_call in response.function_calls:

            if function_call.name == "fetch":

                url = function_call.args["url"]

                activity.append("🤖 Agent decided to use Fetch")
                activity.append("🔧 Calling MCP Fetch Server")
                activity.append(f"🌐 Fetching: {url}")

                content = await fetch_page(url)

                retrieved_content.append(
                    f"Source: {url}\n\n{content}"
                )

                activity.append("✓ Content retrieved from MCP")

    else:

        activity.append("🤖 Agent answered directly")
        activity.append("✓ MCP was not required")

    if retrieved_content:

        sources_content = "\n\n---\n\n".join(retrieved_content)

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                f"""
                You are an AI News Agent.

                The user asked:

                {question}

                Below is information retrieved from AI news sources
                using the MCP Fetch tool.

                {sources_content}

                Based only on the retrieved information:

                1. Summarize the most relevant AI developments.
                2. Keep the answer concise and clear.
                3. Group related developments when appropriate.
                4. Mention the source for each development.
                5. Do not invent information.
                """
            ]
        )

        activity.append("📝 Agent generated final response")

    return response.text, activity