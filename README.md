# **SubwayPOS**

## Order \& Sales Management System



A terminal-based restaurant management system built with Python and MySQL.

Started as a school project, but curiosity kept pushing it further.





###### **## 📁 Project Structure**



SUBWAY\_PROGRAM

├── .env                           <- database credentials (not included in repo)

├── .gitignore

├── README.md

├── requirements.txt

├── SETUP

│   └── setup.py                   <- run once to initialize database

├── MENU\_UPLOAD

│   ├── MENU

│   │   ├── burger.csv

│   │   ├── pizza.csv

│   │   ├── salad.csv

│   │   ├── sandwich.csv

│   │   └── wrap.csv

│   └── menu\_upload.py

├── ADMIN\_PASSWORD\_SETUP

│   └── admin\_password\_setup.py    <- to setup password for admin portal

├── SEED

│   └── seed\_data.py               <-generate and insert fake test data

└── PROGRAM

&#x20;   └── program.py                 <- main application



###### **## ⚙️ Features**



\- Customer Portal — view menu and place orders

\- Admin Portal — password protected

\- Edit, Delete, View orders

\- Auto-generated unique Order IDs

\- Sales graphs — Daily, Monthly, Yearly





###### **## 🛠️ Requirements**



\- Python 3.11+

\- MySQL 8.0+





###### **## 📦 Installation**



pip install -r requirements.txt





###### **## 🔐 Environment Setup**



Create a '.env' file in root:



DB\_HOST=localhost

DB\_USER=root

DB\_PASSWORD=yourpassword

DB\_NAME=SUBWAY\_DATABASE

ADMIN\_PASSWORD\_HASH = 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918



$ --> The above hash is sha256 hash of 'admin'



###### **## 🚀 How to Run**



1\. First run 'ADMIN\_PASSWORD\_SETUP/admin\_password\_setup.py' to set admin password before using the system.

2\. Run 'SETUP/setup.py' once

3\. Run 'MENU\_UPLOAD/menu\_upload.py' to upload the menu

4\. Run 'PROGRAM/program.py

