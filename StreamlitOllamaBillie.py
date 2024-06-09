import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

# Initialize the chatbot
chat = ChatOllama(model="llama2-uncensored")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

    # Add initial message from bot
    st.session_state.chat_history.add_ai_message("Hello! I'm Billie, the customer service assistant bot of webstore 'Bol.com'. How can I assist you today?")

# Define the chat prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are Billie, the customer service assistant bot of webstore 'Bol.com'. Answer all questions to the best of your ability. If the customer asks about package information, you are allowed to make up information.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat

# Streamlit app
st.title("Chatbot Billie")

# Define CSS styles
css = """
<style>
.message-container {
    display: flex;
    padding: 10px;   
    flex-direction: column;
}

.user-message {
    align-self: flex-end;
    background-color: hsl(236, 100%, 85%);
    color: black;
    border-radius: 15px;
    padding: 8px 12px;
    margin: 5px;
    max-width: 70%;
    word-wrap: break-word;
    text-align: right;
}

.bot-message {
    display: flex; /* Added to align items */
    align-items: flex-start; /* Align items to the start (top) */
    background-color: hsl(240, 100%, 32%);
    color: white;
    border-radius: 15px;
    padding: 8px 12px;
    margin: 5px;
    max-width: 70%;
    word-wrap: break-word;
}

.bot-message img {
    width: 40px; /* Adjust image width */
    height: 40px; /* Adjust image height */
    margin-right: 10px; /* Add margin for spacing */
}
</style>
"""

st.write(css, unsafe_allow_html=True)

message_container = st.empty()

with st.form(key='chat_form'):
    user_input = st.text_input("Talk to Billie:")
    if st.form_submit_button("Send"):
        if user_input == "exit":
            st.stop()
        st.session_state.chat_history.add_user_message(user_input)
        response = chain.invoke({"messages": st.session_state.chat_history.messages})
        st.session_state.chat_history.add_ai_message(response.content)

# Display chat history
messages_html = ""
for msg in st.session_state.chat_history.messages:
    if isinstance(msg, HumanMessage):
        messages_html += f'<div class="message-container"><div class="user-message">{msg.content}</div></div>'
    elif isinstance(msg, SystemMessage):  # Add condition for SystemMessage
        messages_html += f'<div class="message-container"><div class="bot-message">{msg.content}</div></div>'
    else:
        messages_html += f'<div class="message-container"><div class="bot-message"><img src="https://assets.s-bol.com/nl/static/assets/images/billie/billie_1000x1000.png">{msg.content}</div></div>'
message_container.write(messages_html, unsafe_allow_html=True)
