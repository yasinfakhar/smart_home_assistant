import uuid
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from iot_functions import get_iot_functions

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

tools = get_iot_functions()

# prompt = hub.pull("hwchase17/openai-functions-agent")

system_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant")
human_message = HumanMessagePromptTemplate.from_template("{input}")
chat_history_placeholder = MessagesPlaceholder(variable_name="chat_history")
agent_scratchpad = MessagesPlaceholder(variable_name="agent_scratchpad")

prompt = ChatPromptTemplate.from_messages([
    system_message,
    chat_history_placeholder,
    human_message,
    agent_scratchpad,
])

agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

memory = ChatMessageHistory(session_id=uuid.uuid4())

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

while True:
    user_input = input('prompt: ')
    if user_input == "q":
        exit(0)
    else:
        result = agent_with_chat_history.invoke({"input": user_input},
                                                config={"configurable": {"session_id": "_"}},)
        print(result)
