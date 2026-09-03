from langgraph.graph import StateGraph
from langgraph.constants import START, END
from langchain_openai import AzureChatOpenAI
from typing import TypedDict
from save_chat import save_chat
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

def create_outline(state: BlogState) -> BlogState:
    title = state['title']

    prompt = f'Create an outline for a blog post titled: {title}'

    outline = azure_client.invoke(prompt).content

    save_chat(
        user_message=prompt,
        assistant_message=outline,
        response_type="Outline"
    )

    state['outline'] = outline
    return state

def create_blog(state: BlogState) -> BlogState:
    title = state['title']
    outline = state['outline']

    prompt = f'Write a blog post titled "{title}" based on the following outline:\n{outline}'

    content = azure_client.invoke(prompt).content

    save_chat(
        user_message=prompt,
        assistant_message=content,
        response_type="Blog"
    )

    state['content'] = content
    return state

class BlogState(TypedDict):
    title: str
    outline: str
    content: str

graph = StateGraph(BlogState)

graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

workflow = graph.compile()

initial_state = {"title": "Janmashtami: The Birth of Lord Krishna", "outline": "", "content": ""}
final_state = workflow.invoke(initial_state)
print(final_state['outline'])  # Should print the generated outline for the blog post.
print(final_state['content'])  # Should print the generated content for the blog post.
