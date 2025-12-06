from langchain_ollama import ChatOllama
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_core.messages import HumanMessage, SystemMessage

# Load stock data using UnstructuredExcelLoader
print("Loading stock data from 3m.xlsx using UnstructuredExcelLoader...")
loader = UnstructuredExcelLoader("./3m.xlsx", mode="elements")
docs = loader.load()

# formatted_content = "\n\n".join([doc.page_content for doc in docs])
# formatted_content = docs[0].page_content
formatted_content = ""
for doc in docs:
    formatted_content += doc.page_content + "\n"

print(f"Loaded {len(docs)} elements from Excel.")

# Initialize the Ollama model
print("Initializing Ollama stocker model...")
model = ChatOllama(
    model="stocker:latest",
    temperature=0.1,
    seed=42,
    max_tokens=2000,
    top_p=0.9,
    top_k=10,
)

# System message defining the model's role
system_message = SystemMessage(
    content="""You are a stock market analyst who analyzes company data from screener 
    and provides investment recommendations. Based on the data provided, you should:
    1. Analyze the financial metrics and trends
    2. Determine if this is a good investment opportunity
    3. If yes, suggest when to enter and when to take an exit
    4. Provide clear reasoning for your recommendation"""
)

# User question with the stock data
user_question = f"""Here is the stock market data for analysis:

{formatted_content}

Based on this data, please analyze and tell me:
1. Should I invest in this stock?
2. If yes, what is the recommended entry point?
3. When should I take an exit (target price or time horizon)?
4. What are the key factors supporting your recommendation?"""

# Prepare messages
messages = [
    system_message,
    HumanMessage(content=user_question)
]

# Get the model's response
print("\nAnalyzing stock data...\n")
print("="*80)
result = model.invoke(messages)
print(result.content)
print("="*80)
