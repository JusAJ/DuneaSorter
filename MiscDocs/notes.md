# Notes

## To-do

### E-mail

- Title of headers should be changed to:
    - Soort contact
    - Gebruikers
    - Telefoonnummer
    - Email
    - Aan
    - Datum
    - Duur
    - Wachtrij
    - Vaardigheden
    - Resultaatcode
    - Case-ID
- "Soort contact" should be changed to "email"
- Double users should be removed. Only the last one should remain
- The following email adresses should be removed from column "Email" **(should the whole entry be removed?)**
    - Duplicated
    - Dunea
    - Noreply
- Duplicated email addresses with `;` should be removed from column "Aan". **Needs clarification**

### Telephone

- Title of headers should be changed to:
    - Soort contact
    - Gebruikers
    - Telefoonnummer
    - Email
    - Aan
    - Datum
    - Duur
    - Wachtrij
    - Vaardigheden
    - Resultaatcode
- "Soort contact" should be changed to "telefonie"
- Double users should be removed, only last one should remain
- Duplicated numbers should be removed (The whole entry should be removed)
- Only 06-numbers are allowed. With other numbers the whole entry needs to be removed.
- Telephone numbers should be checked if valid by:
    - checking if the first number is a 6
    - if it fullfills the required number of numbers (a mobile number has always 8 numbers after the 6)

## Other notes

- The file is comma separated: `,`
- There's more fields than indicated in the example file
- Phone is mediatype "voice"
- E-mail is mediatype "e-mail"
