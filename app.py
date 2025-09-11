from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from .env file
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)

# ====== Agent Function ======
def run_agent(role, text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a {role} agent."),
        ("user", text)
    ])
    return llm.invoke(prompt.format_messages()).content

# ====== API Endpoint ======
@app.route("/ask", methods=["POST"])
def ask_agents():
    query = request.json.get("query", "")
    if not query:
        return jsonify({"error": "please provide a query"}), 400

    research = run_agent("research", query)
    summary = run_agent("summary", research)
    reasoning = run_agent("reasoning", summary)
    final_answer = run_agent("decision_making", reasoning)

    return jsonify({"query": query, "answer": final_answer})

# ====== Home Page ======
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
