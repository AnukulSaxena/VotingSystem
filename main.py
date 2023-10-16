from flask import Flask, render_template, request
from face import abc


# Create a Flask application instance
app = Flask(__name__)

# Function to check if input is in a file
def check_input(input1, input2):
    # Check input1 in aadhar.txt
    with open("aadhar.txt", "r") as file1:
        if input1 not in file1.read():
            return "Input 1 does not match in aadhar.txt"

    # Check input2 in voter.txt
    with open("voter.txt", "r") as file2:
        if input2 not in file2.read():
            return "Input 2 does not match in voter.txt"

    # If both inputs are valid, call the 'abc' function from the 'face' module
    abc()

# Define the route to handle the form
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        input1 = request.form.get("input1")
        input2 = request.form.get("input2")
        result = check_input(input1, input2)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
