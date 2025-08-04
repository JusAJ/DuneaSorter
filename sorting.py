import csv
import os
import re

def newHeader(row):
    parsedHeader = dict()

    if row['Media Type'] == 'voice':
        parsedHeader['Soort contact'] = 'telefonie'
    elif row['Media Type'] == 'e-mail':
        parsedHeader['Soort contact'] = 'email'
    else:
        print('An unsupported mediatype is found. The mediatype is: ' + row['Media Type'])
        raise ValueError()

    parsedHeader['Gebruikers'] = row['Users']
    parsedHeader['Telefoonnummer'] = row['Remote']
    parsedHeader['Email'] = row['From']
    parsedHeader['Aan'] = row['To']
    parsedHeader['Datum'] = row['Date']
    parsedHeader['Duur'] = row['Duration']
    parsedHeader['Wachtrij'] = row['Queue']
    parsedHeader['Vaardigheden'] = row['Skills']
    parsedHeader['Resultaatcode'] = row['Wrap-up']

    if row['Media Type'] == 'e-mail':
        raise NotImplementedError()

    return parsedHeader

def removeMultipleNames(file):
    newFile = []

    """
    Explanation of the regex used:
    [^;]*   Matches everything except the semicolon, so the name itself
    \s*     Possible whitespace after the last name
    $       End of string
    """

    for row in file:
        nameLine = row['Users']
        match = re.search('[^;]*\s*$', nameLine)
        if match:
            row['Users'] = match.group(0).strip()
        
        newFile.append(row)

    return newFile

def removeInvalidPhoneNumbers(file):
    newFile = []

    """
    Explanation of the regex used:
    ^       Matches the start of a string
    6       Matches a 6
    \d{8}   Matches exactly 8 numbers
    \s*     Possible whitespace after the telephone number
    This together matches only valid mobile numbers without a leading '0', because that's the way it's exported it seems.

    Note: this does NOT match +316 mobile numbers, or foreign mobile numbers
    """

    for row in file:
        phoneLine = row['Remote']
        match = re.search('^6\d{8}\s*', phoneLine)
        if match:
            row['Remote'] = "0" + match.group(0).strip()
            newFile.append(row)
    
    return newFile

def removeDuplicatePhoneNumbers(file):
    newFile = []

    for oldRow in file:
        addThisRow = True
        for newRow in newFile:
            if oldRow['Remote'] == newRow['Remote']:
                addThisRow = False
                break
        
        if addThisRow:
            newFile.append(oldRow)

    return newFile

def writeCSV(fileToWrite):
    newFileName = 'newCSV.csv'

    if os.path.exists(newFileName):
        os.remove(newFileName)

    with open(newFileName, 'w', newline='') as csvWriteFile:
        fieldnames = []
        for key in fileToWrite[0]:
            fieldnames.append(key)
        
        writer = csv.DictWriter(csvWriteFile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(fileToWrite)

def main():
    newFile = []

    with open('./MiscDocs/exampleVoice.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        reader = removeMultipleNames(reader)
        reader = removeInvalidPhoneNumbers(reader)
        reader = removeDuplicatePhoneNumbers(reader)

        for row in reader:
            try:
                convertedRow = newHeader(row)
            except ValueError:
                exit()
            
            newFile.append(convertedRow)

    writeCSV(newFile)
    

if __name__ == '__main__':
    main()