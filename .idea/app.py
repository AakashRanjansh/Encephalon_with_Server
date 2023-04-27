import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import Separate_char
import detection
import math
import cmath

app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.config['UPLOAD_FOLDER'] = './static'
app.config['UPLOAD_FOLDER'] = './static/Images'


def quadra(a=1,b=1,c=1):
    # calculate the discriminant
    d = (b ** 2) - (4 * a * c)

    # find two solutions
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)

    return 'solution are {0} and {1}'.format(sol1, sol2)


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

    if input_text.count("<") == 1:
        A = input_text.index("<")
        first = int(input_text[0:A])
        last = int(input_text[A + 1:])
        print(first < last)
        output = f'After Calculation: {first < last}'

    elif input_text.count(">") == 1:
        A = input_text.index(">")
        first = int(input_text[0:A])
        last = int(input_text[A + 1:])
        print(first < last)
        output = f'After Calculation: {first > last}'

    elif input_text.count("<") == 2:
        A = input_text.index("<")
        first = int(input_text[0:A])
        last = int(input_text[A + 2:])
        print(first < last)
        output = f'After Calculation: {first << last}'

    elif input_text.count(">") == 2:
        A = input_text.index(">")
        first = int(input_text[0:A])
        last = int(input_text[A + 2:])
        print(first < last)
        output = f'After Calculation: {first >> last}'

    elif input_text[0:4] == 'sqrt':
        sq_in = int(input_text[4:])
        output = f'After Calculation: {math.sqrt(sq_in)}'


    else:
        output = f'After Calculation: {eval(input_text)}'
        print(output)
    return jsonify({'output': output})



@app.route('/script3')
def script3():
    input_text = request.args.get('input', '')
    # output = f'Output from script 2 with input: {input_text}'
    a = int(input_text[0])
    b = int(input_text[3])
    c = int(input_text[6])


    output = quadra(a,b,c)

    return jsonify({'output': output})


# @app.route('/script4')
# def quiz():
#     return render_template('quiz.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
