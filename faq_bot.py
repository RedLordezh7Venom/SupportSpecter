from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm=ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)
from langchain_google_genai import ChatGoogleGenerativeAI

faq_prompt = """
You are an AI assistant. Here is a frequently asked question (FAQ) and the relevant knowledge base of your company.
Provide an accurate, concise, and contextual response.

FAQ: {question}
Knowledge Base: {knowledge_base}

Response:
"""


#example
knowledge_base="""
1.You can create an account by signing up using your email address, phone number, or by linking your Google or Facebook account.
2.To reset your password, go to the login page and click on “Forgot Password.” You will receive a password reset link via email or SMS
3.You can update your profile information by going to the “Profile” section in the app or website. Click on “Edit Profile” to change your details like name, phone number, or address.
4.To place an order, log in to your account, search for a restaurant, add items to your cart, and proceed to checkout by selecting the preferred payment method.
5.Yes, you can schedule an order for a later time by selecting the “Schedule Order” option at checkout and choosing the preferred delivery time.
6.If you receive an incorrect order or any items are missing, go to the “Orders” section and click on the respective order to report an issue. You can also contact customer support directly.
7.We accept various payment methods, including credit cards, debit cards, digital wallets (PayPal, Google Pay), and cash on delivery.
8.You can apply a promo code during checkout. Look for the “Apply Promo Code” section and enter your code to receive the discount.
9.Refunds are processed within 5-7 business days after the order is canceled. Depending on your payment method, it may take longer for the amount to reflect in your account.
10.If no one is available to receive the order, the delivery person will attempt to contact you. If the order cannot be delivered, it may be canceled, and any refund will be processed as per the cancellation policy"""

def generate_faq_response(question, knowledge_base = knowledge_base):
    prompt = faq_prompt.format(question=question, knowledge_base=knowledge_base)
    response = llm.invoke(prompt)
    print(response.content)
    return response.content

if __name__ == "__main__":
    question = "How do I cancel my order"
    response = generate_faq_response(question, knowledge_base)
    question = "What is your return policy?"
    response = generate_faq_response(question, knowledge_base)


