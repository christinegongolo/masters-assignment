"""
Question 2 (20 marks)
Explain the purpose of the key steps involved in connecting to a SQLite
database in Python, including sqlite3.connect(), the cursor object, and
the commit() method.

--------------------------------------------------------------------------
Key steps
--------------------------------------------------------------------------
1. sqlite3.connect("database.db")
   - Opens a connection to a SQLite database file. If the file does not
     exist, SQLite creates it. This Connection object represents the
     session with the database and is what commit()/close() are called on.

2. connection.cursor()
   - Creates a Cursor object, which is what actually executes SQL
     statements (execute(), executemany()) and lets you fetch results
     (fetchone(), fetchall()) after a SELECT.

3. connection.commit()
   - SQLite wraps changes (INSERT/UPDATE/DELETE) in a transaction.
     commit() permanently saves those changes to the database file.
     Without calling commit(), changes made in the session can be lost,
     especially if the connection is closed or the program crashes.

4. connection.close()
   - Closes the connection and releases the database file/resources.

Below is a worked example showing all of these steps together.
"""

import sqlite3


def demo():
    # Step 1: connect (creates the file if it doesn't exist)
    connection = sqlite3.connect("students.db")

    # Step 2: get a cursor to run SQL commands
    cursor = connection.cursor()

    # Create a table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER
        )
        """
    )

    # Insert some data (using placeholders to avoid SQL injection)
    cursor.execute(
        "INSERT INTO students (name, grade) VALUES (?, ?)",
        ("Andrew", 85),
    )
    cursor.executemany(
        "INSERT INTO students (name, grade) VALUES (?, ?)",
        [("Bismark", 78), ("Siyabonga", 91), ("Lewis", 88)],
    )

    # Step 3: commit — without this, the inserts above are not saved
    connection.commit()

    # Read the data back
    cursor.execute("SELECT id, name, grade FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Step 4: close the connection when done
    connection.close()


if __name__ == "__main__":
    demo()
