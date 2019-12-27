Assumptions and Clarification:
I wrote my code assumming that the data is clean and correct. In the file sent some of the data was not
in the correct JSON format. Things like double quotes were missing or there was an "=" instead of a ":".
I went through and cleaned the data up.


How to run:
I wrote this in Python 3.7.4 and Flask 1.1.1. You can download the latest version of Flask through pip or install 
in another way.

1. Navigate to the "Question 1 REstFul API" folder containing the "app.py" file in command line.
2. Enter "flask run". Server should start up with no issues.
3. Defaults to running on localhost so you url to hit is going to be something like this: 
"http://127.0.0.1:5000/nba/players" with any http api client(I used Postman).