from flask import Flask, render_template, request, session
from algorithimLogic import ScheduleMaker



app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/makeSchedule', methods=['GET', 'POST'])
def makeSchedule():
    if request.method == 'GET':
        return render_template("inputs.html", sportInputs=[i for i in range(1, 5)], teamInputs=[i for i in range(1, 5)])
    
    data = request.form
    sportOptions = [data["sport" + str(i)] for i in range(1, 5)]
    teams = [data["team" + str(i)] for i in range(1, 5)]
    # filter out empty values
    sportOptions = list(filter(lambda x: x is not None, sportOptions))
    teams = list(filter(lambda x: x is not None, teams))
    print(f"{teams = } \n {sportOptions = }")


    main = ScheduleMaker(teams, sportOptions)
    return render_template("createSchedule.html", data=main.createScedule(3))

if __name__ == '__main__':
    app.run(debug=True)