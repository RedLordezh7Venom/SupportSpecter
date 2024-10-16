from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm=ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def querie_generator(sector, field, experience):
    prompt = (
        "Pretend that you are a senior in the customer service sector of a large company in {sector}. "
        "You are tasked with training new employees to become familiar with customer issues. "
        "Consider their field of expertise: {field}, and their experience level: {experience}. "
        "Generate one realistic customer complaint situation for the employee to tackle. "
        "Ensure the situation reflects different sentiments without explicitly stating them, allowing the employee to identify the emotions involved. "
        "Do not include tips or additional information."
    )

    # Insert the field and experience into the prompt
    formatted_prompt = prompt.format(sector=sector, field=field, experience=experience)

    # Create a message object for the LLM
    message = HumanMessage(content=formatted_prompt)

    # Get the response from the LLM
    response = llm.invoke([message])

    # Extract and clean the generated text
    generated_text = response.content.strip()

    # Return the generated situation directly
    return generated_text

def response_evaluation(query, employee_response):
    """
    Evaluates the employee's response against a generated customer complaint situation.

    Parameters:
    - query (str): The customer complaint situation generated by the querie_generator function.
    - employee_response (str): The response provided by the employee to the complaint.

    Returns:
    - A dictionary with scores and detailed feedback for each evaluation criterion.
    """


    prompt = (
        f"Evaluate the following employee response for handling a customer complaint:\n\n"
        f"Customer Complaint: '{query}'\n\n"
        f"Employee Response: '{employee_response}'\n\n"
        "Assess the response based on the following criteria:\n"
        "1. Correct Identification of the Customer's Issue\n"
        "2. Quality of Proposed Solution\n"
        "3. Likelihood of Customer Satisfaction\n"
        "4. Adherence to Company Policy\n"
        "Provide a score (out of 100) and detailed feedback for each criterion."
        "also provide the best response to the query which u think will be the best evaluating the sentiments and everything"
    )


    message = HumanMessage(content=prompt)


    response = llm.invoke([message])


    evaluation_results = response.content.strip()


    return evaluation_results

if __name__ == '__main__':
    query = querie_generator("retail","electronics", "experienced")
    print(query)
    employee_response = "I understand your frustration with the laptop issue. I will escalate this to our technical team and ensure it gets resolved quickly."
    evaluation_results = response_evaluation(query, employee_response)
    print(evaluation_results)
