from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import fitz


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

                


app = Flask(__name__)

# Set the path to the folder where PDF files will be uploaded
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['pdf_file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # show = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # doci = fitz.open("static/sample.pdf")
        # doci = fitz.open(show)
        doci = fitz.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        print('doci:',doci)

        text = ""
        for page in doci:
            # print(type(page))
            text += page.get_text()
        # print(text)

        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)

        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        # Creating a dictionary to keep the score
        # of each sentence
        sentences = sent_tokenize(text)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]

        # Average value of a sentence from the original text
        if(len(sentenceValue) == 0):
            average = 0
        else:
            average = int(sumValues / len(sentenceValue))

        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence

        # print(summary)
        flash('File uploaded successfully!')

        return render_template('index.html', summary=summary)

        
        # return redirect(url_for('uploaded_file', filename=filename))
        # return render_template('index.html')
    else:
        flash('Invalid file. Only PDF files are allowed.')
        return redirect(request.url)


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'  # Set a secret key for the flash messages
    app.run(debug=True)
