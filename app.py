import os
import shutil
from flask import Flask, jsonify, request
from flask_cors import CORS
import PyPDF2


app = Flask(__name__)
CORS(app)

# Define the home route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the PDF Reader!'})

# Define the /api/data route to accept PDF file
@app.route('/upload-pdf', methods=['POST'])
def get_pdf_data():
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file:
    # Folder path where the PDF will be stored
        folder_path = './files'  # Using relative path for the folder

    # Check if the folder exists, delete and recreate if it does
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Remove the folder and all its contents
    os.makedirs(folder_path)  # Create the folder anew

    # Full path to save the file
    full_path = os.path.join(folder_path, file.filename)

    # Save the file
    file.save(full_path)
    

    # Check if the file is a PDF
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file. Please upload a PDF file'})

    # Read the PDF and extract the first line

    
    pdf_reader = PyPDF2.PdfReader(file)
    first_page = pdf_reader.pages[0]
    first_line = first_page.extract_text().split('\n')[0]
    return jsonify({'first_line': first_line})


# Define the /ask-question route to accept POST requests
@app.route('/ask-question', methods=['POST'])
def ask_question():
    # Access the question data from the request body
    question = request.json.get('question')

    # Do something with the question data (e.g., save to a database)
    print('Received question:', question)

    # Send a response back to the client
    answer = "Question received successfully"

    # Return the answer as JSON
    return jsonify(answer=answer)


# Run the Flask app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)