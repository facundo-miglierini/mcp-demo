import streamlit as st
import time

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from tavily_client import agent

st.title("MCP agent")

if "messages" not in st.session_state:
    # default initial message to render in message state
    st.session_state["messages"] = [AIMessage("¿En qué puedo ayudarte?")]

# Loop through all messages in the session state and render them as a chat on every st.refresh mech
for msg in st.session_state.messages:
    # https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
    # we store them as AIMessage and HumanMessage as its easier to send to LangGraph
    if type(msg) == AIMessage:
        st.chat_message("assistant").write(msg.content)

    if type(msg) == HumanMessage:
        st.chat_message("user").write(msg.content)

async def run():
    if prompt := st.chat_input():
        user_prompt = HumanMessage(content=prompt)
        st.session_state.messages.append(user_prompt)
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = await agent.invoke(prompt, [st_callback], "1")

            message_placeholder = st.empty()
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            st.session_state.messages.append(AIMessage(content=response))



if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
