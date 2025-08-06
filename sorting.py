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
        print('Een mediatype is gevonden dat niet ondersteund wordt. Het mediatype is: ' + row['Media Type'])
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
    parsedHeader['Case-ID'] = row['Case-ID']

    return parsedHeader

def removeMultipleNames(file):
    newFile = []

    #| Explanation of the regex used:
    #| [^;]*   Matches everything except the semicolon, so the name itself
    #| \s*     Possible whitespace after the last name
    #| $       End of string

    for row in file:
        nameLine = row['Users']
        match = re.search(r'[^;]*\s*$', nameLine)
        if match:
            row['Users'] = match.group(0).strip()
        
        newFile.append(row)

    return newFile

def removeInvalidPhoneNumbers(file):
    newFile = []

    #| Explanation of the regex used:
    #| ^       Matches the start of a string
    #| 6       Matches a 6
    #| \d{8}   Matches exactly 8 numbers
    #| \s*     Possible whitespace after the telephone number
    #| This together matches only valid mobile numbers without a leading '0', because that's the way it's exported it seems.
    #|
    #| Note: this does NOT match +316 mobile numbers, or foreign mobile numbers

    for row in file:
        phoneLine = row['Remote']
        match = re.search(r'^6\d{8}\s*', phoneLine)
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

def writeCSV(fileToWrite, newFileName):
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

    fileToLoad = ""

    while True:
        fileToLoad = input('Voer het bestand in dat geladen moet worden: \n')

        if fileToLoad != "" and os.path.exists(fileToLoad) and fileToLoad[-4:] == '.csv':
            break;
    
        if fileToLoad == "":
            continue

        if not os.path.exists(fileToLoad):
            print('Het ingevoerde bestand bestaat niet.')
        elif fileToLoad[-4:] != '.csv':
            print('Het ingevoerde bestand is geen CSV bestand.')

    fileToWrite = "./newCSV.csv"

    with open(fileToLoad, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        reader = removeMultipleNames(reader)
        reader = removeInvalidPhoneNumbers(reader)
        reader = removeDuplicatePhoneNumbers(reader)

        for row in reader:
            try:
                convertedRow = newHeader(row)
            except ValueError:
                if os.path.exists(fileToWrite):
                    os.remove(fileToWrite)
                exit('Het script kan niet verder, en sluit nu af.')
            except KeyError as ke:
                exit(f'De volgende kolom kan niet worden gevonden: {ke.args[0]}')
            
            newFile.append(convertedRow)

    writeCSV(newFile, fileToWrite)
    

if __name__ == '__main__':
    main()