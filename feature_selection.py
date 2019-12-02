import statistics
#converts data in txt file to floats and stores in list
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

    return normalizedList



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

print('This dataset has ' + str(len(featuresList)) + ' (not including the class attribute), with ' + str(len(classList)) + ' instances.')
print('Please wait while I normalize the data...')
featuresList = normalizeFeatures(featuresList)

print(featuresList[0])

if userChoice == '1':
    #TODO
    pass
elif userChoice == '2':
    #TODO
    pass
elif userChoice == '3':
    #TODO
    pass