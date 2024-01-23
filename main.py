# Import Necessary Libraries:
import streamlit as st
from langchain_community.document_transformers import DoctranPropertyExtractor
from langchain.schema import Document
import os
from langchain.document_transformers import DoctranPropertyExtractor
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import openai
import json
import time

from trello import TrelloClient
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Create a Trello API instance
client = TrelloClient(api_key=os.getenv('api'), token=os.getenv('token'),api_secret=os.getenv('secret'))

# OpenAI API
openai.api_key = os.getenv('API_KEY')
os.environ['OPENAI_API_KEY'] = openai.api_key



# This function will extract features from the user message and uses LangChain and OpenAI API to Generate Reply
def interpret_and_evaluate(data):
        template = f"""
        You are an AI Customer Support that writes friendly emails back to customers. Adresse the user with his or her name {data['extracted_properties']['name']}. If no name was provided, 
        say 'Dear customer'. 
        The customer's email was categorized as {data['extracted_properties']['category']}, and mentioned the product {data['extracted_properties']['mentioned_product']}. 
        They described an issue: {data['extracted_properties']['issue_description']}. The emotion is: {data['extracted_properties']['emotion']}.
        The sentiment is: {data['extracted_properties']['sentiment']}. 



        Follow the below steps for replying only if the issue description is empty:

        1. If the issue is empty or nothing specified or (if sentiment is positive and emotion is related to happiness)  reply 'Thank you for your Feedback! We'll get back to you soon 😊'

        Follow the below steps for replying only if the issue description is related to suggestion, complaint, feedback:

        1. Reply to user based on category and issue description. reply in a friendly manner.


        Finally end the message with polite sign off
        Your sign-off name in the email is John Doe

        """

        llm = ChatOpenAI(temperature=0)
        prompt_template = PromptTemplate.from_template(template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)

        result = chain.predict(input="")
        return result






# Define the properties to extract from the user text
properties = [
            {
                "name": "category",
                "description": "The type of email this is.",
                "type": "string",
                "enum": [
                    "complaint",
                    "refund_request",
                    "product_feedback",
                    "customer_service",
                    "Appreciation",
                    "Good Feedback",
                    "Bad Feedback",
                ],
                "required": True,
            },
            {
                "name": "mentioned_product",
                "description": "The product mentioned in this email.",
                "type": "string",
                "required": True,
            },
            {
                "name": "issue_description",
                "description": "A list of all problems faced by customer or updates required by the customer or appreciation messages or happy messages ",
                "type": "array",
                "items": {
                        "name": 'Name of the problem',
                        "description": 'Brief explanation of the problem',
                        "type": "string",
                },
                "required": True,
            },
            {
                "name": "name",
                "description": "Name of the person who wrote the email",
                "type": "string",
                "required": True,
            },
            {
                    "name": "sentiment",
                    "description": "Identify the sentiment of the message",
                    "type": "string",
                    "enum": [
                            "Positive",
                            "negative",
                            "neutral",
                    ],
                    "required": True,
            },
            {
                    "name": "emotion",
                    "description": "Identify the emotion of the message",
                    "type": "string",
                    "enum": [
                            "Happy",
                            "Sad",
                            "Anger",
                            "Surprise",
                            "Disgust",
                            "Love",
                            "Anticipation",
                            "Trust",
                            "Gratitude",
                            "Excitement",
                            "Confusion"
                    ],
                    "required": True,
            },
        ]



st.title('Customer Support')
user_input = st.text_area('Enter your message:', '')

# Extracting Features from the user message
documents = [Document(page_content=user_input)]
property_extractor = DoctranPropertyExtractor(properties=properties,openai_api_model = 'gpt-3.5-turbo')
extracted_document = property_extractor.transform_documents(
            documents, properties=properties
        )
# Converting to JSON format
result = json.dumps(extracted_document[0].metadata,indent=2)
result_json = json.loads(result)

reply = interpret_and_evaluate(result_json)


# Streamlit app
if st.button('Submit'):
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')
    st.write(result_json)
    
    if result_json['extracted_properties']['category'] in ['complaint',"refund_request", "product_feedback","customer_service", "Bad Feedback"] or result_json['extracted_properties']['sentiment']=='negative':
        for board in client.list_boards():
            for l in board.list_lists():
                if str(l)=="<List To do>":
                    l.add_card(name=result_json['extracted_properties']['category'],desc=str(result_json['extracted_properties']['issue_description']))
        st.info("Thank you for your Feedback! We'll get back to you soon 😊")
    st.success('Generated AI Reply')                    
    st.write('AI Reply: 😎')
    st.write(reply)

