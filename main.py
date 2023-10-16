from flask import Flask, render_template, request, redirect, url_for
import face_recognition
import dlib
import cv2
from imutils.video import WebcamVideoStream
import time
import openpyxl

app = Flask(__name__)

known_image = face_recognition.load_image_file("anukul.png")
known_encoding = face_recognition.face_encodings(known_image)[0]

def abc():
    detect = dlib.get_frontal_face_detector()
    vs = WebcamVideoStream(src=0).start()

    start_time = time.time()
    while True:
        frame = vs.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        if subjects:
            rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([known_encoding], face_encoding)
                if True in matches:
                    vs.stop()
                    return 1

        # Check if a certain time limit (e.g., 30 seconds) has passed
        if time.time() - start_time > 10:
            vs.stop()
            break

    return 0

@app.route('/process_data', methods=['POST'])
def process_data():
    input1 = request.form.get('input1')
    input2 = request.form.get('input2')

    with open("aadhar.txt", "r") as file1:
        if input1 not in file1.read():
            return "Input 1 does not match in aadhar.txt"

    # Check input2 in voter.txt
    with open("voter.txt", "r") as file2:
        if input2 not in file2.read():
            return "Input 2 does not match in voter.txt"

    result = abc()

    if result == 0:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("face_matched"))

@app.route('/face_matched')
def face_matched():
    return render_template('vote.html')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/input_vote", methods=['POST'])
def input_vote():
    selected_option = request.form.get('option')

    # Load the existing Excel file or create a new one if it doesn't exist
    try:
        workbook = openpyxl.load_workbook('result.xlsx')
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

    # Select the first sheet in the workbook
    sheet = workbook.active

    # Find the next empty row in the sheet
    next_row = len(sheet['A']) + 1

    # Write the selected option to the Excel file
    sheet[f'A{next_row}'] = selected_option

    # Save the Excel file
    file_name = 'result.xlsx'
    workbook.save(file_name)
    result = f"Result appended to {file_name}"
    return result

if __name__ == "__main__":
    app.run(debug=True)
