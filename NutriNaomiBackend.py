from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

# Initialize the chatbot
chat = ChatOllama(model="dolphin-llama3:8b")

# Initialize chat history
chat_history = ChatMessageHistory()
human_history = ChatMessageHistory()

# Add initial message from bot
initial_message = "Hello! I'm Naomi, I help dietitians collect information. Is it ok if I record our conversation and share it with your dietitian? Your answers will not be shared with third-parties."
chat_history.add_ai_message(initial_message)
print("\n")
print("Naomi: " + initial_message)
# Get user consent
user_input = input("You: ")
chat_history.add_user_message(user_input)
human_history.add_user_message(user_input)

# Define the privacy checking prompt
prompt_privacy= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'You are checking to see if the user consented to their data being collected and saved. If they did, answer "User consented". Else, answer "Without consent, we cannot continue our conversation. Please restart if you changed your mind.". Do not respond with any other words.',
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Check for consent
chain = prompt_privacy | chat
response = chain.invoke({"messages": chat_history.messages})
if "user consented" in response.content.lower(): 
    # Continue the script
    
    # Topics of questions for information to be collected
    fields = [
        {"name": "full name"},
        {"name": "age in years"},
        {"name": "medical conditions"},
        {"name": "height in cm"},
        {"name": "weight in kg"},
        {"name": "breakfast"},
        {"name": "lunch"},
        {"name": "dinner"},
        {"name": "snacks"},
    ]
    topic_number = 0

    # For loop to ask the information
    for field in fields:
        topic_number = topic_number + 1
        follow_up_prompt = ""
        while True:
            
            # Define the question asking prompt with a variable to feed the question topic
            topic = field['name']
            prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are Naomi, you ask questions to new clients and you help dietitians collect information by asking the new clients about {len(fields)} different topics. You are currently on number {topic_number}: {topic}. Ask no more than one question at a time. {follow_up_prompt}"
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
            )
            # Prompt LLM
            chain = prompt | chat
            response = chain.invoke({"messages": chat_history.messages})
            chat_history.add_ai_message(response.content)
            ## print(f"Current prompt: {prompt}")
            print("\n")
            print("Naomi: " + response.content)
            # Prompt User
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            chat_history.add_user_message(user_input)
            human_history.add_user_message(user_input)
            if user_input.lower() == "next topic": # User can force next topic for testing purposes
                break
            # Decide to stay on topic or move on
            # Define a rating prompt for the current topic
            rating_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f'Your job is to rate the conversation another AI is having with a user. The goal is to help dietitians collect information about their clients. Determine if the chat history contains enough information about ONLY the current topic: {topic} . Answer "Sufficient: yes." if so, followed by why it is sufficient for this topic. Else, explain what should be asked to the user to get the missing information. The conversation AI will receive this instruction.'
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
            )
            chain = rating_prompt | chat
            rating = chain.invoke({"messages": human_history.messages})
            ## print(human_history.messages)
            print("\n")
            print(f'--System message-- Rating: {rating.content} ----')

            if "sufficient: yes" in rating.content.lower(): 
                ## print("Answer found to be sufficient.")

                # Summarize full chat history
                summary_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        f'Your job is to summarize the information provided by the user about ONLY the current topic: {topic}. Sum up the facts given by the user as your response. There is no need for any extra explaination or information.'
                    ),
                    MessagesPlaceholder(variable_name="messages"),
                ]
                )
                chain = summary_prompt | chat
                summary = chain.invoke({"messages": human_history.messages})
                # Save the summary to the fields list
                field['summary'] = summary.content
                print("\n")
                print(f'--System message-- Input summary: {field['summary']} ----')

                # reset human_history chat history
                human_history = ChatMessageHistory()

                # exit current while loop and move on to next topic
                break

            # Else add the follow up prompt information to the system prompt
            follow_up_prompt = rating.content

    # Continue as while loop indefinitely
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        chat_history.add_user_message(user_input)
        human_history.add_user_message(user_input)
        chain = prompt | chat
        response = chain.invoke({"messages": chat_history.messages})
        chat_history.add_ai_message(response.content)
        print("\n")
        print("Naomi: " + response.content)

else:
    print("\n")
    print("Naomi: " + response.content)
