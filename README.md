# Medicine Reminder Application (Python)

## Description
A desktop application built using Tkinter that helps users manage and track their medicine schedules with real-time reminders.

## Features
- User authentication (Login & Signup using MySQL)
- Add medicines with scheduled reminder times
- View medicines in a dynamic table
- Delete medicines with a double-click
- Real-time reminder alerts (checks every minute)
- Personalized greeting for logged-in users

## Tech Stack
- Python
- Tkinter (GUI)
- MySQL (Database)
- Datetime module

## Database Structure
Database: login_db

Tables:
- users(username, password)
- data(username, medicine, frequency, id)

## How to Run
1. Install required modules:
   pip install mysql-connector-python

2. Setup MySQL database:
   - Create database: login_db
   - Create required tables

3. Run the program:
   python reminder.py

## Future Improvements
- Add sound notifications
- Improve UI design
- Add edit/update medicine feature

## Developer
Daksh Sharma (Eagle Head)
