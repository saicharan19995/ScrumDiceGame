from utils import game
import unittest


def getInfoTextMock(gameCount, bucketCount):
    return "1. Click on Roll a Dice button to roll and move the tokens in the bucket to next stage." \
           "<br>" \
           "2. This steps contines till " + str(gameCount) + " days are completed. After " + str(
        bucketCount - 1) + " roll of dice is considered as 1 day." \
                           "<br>" \
                           "3. You can rest the game any time by clicking on the rest button" \
                           "<br>" \
                           "4. Roll a dice for a day is a special feature which rolls the dice " + str(
        bucketCount - 1) + " times and displays day result."


class TestGame(unittest.TestCase):

    def test_createInfo(self):
        # Mocking Configurations
        game.initGlobal(game, gameCount=5, bucketCount=6)
        assert game.infoText == getInfoTextMock(gameCount=5, bucketCount=6)
        game.initGlobal(game, gameCount=10, bucketCount=8)
        assert game.infoText == getInfoTextMock(gameCount=10, bucketCount=8)

    def test_createLabel(self):
        # Mocking Configurations
        game.initGlobal(game, bucketCount=6)
        assert game.bucketNames == {0: "Backlog", 1: "Refinement", 2: "Design", 3: "Development", 4: "QA",
                                    5: "Production"}
        game.initGlobal(game, bucketCount=8)
        assert game.bucketNames == {0: 'B: 1', 1: 'B: 2', 2: 'B: 3', 3: 'B: 4', 4: 'B: 5', 5: 'B: 6', 6: 'B: 7',
                                    7: 'B: 8'}

    def test_getRollCount(self):
        game.initGlobal(game)
        assert game.getRollCount() == 0

    def test_getNewValue(self):
        game.initGlobal(game)
        assert game.getNewValue() == -1

    def test_initGlobal(self):
        game.initGlobal(game)
        # Test cases
        bucket = [10, 20, 30, 40, 50]
        assert game.diceRolled(5, bucket, 2, 5, 1) == None

        bucket = [5, 10, 15, 20]
        assert game.diceRolled(10, bucket, 1, -1, 1) == None

    def test_getScore(self):
        game.initGlobal(game)
        bucket = [10, 20, 30, 40, 50, 60]
        rollCount = 5
        assert game.getScore(bucket, rollCount) == ('Score for Day 1 is: -80', '')
        game.initGlobal(game, bucketCount=5)
        bucket = [10, 20, 30, 40, 50]
        rollCount = 2
        assert game.getScore(bucket, rollCount) == ("", "")

    def test_enableRollForDay(self):
        game.initGlobal(game)
        assert game.enableRollForDay(5) == ""

    def test_gameDayCount(self):
        game.initGlobal(game)
        assert game.gameDayCount(5) == ""

    def test_gameComplete(self):
        game.initGlobal(game)
        assert game.gameComplete(5) == False
        assert game.gameComplete(50) == True


if __name__ == '__main__':
    unittest.main()
