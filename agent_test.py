import asyncio
from agent import ask_agent

async def main():
    question = """
        What is the latest information available on 
        https://www.openai.com/news/
        """

    answer = await ask_agent(question)

    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    asyncio.run(main())