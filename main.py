from flask import Flask, render_template, request, jsonify
import openai
import os

# ✅ Create OpenAI client using new version of the library
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Set up the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # ✅ Use new-style OpenAI chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Civily, an AI assistant trained in UK civil law. "
                        "You provide detailed, factual, and case-based information to people dealing with civil disputes — like housing, tenancy, deposits, breakups, co-parenting, and consumer rights. "
                        "You must respond with actual information from UK law where relevant: refer to real laws, acts (e.g. Housing Act 1988), case law, and procedures. "
                        "Do NOT refer the user to other services (like Citizens Advice) unless the user asks for help contacting someone. "
                        "Do NOT say 'I cannot provide legal advice' — instead, share helpful legal **facts**, rights, timelines, and what the law says. "
                        "You are here to empower users with legal knowledge, not to avoid responsibility. "
                        "Answer in a calm, clear tone. Format multi-step answers with short paragraphs or bullet points. Be direct, supportive, and legally useful."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR FROM OPENAI:", e)  # 🛠 Debugging info in the Console
        return jsonify({"error": "Internal server error"}), 500

# ✅ Run the web app on Replit's hosted port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
