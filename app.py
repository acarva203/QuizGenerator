import json
import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = "insert_actual_api_key_here"

class OpenAIQuizGenerator:
    def __init__(self,api_key=None):
        self.api_key=api_key
    
    def generate_quiz (self,topic, num_questions=5):
        system_prompt = " You are an expert quiz creator. Create a well-formed, educational quiz for college students."

        user_prompt = f"""Generate a multiple-choice quiz with {num_questions} questions about {topic}
        For each question:
        - make the question clear and consise
        - Provide 4 options (A,B,C,D)
        - make sure exactly one option is correct
        - make the distractors plausible but clearly incorrect
        
        Format your response as valid JSON following this exact structure
        {{
            "title": "Quiz title relate to topic"
            "questions": [
            {{
                "question": "Questions text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index" : 0 #0-based index of correct answer
            }},
            #More qeustions..
            
            ]
        }}"""
        return self.call_openai_api(system_prompt,user_prompt)

def call_openai_api(system_prompt,user_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.api_key}" 
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt },
            {"role": "user", "content": user_prompt}
        ], 
        "temperature": 0.7
        }

    try: 
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json = data
        )

        if response.status_code ==200:
            content = response.json()["choices"][0]["messages"]["content"]
            return self._parse_quiz_json(content)
        else:
            error_message = f"API Error: {response.status_code} - {response.text}"
        print (error_message)
        return {"error": error_message}
    except Exception as e:
        print (f"Error calling OpenAI API {str(e)}")
        return {"error": str(e)}

    
    
def _parse_quiz_json(self,content):
    try:
        if "``json" in content:
            json_str = content.split ("``json")[1].split("``")[1].strip()
        elif "``" in content:

            json_str = content.split("``")[1].strip()
        else:
            json_str =content
        quiz_data = json.loads(json_str)
        return quiz_data
    except Exception as e:
        print(f"Error parsing JSON: {str(e)}")
        print(f"Raw content: {content}")

        return {"error": "Failed to parse the AI response as JSON"}
@app.route('/api/generate_quiz',methods=['POST'])
def generate_quiz():
    data = request.json
    topic = data.get('topic')
    num_questions = int(data.get('num_questions',5))
    
    if not topic:
        return jsonify({"error": "Topci is required"})
    
    quiz_generator= OpenAIQuizGenerator(OPENAI_API_KEY)

    result = quiz_generator.generate_quiz(topic, num_questions)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False)