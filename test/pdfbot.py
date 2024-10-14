import os
from werkzeug.utils import secure_filename
import PyPDF2
import requests
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import traceback


app = Flask(__name__)
CORS(app)

# Set your OpenAI and Bing Search API keys
openai_api_key = 'sk-sanctum-gpt-bot-L5KqREC792DiYVUYAc3GT3BlbkFJu4KMXQh0gL2itNJVs3QS'

from openai import OpenAI

client = OpenAI(api_key=openai_api_key)


def classify_query(pdf_extract):
    medical_classification_prompt = f"""
                                    You are tasked with classifying the content of a PDF extract to determine if it is a medical report.

                                    Instructions:
                                    - Analyze the provided text carefully.
                                    - If the text contains medical terminology, diagnoses, treatment information, or any relevant healthcare data, classify it as 'medical'.
                                    - If the text does not contain any medical information and relates to non-medical topics, classify it as 'non-medical'.
                                    
                                    PDF Extract:
                                    {pdf_extract}
                                    
                                    Please provide your classification result as either 'medical' or 'non-medical'.
                                    """
    # Call the model to classify the query

    classification_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a query classifier."},
            {"role": "user", "content": medical_classification_prompt}
        ]
    )
    print(classification_response.choices[0].message.content)
    # Extract the classification result
    classification_result = classification_response.choices[0].message.content.strip()
    return classification_result


@app.route("/pdfchatbot", methods=['POST'])
def chat():
    try:

        if 'file' not in request.files:
            return jsonify({"Input error": "No file part provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"Input error": "No selected file"}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"File error": "The uploaded file is not a PDF"}), 400

        # Use the /tmp directory to save the file temporarily
        tmp_file_path = os.path.join('/tmp', secure_filename(file.filename))
        file.save(tmp_file_path)

        # Read and validate PDF content
        with open(tmp_file_path, 'rb') as pdf_file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(pdf_file)

            # Get the number of pages in the PDF
            num_pages = len(reader.pages)

            # Extract text from all pages
            all_text = ''
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                all_text += page.extract_text()

            # Print or process the extracted text
            print(all_text)

            medical_classify = classify_query(all_text)
            print(medical_classify)
            if medical_classify == "non-medical":
                return jsonify({"File error": "The file does not seem to be a medical report"}), 400

        # Clean up temporary file after use
        os.remove(tmp_file_path)

        # Continue with your agent prompt handling logic
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({"Input error": "No prompt provided"}), 400

        # Call your existing agent logic here...
        return jsonify({"response": "File processed and prompt received successfully."})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"API Internal Error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))