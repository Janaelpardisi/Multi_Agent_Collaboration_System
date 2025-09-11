from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key from .env
api_key = os.getenv("GOOGLE_API_KEY")

# prepare model for gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=api_key
)

# ====== Agent1 for Research Agent ======
def research_agent(query):
    prompt = f"""
انت Research Agent . ابحث عن معلومة مبدئية للاجابة عن السؤال التالي:
{query}
اعطني نصوص خام للاجابة عن معلومات غير ملخصة
"""
    return llm.invoke([HumanMessage(content=prompt)]).content

# ====== Agent2 for Summarizer Agent ======
def summarizer_agent(text):
    prompt = f"""
انت Summarizer Agent. لخص النص التالي في نقاط اساسية :
{text}
"""
    return llm.invoke([HumanMessage(content=prompt)]).content

# ====== Agent3 for Reasoning Agent ======
def reasoning_agent(summary, query):
    prompt = f"""
انت Reasoning Agent. بناء علي الملخص التالي :
{summary}
جاوب علي السؤال الاصلي : {query}
مع توضيح الاستنتاجات المهمة
"""
    return llm.invoke([HumanMessage(content=prompt)]).content

# ====== Agent4 for Decision Agent ======
def decision_agent(answer):
    prompt = f"""
انت Decision Agent. صغ الاجابة التالية في شكل نهائي وواضح وسهل الفهم 
{answer}
"""
    return llm.invoke([HumanMessage(content=prompt)]).content

# ====== Orchestrator ======
def multi_agent_system(query):
    print("Research Agent Running ..........")
    research_output = research_agent(query)

    print("Summarizer Agent Running .........")
    summarizer_output = summarizer_agent(research_output)

    print("Reasoning Agent Running ...........")
    reasoning_output = reasoning_agent(summarizer_output, query)

    print("Decision Agent Running .......")
    final_answer = decision_agent(reasoning_output)

    return final_answer

# ====== Testing Stage ======
if __name__ == "__main__":
    question = "ما هو دور الLSTM في الترجمة الآلية مقارنة ب Transformer?"
    result = multi_agent_system(question)
    print("Final Answer:", result)
