from langgraph.graph import StateGraph
from langgraph.constants import START, END
from langchain_openai import AzureChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

azure_client = AzureChatOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
    azure_deployment=deployment,
    model_name=deployment,
)

def llm_qa(state: LLMState) -> LLMState:
    question = state['question']

    prompt = f'Answer the following question: {question}'

    answer = azure_client.invoke(prompt).content

    state['answer'] = answer
    return state


class LLMState(TypedDict):
    question: str
    answer: str


graph = StateGraph(LLMState)

graph.add_node('llm_qa', llm_qa)

graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

workflow = graph.compile()

initial_state = {"question": "What is the capital of France?", "answer": ""}
final_state = workflow.invoke(initial_state)
print(final_state['answer'])  # Should print "The capital of France is Paris."
