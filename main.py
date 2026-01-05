
# from flask import Flask, render_template, request, jsonify
# from google import genai

# client = genai.Client(api_key="AIzaSyDHe-07Vh_9e8rQEwEHvrXJFiWX7Yv75aw")

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json["message"]

#     instructions = """
#     You are a Student AI Assistant.
#     Format nicely with emojis and bullets.
#     DO NOT use Markdown bold like **text**
#     DO NOT use asterisks
#     Use headings with emojis and clean spacing.
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=f"{instructions}\n\nUser Question: {user_input}"
#     )

#     clean_reply = response.text.replace("**", "")  # 🔥 Removes stars

#     return jsonify({"reply": clean_reply})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)


API_KEY = "AIzaSyDHe-07Vh_9e8rQEwEHvrXJFiWX7Yv75aw"
client = genai.Client(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        
        return jsonify({"reply": response.text})

    except Exception as e:
        # This will print the SPECIFIC error to your terminal (e.g., Invalid API Key)
        print(f"--- SERVER ERROR ---")
        print(e)
        print(f"--------------------")
        return jsonify({"reply": f"Backend Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=8080, debug=True)