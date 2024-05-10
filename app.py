from flask import Flask, request, render_template
import pyodbc
import os

SERVER = os.environ['SERVER']
DATABASE = os.environ['DATABASE']
USERNAME = os.environ['NAME']
PASSWORD = os.environ['PASSWORD']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', success_message=None)

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        # Get inputs from POST request
        input1 = request.form.get('input1')
        input2 = request.form.get('input2')
        input3 = request.form.get('input3')

        # Azure SQL connection string
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

        # Establish connection
        conn = pyodbc.connect(connectionString) 

        # Create cursor
        cursor = conn.cursor()

        # Insert data into table
        cursor.execute(
            "INSERT INTO test_table (column1, column2, column3) VALUES (?, ?, ?)",
            input1, input2, input3
        )

        # Commit transaction
        conn.commit()

        success_message = 'Data stored successfully'

    except Exception as e:
        success_message = f'Error: {str(e)}'

    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
