from googletrans import Translator
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
from langchain_google_genai import ChatGoogleGenerativeAI

#configure LLM
llm=ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

#Configure conversation history
conversation_history=[]
def add_to_convo(user_input,bot_response):
  conversation_history.append(f"User:{user_input}")
  conversation_history.append(f"Bot:{bot_response}")

def save():
  df = pd.DataFrame(conversation_history, columns=['Conversation']) # Changed to one column to match data shape
  df.to_csv('conversation_history.csv', index=False)

def sentiment_analyzer(text):
  prompt = f"Analyze the text of this complaint or feedback given: '{text}'. Just give the tone and other observations:"
  message=HumanMessage(content=prompt)
  response=llm.invoke([message])
  return response.content

translator=Translator()
def chatbot(input_text,output_language):
    message = HumanMessage(
        content=f"you are a chatbot for an e commerce website equivalent to amazon or flipkart. the user is giving you {input_text}...derive the sentiments from sentiment_analyzer({input_text}) and generate a good respone or a humanly respone so as to mantian the interest...prioritize accordingly to the sentiments. ask for any further information required by the user and save the previous information. do not print the sentiment analysis,just print the response....and take inspiration from order tracking of amazon. also consider a feature that a customer can change his delivery time or payment method using chatbot but verify the customer first" # Call sentiment_analyzer function with input_text
    )
    response = llm.invoke([message])
    translated_response=response.content
    translated_response = translator.translate(translated_response, dest=output_language).text
    print(f"Chatbot: {translated_response}")
    add_to_convo(input_text,response.content)
    save()
    return translated_response

def feedback_analysis(input_text, organization_type):
    sentiment = sentiment_analyzer(input_text)


    message_content = (
        f"You are a customer service chatbot for a multimillion-dollar {organization_type}. "
        f"The following text is from a customer: '{input_text}'. "
        f"Analyze it to understand the emotions (detected sentiment: {sentiment}). "
        f"Based on this, provide personalized advice points for the customer service agent. "
        f"Focus on what actions can be taken to address the feedback and areas to improve upon."
        f"if its a complaint,categorize the {input_text} into the type of problem it is and tell the customer service agent to contanct the appropriate people"
    )


    message = HumanMessage(content=message_content)
    response = llm.invoke([message])

    print("Personalized advice for customer service agent:")
    return response.content


#Summarize

def summarize(adress):
  conversation_data=pd.read_csv(f"{adress}")
  conversation_text = ""
  for index, row in conversation_data.iterrows():
        # Access the conversation from the 'Conversation' column and split into user and bot parts
        parts = row['Conversation'].split(':')
        if len(parts) >= 2:  # Make sure there's at least a user and bot part
          user_part = parts[0]
          bot_part = parts[1]
          conversation_text += f"{user_part}: {bot_part} \n\n"
  prompt = f"""
  The issue that the customer had couldn't be solved using the chatbot,
  and now the customer service agent has to come into play.
  Summarize the chats done by the customer and chatbot. Here is the conversation:
  {conversation_text}
  """

  message = HumanMessage(content=prompt)
  response = llm.invoke([message])
  return response.content

if __name__ == "__main__":
    summary = summarize('conversation_history.csv')
    print(summary)
    resp1 = chatbot("मुझे प्राप्त ऑर्डर पूरी तरह से खराब गुणवत्ता का है, मैं इस सेवा से बहुत निराश हूं और अपना ऑर्डर वापस करना चाहता हूं, इसके लिए चरण बताएं","spanish")
    print(sentiment_analyzer("I absolutely love the new headphones! The sound quality is amazing and they're so comfortable to wear."))