import os
import random
import matplotlib.pyplot as plt
import json

# All Common values which are required based on config
bucketNames = {0: "Backlog", 1: "Refinement", 2: "Design", 3: "Development", 4: "QA", 5: "Production"}
bucketData = {}
bucketCount = 6
gameDays = 10
diceMaxCount = 8
# Bucket values to handle as global varibale.
bucket_values = [0, 0, 0, 0, 0, 0]
rollCount = 0
newValues = -1  # Value as per new laws
optionIndex = -1  # Default for normal game
infoText = ""
filename = "static/game_result.json"
paraterText = ""

def createInfo(self):
    self.infoText = "1. Click on Roll a Dice button to roll and move the tokens in the bucket to next stage." \
                    "<br>" \
                    "2. This steps contines till " + str(self.gameDays) + " days are completed. After " + str(
        self.bucketCount - 1) + " roll of dice is considered as 1 day." \
                                "<br>" \
                                "3. You can rest the game any time by clicking on the rest button" \
                                "<br>" \
                                "4. Roll a dice for a day is a special feature which rolls the dice " + str(
        self.bucketCount - 1) + " times and displays day result."

def createParameterTest(self):
    configText = "The Limit on Refinement Bucket is " + str(self.newValues) if optionIndex == 1 else \
        "The Limit on All Middle Bucket is " + str(self.newValues) if optionIndex == 2 else \
        "The Dice value is increased by " + str(self.newValues) if optionIndex == 3 else ""

    self.paraterText = f"The Dice Range is from 1 to {diceMaxCount}" \
                       f"<br>" \
                       f"Number of Buckets in the game are {bucketCount}" \
                       f"<br>" \
                       f"The Game ends in {gameDays}" \
                       f"<br>" \
                       f"{configText}" \
                       f"<br>" \
                       f"You can modify all these values in the Config page"

def createLabel(self):
    if self.bucketCount != 6:
        self.bucketNames = {}
        self.bucketData = {}
        for i in range(0, self.bucketCount):
            temp = "B: " + str(i + 1)
            self.bucketNames[i] = temp
            self.bucketData[temp] = []
    else:
        self.bucketNames = {0: "Backlog", 1: "Refinement", 2: "Design", 3: "Development", 4: "QA", 5: "Production"}
        self.bucketData = {"Backlog": [], "Refinement": [], "Design": [], "Development": [], "QA": [], "Production": []}


def roll_dice():
    return random.randint(1, diceMaxCount)


def getRollCount():
    return rollCount


def initGlobal(self, bucketCount=6, gameCount=10, diceMaxCount=6, rollCount=0, newValues=-1, optionIndex=-1):
    self.bucketCount = bucketCount
    self.gameDays = gameCount
    self.rollCount = rollCount
    self.newValues = newValues
    self.optionIndex = optionIndex
    self.diceMaxCount = diceMaxCount
    self.bucket_values = [1000]
    createLabel(self)
    createInfo(self)
    createParameterTest(self)
    initJson()
    for i in range(1, bucketCount):
        self.bucket_values.append(0)


def getNewValue():
    return newValues

def diceRolled(dice, bucket, rollCount, bucketLimit, optionIndex):
    # Leaving the last bucket as it is production.
    shift_from = rollCount % (bucketCount - 1)
    temp_dice = dice
    # Condition to check if Option 1 is selected in game config i.e Limit Refinement
    if bucketLimit != -1 and shift_from == 0 and optionIndex == 1:
        if bucketLimit < temp_dice:
            temp_dice = bucketLimit
        if bucket[shift_from] < temp_dice:
            temp_dice = bucket[shift_from]
    # Condition to check if Option 2 is selected in game config i.e Limit all middle buckets
    elif bucketLimit != -1 and optionIndex == 2:
        if bucketLimit < temp_dice:
            temp_dice = bucketLimit
        if bucket[shift_from] < temp_dice:
            temp_dice = bucket[shift_from]
    # Condition to check if Option 3 is selected in game config i.e Positive adder
    elif bucketLimit != -1 and shift_from == 0 and optionIndex == 3:
        if (temp_dice + bucketLimit) > bucket[shift_from]:
            temp_dice = bucket[shift_from]
        else:
            temp_dice += bucketLimit
    # Normal game flow
    elif bucket[shift_from] < temp_dice:
        temp_dice = bucket[shift_from]
    bucket[shift_from] = bucket[shift_from] - temp_dice
    bucket[shift_from + 1] = bucket[shift_from + 1] + temp_dice
    pass

def updateBucketValues(self):
    if self.rollCount % (self.bucketCount - 1) == 0:
        for index, item in enumerate(self.bucketData):
            self.bucketData[item].append(self.bucket_values[index])

def getCumScore(self):
    cum_data = {}
    for bucket, values in self.bucketData.items():
        cum_data[bucket] = [sum(values[:i + 1]) for i in range(0, len(values))]

    # Create the plot with multiple lines
    for bucket, data in cum_data.items():
        plt.plot(data, label=bucket)
    plt.title("Cumulative Graph")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Value")
    plt.xticks(range(max(map(len, cum_data.values()))))
    plt.legend()
    plt.savefig("static/cumulative_graph.png")

def getScore(bucket, rollCount):
    score = ""
    disable = ""
    if rollCount % (bucketCount - 1) == 0:
        scoreValue = bucket[bucketCount - 1]
        for i in range(1, (bucketCount - 1)):
            scoreValue -= bucket[i]
        score = "Score for Day " + str(rollCount // (bucketCount - 1)) + " is: " + str(scoreValue)
    if rollCount // (bucketCount - 1) == gameDays:
        score = score + "......Game Over !!....."
        disable = "disabled"
    return score, disable


def enableRollForDay(rollCount):
    return "" if rollCount % (bucketCount - 1) == 0 and rollCount // (bucketCount - 1) != gameDays else "disabled"


def gameDayCount(rollCount):
    return "Day Count is: " + str(rollCount // (bucketCount - 1)) if rollCount % (bucketCount - 1) != 0 else ""


def gameComplete(rollCount):
    return rollCount // (bucketCount - 1) == gameDays

def getJson() -> []:
    filename = "static/game_result.json"
    if os.path.exists(filename):
        try:
            with open("static/game_result.json", "r") as f:
                game_result = json.load(f)
                f.close()
        except json.decoder.JSONDecodeError:
            game_result = []
            print("Invalid JSON data.")
        except FileNotFoundError:
            game_result = []
            print("File not found.")
        except Exception:
            game_result = []
    else:
        game_result = []
    return game_result

def initJson():
    game_result = []
    with open(filename, "w") as f:
        json.dump(game_result, f)
        f.close()

def storeJson(self):
    game_result = getJson()
    game = {}

    for index, value in enumerate(self.bucket_values):
        # To ignore Backlog in the table as it is infi
        if index != 0:
            game[bucketNames[index]] = value
    game_result.append(game)

    with open(filename, "w") as f:
        json.dump(game_result, f)
        f.close()

def gameLogic(self):
    dice = self.roll_dice()
    diceRolled(dice=dice, bucket=self.bucket_values, rollCount=self.rollCount, bucketLimit=self.getNewValue(),
               optionIndex=self.optionIndex)
    self.rollCount += 1
    if self.rollCount % (bucketCount - 1) == 0:
        storeJson(self = self)
    score, disable = getScore(bucket=self.bucket_values, rollCount=self.rollCount)
    updateBucketValues(self=self)
    return dice, score, disable


def getCurrentStatusMsg(count):
    return "Moving tasks from: " + bucketNames[count % (bucketCount - 1)]
