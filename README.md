# AI-Powered Product Research Assistant

This application uses AI agents to research and generate comprehensive product reviews. It employs a team of AI agents (a researcher and a writer) managed by a project manager to gather information about products, analyze them, and create detailed review articles.

## Features

- Web-based product research using DuckDuckGo or SerperDev
- Website scraping for detailed product information
- AI-powered analysis and review generation
- Support for local LLM (Ollama) or OpenAI integration
- Customizable search by product type and location (zipcode)

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Ollama (for local LLM) or OpenAI API key
- Optional: SerperDev API key for enhanced search capabilities

## Installation

1. Clone the repository:
```bash
git clone git@github.com:rchow93/prodsearch.git
cd prodsearch
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```env
# Required if using OpenAI
OPENAI_API_KEY=your-openai-api-key

# Optional - for enhanced search capabilities
SERPERDEV_API_KEY=your-serperdev-api-key
```

## Configuration

The application can be configured to use either:
- Local LLM via Ollama (default configuration)
- OpenAI's GPT models (requires API key)

To use Ollama (local LLM):
- Ensure Ollama is installed and running
- update the mode as needed
- update the temperature as needed
- update the num_ctx as needed (tokens)
- Update the base_url in prodreview.py if needed:
```python
llm = ChatOllama(
    base_url="http://your-ollama-server:11434",
    model="ollama run deepseek-r1:32b",
    temperature=0,
    num_ctx=16096,
)
```

To use OpenAI:
- Uncomment the OpenAI configuration section in prodreview.py
- Ensure your API key is set in the .env file

## Usage

1. Run the script with your desired product search:
```python
if __name__ == "__main__":
    subject = "Your Product Category"  # e.g., "Top Loading Washers that are exactly 4.3 cubic feet capacity"
    zipcode = "Your Zipcode"  # e.g., "94121"
    crew = create_crew(subject, zipcode)
    result = crew.kickoff()
```

2. Execute the script:
```bash
python prodreview.py
```

## Example Output

Here’s a comprehensive guide to the top gaming laptops of 2025, ranked by cost, reviews, and recommendations:

```markdown
# Top Gaming Laptops of 2025
In the world of gaming laptops, choosing the right machine can greatly affect your experience. Whether you're a casual player or a competitive gamer, having a reliable and powerful laptop is essential.

## 1. Lenovo Legion Pro 5i Gen 9
- **Specs:**  
  - Processor: Intel Core i7-14650HX  
  - RAM: 16 GB  
  - Graphics: Nvidia GeForce RTX 4060  
  - Storage: 512 GB SSD  
  - Display: 16 inches, 2560 x 1600, 165 Hz  
- **Pros:** Excellent sustained performance, long battery life. 
- **Cons:** Limited color gamut, chunky design.  
- **Review:** A great value for average gamers, delivering decent midrange performance at a reasonable price.

## 2. MSI Titan 18 HX
- **Specs:**  
  - Processor: Intel Core i9-14900HX  
  - RAM: 128 GB  
  - Graphics: Nvidia GeForce RTX 4090  
  - Storage: 4 TB SSD  
  - Display: 18 inches, 3840 x 2400, 120 Hz  
- **Pros:** Unmatched performance, 4K display.  
- **Cons:** Extremely expensive, heavy.  
- **Review:** The top choice for serious gamers wanting maximum performance, albeit at a high cost.
```

See the example outputs in `Top_Gaming_Laptops_2025_Article.txt`.

## Dependencies

Key libraries used in this project:
- crewai: Core framework for AI agent coordination
- langchain: For LLM interactions and tools
- python-dotenv: Environment variable management
- beautifulsoup4: Web scraping support
- requests: HTTP requests handling

Full dependencies are listed in `requirements.txt`.

## Contributing

Feel free to submit issues and pull requests.

## License

Apache License 2.0

```
Copyright 2024 Richard Chow (askqai@mitns.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

For the full license text, see the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Notes

- The quality and accuracy of results may vary depending on the LLM model used
- Web search results depend on the search tool used (DuckDuckGo or SerperDev)
- Processing time may vary based on the complexity of the search and the LLM model used