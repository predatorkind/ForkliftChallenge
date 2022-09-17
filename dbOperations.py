#import pyodbc
import datetime

def saveHiscore(name, score):
    try:
        print("Saving Hi-Score: " + str(score) + " by " + name)
        #todo
    except Exception as e:
        print("Failed to save hi-score.")





def getHiscores():
    try:
        names = []
        scores = []

        #todo


    except Exception as e:
        print("Failed to connect to database to get hi-scores.")

    return names, scores