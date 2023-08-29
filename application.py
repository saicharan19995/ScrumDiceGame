import time

import numpy as np

import utils.game as game
from flask import Flask, render_template, jsonify, request
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def renderGamePage(page= 'gamePage.html',dice=5, score=0, disable=''):
    dayCount = game.gameDayCount(game.rollCount)
    currentStatus = game.getCurrentStatusMsg(game.rollCount)
    return render_template(page, dice_value=dice, bucket_values=game.bucket_values,
                           bucket_name=game.bucketNames, scoreText=score,
                           disable_button=disable, dayCount=dayCount,
                           bucketLimit=game.getNewValue(), currentStatus=currentStatus,
                           gameInfoText=game.infoText, gameParameterText=game.paraterText)

def renderInitalGamePage(page= 'gamePage.html'):
    return render_template(page, dice_value=5, bucket_values=game.bucket_values,
                       bucket_name=game.bucketNames, gameInfoText=game.infoText, gameParameterText=game.paraterText)

def cumGraphArea(buckets, noOfDays):
    days = [x for x in range(1, int(noOfDays)+1)]
    cumulative_data = []
    labels = list(buckets.keys())
    for bucket, values in buckets.items():
        if bucket != "Backlog" and bucket != "B: 1":
            cumulative_data.append(list(np.cumsum(values)))
    plt.clf()
    plt.stackplot(days, cumulative_data, baseline='zero',labels=labels)
    plt.title("Cumulative Graph")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Value")
    plt.legend()
    plt.savefig("static/cumulative_graph.png")

def initCumGraph():
    plt.clf()
    plt.title("Cumulative Graph")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Value")
    plt.savefig("static/cumulative_graph.png")

@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route('/hello')
def helloWorld():
    return render_template("hello.html")


@app.route('/gamePage')
def gamePage():
    # Normal Game Configs are set
    game.initGlobal(game, bucketCount=6, diceMaxCount=6, gameCount=10)
    initCumGraph()
    return renderInitalGamePage()

@app.route('/gamePage/roll')
def mainPageRollClicked():
    dice, score, disable = game.gameLogic(self=game)
    cumGraphArea(game.bucketData, (game.rollCount // (game.bucketCount - 1)))
    return renderGamePage(dice=dice, score=score, disable=disable)

@app.route('/gamePage/roll_day')
def mainPageRollDayClicked():
    rollCount = game.rollCount
    time.sleep(0.25)
    dice, score, disable = game.gameLogic(self=game)
    if (rollCount + 1) % (game.bucketCount - 1) == 0:
        cumGraphArea(game.bucketData, (game.rollCount // (game.bucketCount - 1)))
        return renderGamePage(page="gamePage.html", dice=dice,score=score,disable=disable)
    else:
        return renderGamePage(page="gamePageDay.html", dice=dice, score=score, disable=disable)

@app.route('/graph')
def graphPage():
    return render_template('graph.html', img_url="/static/cumulative_graph.png")

@app.route('/check_game_completion')
def check_game_completion():
    isGameComplete = game.gameComplete(game.rollCount)
    return jsonify({'isGameComplete': isGameComplete})


@app.route('/configration')
def configPage():
    return render_template('gameConfig.html')


@app.route('/gameTypePage')
def gameTypePage():
    return render_template('gameTypeSelection.html')

@app.route('/gameResultPage')
def gameResultPage():
    game_result = game.getJson()
    header = list(game.bucketNames.values())
    return render_template('gameResult.html', game_result = game_result, headers = header[1:])

@app.route('/gameParameterPage')
def gameParameterPage():
    return render_template('gameParameterSelection.html')

@app.route('/gameAllConfigPage')
def gameAllConfigPage():
    return render_template('gameAllConfigSelection.html')

@app.route('/select_option', methods=['POST'])
def optionSelected():
    selected_option = request.form['option']
    selected_value = request.form['newValue']
    game.initGlobal(self=game, optionIndex=int(selected_option[-1]), newValues=int(selected_value))
    initCumGraph()
    return renderInitalGamePage()


@app.route('/select_parameter_option', methods=['POST'])
def parmeterSelected():
    game.initGlobal(game, bucketCount=int(request.form['bucket_max']),
                    diceMaxCount=int(request.form['dice_max']),
                    gameCount=int(request.form['game_over_max']))
    initCumGraph()
    return renderInitalGamePage()

@app.route('/select_multiple_config_option', methods=['POST'])
def mulipltConfigSelected():
    game.initGlobal(game, optionIndex=int(request.form['option'][-1]),
                    newValues=int(request.form['newValue']),
                    bucketCount=int(request.form['bucket_max']),
                    diceMaxCount=int(request.form['dice_max']),
                    gameCount=int(request.form['game_over_max']))
    initCumGraph()
    return renderInitalGamePage()

if __name__ == '__main__':
    app.run(debug=True)
