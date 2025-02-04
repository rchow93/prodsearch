import os
import dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool, FileReadTool, ScrapeWebsiteTool, SerperDevTool
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool  # Only importing 'tool' since BaseTool isn't used
import contextlib  # Optional - used only for error suppression in search_tool
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()
SERPERDEV_API_KEY = os.getenv("SERPERDEV_API_KEY") #serper search tool - get api key from serperdev.com otherwise use the duckduckgo search tool
openai_api_key = os.getenv("OPENAI_API_KEY") #openai llm access - get api key from openai.com if not using local llm (ollama/lm studio)
ollama_base = os.getenv("OLLAMA_BASE_URL") #ollama base url - get the base url for the ollama model

# Get current date - I'll use this to find the year for the product search query - otherwise it may default to the LLM trained fixed data.
now = datetime.now()
human_readable_date = now.strftime("%Y")

# Initialize tools
file_writer_tool = FileWriterTool() #file writer tool - this would be needed if wanted to write this to a file.
file_read_tool = FileReadTool() #file read tool - this would be needed if you wanted to read from a file.
websearch = SerperDevTool()  #use this tool if you have a serperdev api key, otherwise use the duckduckgo search tool
scrape_tool = ScrapeWebsiteTool() #allow agents to scrape a website for information

# Initialize LLM - local llm model using ollama
llm = LLM(
    model="ollama/deepseek-r1:1.5b",
    base_url=f"{ollama_base}",
    #provider="ollama"  # Specify the provider
)

'''
# Required: Your API key for authentication
OPENAI_API_KEY=<your-api-key>

# Optional: Default model selection
OPENAI_MODEL_NAME=gpt-4o-mini  # Default if not set

# Optional: Organization ID (if applicable)
OPENAI_ORGANIZATION_ID=<your-org-id>

llm = LLM(
    model="gpt-4",
    max_tokens=4000,  # Limit response length
)
'''

@tool("DuckDuckGoSearch")
def search_tool(search_query: str):
    """Search the web for information on a given topic."""
    with contextlib.suppress(Exception):
        return DuckDuckGoSearchRun().run(search_query)
    return "Search failed. Please try again."

def create_crew(subject, zipcode):
    researcher = Agent(
        role='Senior Consumer Product Researcher',
        goal=f""" You've been tasked with using the web search for product reviews for {subject} products.
        The customer is dependant on your expertise to find the best products available near {zipcode} or with free shipping.
        This is for {human_readable_date} so need to find the best products still available. 
        Deliver a comprehensive list of the top products, their specifications, prices, reviews, availability, and pros/cons.""",
        backstory=f"A smart, experienced, and caring professional expert product researcher who specializes in {subject}.",
        verbose=True,
        allow_delegation=True,
        max_iter=50,
        llm=llm,
        tools=[search_tool, scrape_tool],
    )

    writer = Agent(
        role='Senior Product Review Writer',
        goal=f""" The team has been tasked on researching, collecting, and analyzing the data on the top {subject} products.
        You will write a professional article based on the researcher's findings. The article should include rankings by cost, reviews, and recommendations.
        The style should be clear, concise, and informative, with a clear conclusion and recommendations.
        It should best effort contain the top 10 product analysis and recommendations. This should be in the style of something
        in a consumers report or similar professional product review publication.""",
        backstory=f"""Expert content writer specializing in consumer product reviews. "
                  Passionate about {subject} products and dedicated to providing accurate and detailed information.""",
        verbose=True,
        allow_delegation=True,
        max_iter=50,
        llm=llm,
        tools=[file_read_tool, file_writer_tool]
    )

    manager = Agent(
        role="Project Manager",
        goal=f"""Efficiently manage the crew and ensure high-quality task completion on making recommendations on purchasing {subject}. "
             Best effort to try compile a comprehensive list of at least 10 products researched and written about to give consumers more choice.""",
        backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
        allow_delegation=True,
        llm=llm,
    )

    task1 = Task(
        description=f"""Research Task:
            1. When searching, use exactly this format for the search tool:
               {{"search_query": "search terms here"}}

               For example, to search for washers:
               {{"search_query": "best {subject} {human_readable_date}"}}

            2. For the top 20 {subject} products found:
               - Get product specifications
               - Compare prices
               - Analyze reviews/ratings
               - Check availability
               - List pros/cons
               - Capture the most insightful product reviews

            3. Rank products and write brief reviews

            4. Present findings in clear text format for the writer.

            IMPORTANT: When using the search tool, always use the exact format shown above with 
            "search_query" as the key. Do not use "description" or other keys.""",
        expected_output="Detailed analysis report with rankings and reviews",
        agent=researcher
    )

    task2 = Task(
        description=f"""Writing Task:
            Create a comprehensive article on the top {subject} products including:
            1. Rankings by cost, reviews, and recommendations
            2. Product details: model, specs, pros/cons, pricing, availability
            3. Clear conclusion and recommendations""",
        expected_output=f"Professional article about top {subject} products",
        agent=writer
    )

    return Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        manager_agent=manager,
        manager_llm=llm,
        process=Process.hierarchical,
        verbose=True,
    )


# Main execution
if __name__ == "__main__":
    subject = "12 cup coffee makers"
    zipcode = "94105"
    crew = create_crew(subject, zipcode)
    result = crew.kickoff()

    print("-----------------------------")
    print(result)
