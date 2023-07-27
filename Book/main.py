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
        show = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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














# from flask import Flask, flash, url_for, render_template ,request,redirect,session
# import urllib.request
# from werkzeug.utils import secure_filename
# import os
# import pymysql

# app = Flask(__name__,template_folder="templates")
# app.secret_key=os.urandom(24)

# # conn=pymysql.connect(host="localhost",user="root",password="",database="hacknova")
# # Cursor=conn.cursor()

# # @app.route('/', methods=['GET','POST'])
# # def landing():
# #     return render_template('upload.html')

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('upload.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     if request.method == 'POST' and 'upload' in request.files:
#         upload = request.files['upload']
#         filename = upload.filename
#         file_ext = os.path.splitext(filename)[-1]  # Get the file extension
#         if file_ext.lower() in ['.pdf', '.txt', '.docx']:  # Add other allowed extensions if needed
#             upload.save(os.path.join("Static", filename))
#             return "File successfully uploaded and saved!"
#         else:
#             return "Invalid file format. Please upload a PDF, TXT, or DOCX file."

#     return "Upload failed. Please select a file."


# # @app.route('/' , methods=['POST'])
# # def upload():
# #     upload = request.files['upload']
# #     upload.save(os.path.join("Static/", upload.filename))

# #     return render_template('upload.html')

# # @app.route('/login.html')
# # def Login():
# #     return render_template('login.html')

# # @app.route('/register.html')
# # def register():
# #     return render_template('register.html') 

# # @app.route('/logout')
# # def logout():
# #     session.pop('user_Id')
# #     return redirect('/')

# # @app.route('/feedback.html')
# # def contact():
# #     if 'user_Id' in session:
# #         if 'user_Id' or 'email' in session:
# #             user_Id = session['user_Id']  
# #             email = session['email']
# #             # name = session['name']
# #             return render_template('feedback.html', email=email)
# #         elif 'user_Id' not in session:
# #             return redirect('/login.html')
# #         else:
# #             user_Id = None
# #             return render_template('feedback.html', user_Id=user_Id) 
# #     else:
# #         return render_template('login.html')

# # @app.route('/welcome.html')
# # def home():
# #     if 'user_Id' or 'email' in session:
# #         user_Id = session['user_Id']  
# #         email = session['email']
# #         # name = session['name']
# #         return render_template('welcome.html', email=email)
# #     elif 'user_Id' not in session:
# #         return redirect('/login.html')
# #     else:
# #         user_Id = None
# #         return render_template('welcome.html', user_Id=user_Id)


# # @app.route('/login_validation', methods=['POST'])
# # def login_validation():
# #     email=request.form.get('email')
# #     password=request.form.get('password')

# #     Cursor.execute(""" SELECT * FROM `login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'  """.format(email,password))
# #     login = Cursor.fetchall()
# #     if len(login)>0:
# #         session['user_Id']=login[0][0] 
# #         session['email']=login[0][1]       #to print the name of the perticular logged in user
# #         return redirect('/welcome.html')
# #     else:
# #         return render_template('/login.html')


# # @app.route('/add_user', methods=['POST'])
# # def add_user():
# #     name=request.form.get('name')
# #     email=request.form.get('email')
# #     password=request.form.get('password')

# #     Cursor.execute(""" INSERT INTO `login` (`user_Id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')  """.format(name,email,password))
# #     conn.commit()

# #     Cursor.execute(""" SELECT * FROM `login` WHERE `email` LIKE '{}' """.format(email))
# #     myuser = Cursor.fetchall()
# #     session['user_Id'] = myuser[0][0]
# #     return redirect("/login.html")


# # @app.route('/feedback.html', methods=['POST'])
# # def contact_us():
# #     name=request.form.get('name')
# #     email=request.form.get('email')
# #     message=request.form.get('message')

# #     Cursor.execute(""" INSERT INTO `contact_us` (`user_Id`,`name`,`email`,`message`) VALUES (NULL,'{}','{}','{}')  """.format(name,email,message))
# #     conn.commit()

# #     return redirect("/feedback.html")



# app.run(debug=True)