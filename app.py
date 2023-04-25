import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import Separate_char
import detection

app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.config['UPLOAD_FOLDER'] = './static'
app.config['UPLOAD_FOLDER'] = './static/Images'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = "equation" + os.path.splitext(file.filename)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image uploaded successfully', 'success')
        else:
            flash('No file uploaded', 'error')
    return redirect(url_for('index'))


@app.route('/script1')
def script1():
    if Separate_char.separate_dig():
        # output = 'Output from script 1'
        out_put = detection.detector_result()
        output = ""
        for i in out_put:
            output += i

        folder_path = './static/digits/'

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        output = 'Character Segmentation Failed...'

    return jsonify({'output': output})


@app.route('/script2')
def script2():
    input_text = request.args.get('input', '')
    # output = f'Output from script 2 with input: {input_text}'
    output = f'After Calculation: {eval(input_text)}'
    print(output)
    return jsonify({'output': output})
