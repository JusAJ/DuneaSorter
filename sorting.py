import csv
import os
import re

VoiceName = 'voice'
EmailName = 'e-mail'
PhoneNumberColumn = 'Remote'
EmailColumn = 'From'
UsersColumn = 'Users'

def newHeader(row):
    parsedHeader = dict()

    if row['Media Type'] == VoiceName:
        parsedHeader['Soort contact'] = 'telefonie'
    elif row['Media Type'] == EmailName:
        parsedHeader['Soort contact'] = 'email'
    else:
        print('Een mediatype is gevonden dat niet ondersteund wordt. Het mediatype is: ' + row['Media Type'])
        raise ValueError()

    parsedHeader['Gebruikers'] = row[UsersColumn]
    parsedHeader['Telefoonnummer'] = row[PhoneNumberColumn]
    parsedHeader['Email'] = row[EmailColumn]
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
        nameLine = row[UsersColumn]
        match = re.search(r'[^;]*\s*$', nameLine)
        if match:
            row[UsersColumn] = match.group(0).strip()
        
        newFile.append(row)

    return newFile


def removeInvalids(file):
    if file[0]['Media Type'] == VoiceName:
        return removeInvalidPhoneNumbers(file)
    elif file[0]['Media Type'] == EmailName:
        return removeInvalidEmail(file)

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
        phoneLine = row[PhoneNumberColumn]
        match = re.search(r'^6\d{8}\s*', phoneLine)
        if match:
            row[PhoneNumberColumn] = "0" + match.group(0).strip()
            newFile.append(row)
    
    return newFile

def removeInvalidEmail(file):
    newFile = []

    for row in file:
        emailLine = row[EmailColumn]
        emailLine = emailLine.split(";")[-1].strip()

        if '@dunea' in emailLine.lower():
            continue

        if 'noreply' in emailLine.lower() or 'no-reply' in emailLine.lower():
            continue

        newRow = row
        newRow[EmailColumn] = emailLine

        newFile.append(row)

    return newFile

def removeDuplicates(file):
    if file[0]['Media Type'] == VoiceName:
        return removeDuplicatePhoneNumbers(file)
    elif file[0]['Media Type'] == EmailName:
        return removeDuplicateEmails(file)


def removeDuplicatePhoneNumbers(file):
    newFile = []

    for oldRow in file:
        addThisRow = True
        for newRow in newFile:
            if oldRow[PhoneNumberColumn] == newRow[PhoneNumberColumn]:
                addThisRow = False
                break
        
        if addThisRow:
            newFile.append(oldRow)

    return newFile

def removeDuplicateEmails(file):
    newFile = []

    for oldRow in file:
        addThisRow = True
        for newRow in newFile:
            if oldRow[EmailColumn] == newRow[EmailColumn]:
                addThisRow = False
                break;

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

    fileToWrite = os.path.join(os.path.dirname(fileToLoad), "output.csv")

    with open(fileToLoad, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        reader = removeMultipleNames(reader)
        reader = removeInvalids(reader)
        reader = removeDuplicates(reader)

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
    print('De conversie is voltooid! Het resultaat staat op de volgende locatie: ' + fileToWrite)


if __name__ == '__main__':
    main()
