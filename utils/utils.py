import random

# Bucket values to handle as global varibale.
bucket_values = [0, 0, 0, 0, 0, 0]
rollCount = 0
newValues = -1  # Value as per new laws
optionIndex = -1  # Default for normal game


def getNewValue():
    return newValues


def getOption():
    return optionIndex


def roll_dice():
    return random.randint(1, 6)


def getRollCount():
    return rollCount


def initGlobalValues(self, ):
    self.bucket_values = [100, 0, 0, 0, 0, 0]
    self.rollCount = 0
    self.optionIndex = -1
    self.newValues = -1
