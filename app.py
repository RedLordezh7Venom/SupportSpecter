from flask import Flask,request,jsonify
from faq_bot import generate_faq_response
from customer_service_chatbot import summarize,chatbot,sentiment_analyzer,feedback_analysis
from employee_training import response_evaluation,querie_generator
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
        
        response = jsonify({"response": resp})
        response.charset = 'utf-8'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}),403


@app.route("/summary",methods = ["GET"])
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
        print(feedback)
        sent = sentiment_analyzer(feedback)
        print(sent)
        return jsonify({"sentiment":sent})
    except Exception as e:
        return jsonify({"error": str(e)}),401
    
@app.route("/evaluation",methods = ["POST"])
def evaluation():
    try:
        data = request.form
        query = data.get("query")
        response = data.get("response")
        print(query)
        evaluated = response_evaluation(query,response)
        print(evaluated)
        return jsonify({"evaluated":evaluated})
    except Exception as e:
        return jsonify({"error": str(e)}),401
    
@app.route("/querygen",methods = ["POST"])
def querygen():
    try:
        data = request.form
        sector = data.get("sector")
        field = data.get("field")
        experience = data.get("experience")
        generated = querie_generator(sector,field,experience)
        print(generated)
        return jsonify({"generated_query":generated})
    except Exception as e:
        return jsonify({"error": str(e)}),401
    

@app.route("/feedback",methods = ["POST"])
def feedback():
    try:
        data = request.form
        text = data.get("text")
        organization = data.get("organization")
        output = feedback_analysis(text,organization)
        return jsonify({"feedback_analysis":output})
    except Exception as e:
        return jsonify({"error": str(e)}),401
    

if __name__ == "__main__":
    app.run(debug=True)    



