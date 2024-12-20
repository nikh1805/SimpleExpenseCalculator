# Simple Expense Calculator
Expense Calculator is a web application that helps users manage their budget and expenses. It allows users to track daily expenditures by recording who bought what, when, and how much was spent or earned. The application provides a summary of total balance and daily average income/expenses since the first recorded transaction.

## Features

- Track and record expenses with descriptions, types (Credit or Debit), dates, and amounts.
- View a summary of total balance and daily average since the first transaction.
- Add, update, and delete expense records.
- Simple and basic user interface.

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- SQLite (pre-installed with Python)

### Create Environment and Install Dependencies

**Windows**

```shell
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac**

```shell
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

### Run the application

```shell
python expense.py
```

### Open your browser and go to: http://localhost:9000
