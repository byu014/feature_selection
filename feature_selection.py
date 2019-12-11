import statistics
import math
#converts data in txt file to floats and stores in list
def euclideanDistance(a,b,currentFeatures, potentialFeature, mode):
    if mode == 'add':
        total = 0
        for feature in currentFeatures:
            difference = b[feature] - a[feature]
            total += pow(difference,2)
        difference = b[potentialFeature] - a[potentialFeature]
        total += pow(difference,2)
        return math.sqrt(total)
    elif mode == 'remove':
        total = 0
        for feature in currentFeatures:
            if feature != potentialFeature:
                difference = b[feature] - a[feature]
                total += pow(difference,2)
        return math.sqrt(total)

def leaveOneOutCrossValidation(data, currentFeatures, potentialFeature, dataClasses, mode):
    numCorrect = 0
    for i in range(0, len(data)):
        bestSoFar = float("inf")
        bestSoFarLoc = 0
        for j in range(0, len(data)):
            if i != j:
                distance = euclideanDistance(data[i],data[j],currentFeatures, potentialFeature, mode)
                if distance < bestSoFar:
                    bestSoFar = distance
                    bestSoFarLoc = j
        if dataClasses[i] == dataClasses[bestSoFarLoc]:
            numCorrect += 1
    
    accuracy = numCorrect/len(classList)
    return accuracy

def printTestingSet(currentSetOfFeatures, k, accuracy, mode):
    featuresToPrint = ''
    if mode == 'add':
        for feature in currentSetOfFeatures:
            featuresToPrint += str(feature + 1) + ','
        print('Using feature(s) {', featuresToPrint, k+1,'} accuracy is ', round(accuracy * 100, 2),'%',sep = '')
    elif mode == 'remove':
        for feature in currentSetOfFeatures:
            if feature != k:
                featuresToPrint += str(feature + 1) + ','
        print('Using feature(s) {', featuresToPrint.strip(','),'} accuracy is ', round(accuracy * 100, 2),'%',sep = '')

def printBestSetCurrently(currentSetOfFeatures, accuracy):
    featuresToPrint = ''
    for feature in currentSetOfFeatures:
        featuresToPrint += str(feature + 1) + ','
    print('Feature set {', featuresToPrint.strip(','),'} was best, accuracy is ', round(accuracy * 100, 2), '%',sep = '')

def printBestFeatureSubset(bestSubsetAccuracyTuple):
    featuresToPrint = ''
    for feature in bestSubsetAccuracyTuple[0]:
        featuresToPrint += str(feature + 1) + ','
    print('Finished search!! The best feature subset is {', featuresToPrint.strip(','),'}, which has an accuracy of ', round(bestSubsetAccuracyTuple[1] * 100, 2), '%',sep = '')

def forwardSelection(data, dataClasses):
    currentSetOfFeatures = []
    bestSubsetAccuracyTuple = ([],0)
    
    for i in range(0,len(data[0])):
        featureToAddAtThisLevel = 0
        bestSoFarAccuracy = 0

        for k in range(0, len(data[0])):
            if k not in currentSetOfFeatures:
                accuracy = leaveOneOutCrossValidation(data, currentSetOfFeatures, k, dataClasses, 'add')
                printTestingSet(currentSetOfFeatures, k, accuracy, 'add')
                if accuracy > bestSoFarAccuracy:
                    bestSoFarAccuracy = accuracy
                    featureToAddAtThisLevel = k

        currentSetOfFeatures.append(featureToAddAtThisLevel)
        printBestSetCurrently(currentSetOfFeatures,bestSoFarAccuracy)
        if bestSoFarAccuracy > bestSubsetAccuracyTuple[1]:
            bestSubsetAccuracyTuple = (currentSetOfFeatures.copy(), bestSoFarAccuracy)
    
    printBestFeatureSubset(bestSubsetAccuracyTuple)

def backwardElimination(data, dataClasses):
    currentSetOfFeatures = [i for i in range(0, len(data[0]))]
    bestSubsetAccuracyTuple = ([],0)
    
    for i in range(0,len(data[0])):
        featureToRemoveAtThisLevel = 0
        bestSoFarAccuracy = 0

        for k in range(0, len(data[0])):
            if k in currentSetOfFeatures:
                accuracy = leaveOneOutCrossValidation(data, currentSetOfFeatures, k, dataClasses, 'remove')
                printTestingSet(currentSetOfFeatures, k, accuracy, 'remove')
                if accuracy > bestSoFarAccuracy:
                    bestSoFarAccuracy = accuracy
                    featureToRemoveAtThisLevel = k

        currentSetOfFeatures.remove(featureToRemoveAtThisLevel)
        printBestSetCurrently(currentSetOfFeatures,bestSoFarAccuracy)
        if bestSoFarAccuracy > bestSubsetAccuracyTuple[1]:
            bestSubsetAccuracyTuple = (currentSetOfFeatures.copy(), bestSoFarAccuracy)
    
    printBestFeatureSubset(bestSubsetAccuracyTuple)


def txtToList(f):
    classList = []
    featuresList = []
    for line in f:
        row = line.split()
        row = [float(num) for num in row]
        # featuresArray.append((row[0],row[1:]))
        classList.append(row[0])
        featuresList.append(row[1:])
    
    return classList, featuresList

def normalizeFeatures(featuresList):
    #TODO
    normalizedList= []
    for i in range(0, len(featuresList[0])):
        feature = [row[i] for row in featuresList]
        normalizedFeature = [(num - statistics.mean(feature))/statistics.stdev(feature) for num in feature]
        normalizedList.append(normalizedFeature)
    transposedList = [[row[i] for row in normalizedList] for i in range(len(normalizedList[0]))] #transposes list due to way I made the list
    return transposedList 


algorithmDict = {'1':'Forward Selection', '2':'Backward Elimination', '3':'Bailey\'s Special Algorithm'}

print('Welcome to Bailey Yu\'s Feature Selection Algorithm')

f = ''
while f == '':
    inputFile = input('Type in the name of the file to test: ')
    try:
        f = open(inputFile,'r')
    except:
        print('Invalid file')
        f = ''

classList, featuresList = txtToList(f)

print('Type the number of the algorithm you want to run.')

userChoice = '0'
while userChoice == '0':
    for number,choice in algorithmDict.items():
        print(number + ') ' + choice)

    userChoice = input('')

    if userChoice not in algorithmDict.keys():
        print('Invalid choice')
        userChoice = '0'

print('This dataset has ' + str(len(featuresList[0])) + ' (not including the class attribute), with ' + str(len(classList)) + ' instances.')
print('Please wait while I normalize the data...')
featuresList = normalizeFeatures(featuresList)


if userChoice == '1':
    forwardSelection(featuresList, classList)
elif userChoice == '2':
    backwardElimination(featuresList, classList)
elif userChoice == '3':
    #TODO
    pass