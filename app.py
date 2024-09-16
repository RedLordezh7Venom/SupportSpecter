from flask import Flask,request,jsonify
from faq_bot import generate_faq_response
from customer_service_chatbot import summarize,chatbot,sentiment_analyzer
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

@app.route("/",methods = ["GET"])
def home():
    return jsonify({"message": "Welcome to the home page"})

@app.route("/faq",methods = ["POST"])
def faq():
    try:
        data = request.form
        faq_query = data.get("question")

        #Generate answer
        ans = generate_faq_response(faq_query)

        #Return JSON response
        return jsonify({"answer":ans})
    except Exception as e:
        return jsonify({"error": str(e)}),403
    
@app.route("/chatbot",methods = ["POST"])
def chat():
    try:
        data = request.form
        query = data.get("question")
        language = data.get("language")

        resp = chatbot(query,language)

        return jsonify({"response":resp})
    except Exception as e:
        return jsonify({"error": str(e)}),403


@app.route("/summary",methods = ["POST"])
def summ():
    try:
        summary = summarize('conversation_history.csv')
        return jsonify({"summary":summary})
    except Exception as e:
        return jsonify({"error": str(e)}),403
    
@app.route("/sentiment",methods = ["POST"])
def sentiment():
    try:
        data = request.form
        feedback = data.get("feedback")
        sent = sentiment_analyzer(feedback)
        return jsonify({"sentiment":sent})
    except Exception as e:
        return jsonify({"error": str(e)}),401
    

if __name__ == "__main__":
    app.run(debug=True)    



