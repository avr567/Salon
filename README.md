# Treat Yo Self -- Alexander Ritov

Name: Alexander Ritov
Pitt ID: avr16

## Installation

1. Instructions to get your code up and running.

set FLASK_APP=salon.py

flask initdb

flask run


## Running the App

1. Instructions to run your application.

Some assumptions:

1. the next 7 days will include days that the stylist will not be working. Those days will not have open appointments for them.
2. Cancel appointment and create appointment work by the user clicking on the available time rather than using a form.
3. After an appointment is cancelled, the appointment will be visible in open appointments all the way at the bottom of the list.
4. Message flashes are used for every user interaction with the system.
