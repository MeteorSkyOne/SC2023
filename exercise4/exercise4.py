import sqlite3
from sqlite3 import Error
import datetime

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('library.db')  # You can replace ':memory:' with 'library.db' to persist the database.
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def create_tables(connection):
    create_books_table = """
    CREATE TABLE IF NOT EXISTS Books (
      BookID TEXT PRIMARY KEY,
      Title TEXT NOT NULL,
      Author TEXT NOT NULL,
      ISBN TEXT NOT NULL,
      Status TEXT NOT NULL
    );
    """

    create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
      UserID TEXT PRIMARY KEY,
      Name TEXT NOT NULL,
      Email TEXT NOT NULL
    );
    """

    create_reservations_table = """
    CREATE TABLE IF NOT EXISTS Reservations (
      ReservationID TEXT PRIMARY KEY,
      BookID TEXT NOT NULL,
      UserID TEXT NOT NULL,
      ReservationDate TEXT NOT NULL,
      FOREIGN KEY (BookID) REFERENCES Books (BookID),
      FOREIGN KEY (UserID) REFERENCES Users (UserID)
    );
    """

    execute_query(connection, create_books_table)
    execute_query(connection, create_users_table)
    execute_query(connection, create_reservations_table)


def menu():
    print("\n1. Add a new book to the database.")
    print("2. Find a book’s detail based on BookID.")
    print("3. Find a book’s reservation status.")
    print("4. Find all the books in the database.")
    print("5. Modify / update book details.")
    print("6. Delete a book based on its BookID.")
    print("7. Exit")


def add_book(connection):
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    query = f"""
    INSERT INTO
      Books (BookID, Title, Author, ISBN, Status)
    VALUES
      ('{book_id}', '{title}', '{author}', '{isbn}', '{status}');
    """
    execute_query(connection, query)


def find_book_details(connection):
    book_id = input("Enter BookID: ")

    query = f"""
    SELECT
      Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
    FROM
      Books
    LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
    LEFT JOIN Users ON Reservations.UserID = Users.UserID
    WHERE
      Books.BookID = '{book_id}';
    """

    results = execute_read_query(connection, query)

    if results:
        for result in results:
            print(result)
    else:
        print("No such book exists.")


def find_reservation_status(connection):
    identifier = input("Enter BookID, Title, UserID, or ReservationID: ")

    if identifier.startswith("LB"):
        condition = f"Books.BookID = '{identifier}'"
    elif identifier.startswith("LU"):
        condition = f"Users.UserID = '{identifier}'"
    elif identifier.startswith("LR"):
        condition = f"Reservations.ReservationID = '{identifier}'"
    else:
        condition = f"Books.Title = '{identifier}'"

    query = f"""
    SELECT
      Books.BookID, Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
    FROM
      Books
    LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
    LEFT JOIN Users ON Reservations.UserID = Users.UserID
    WHERE
      {condition};
    """

    results = execute_read_query(connection, query)

    if results:
        for result in results:
            print(result)
    else:
        print("No such book/reservation/user exists.")


def find_all_books(connection):
    query = """
    SELECT
      Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
    FROM
      Books
    LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
    LEFT JOIN Users ON Reservations.UserID = Users.UserID;
    """

    results = execute_read_query(connection, query)

    if results:
        for result in results:
            print(result)


def update_book_details(connection):
    book_id = input("Enter BookID: ")
    choice = input("Enter '1' to modify book details, '2' to modify reservation status: ")

    if choice == '1':
        title = input("Enter new Title (Leave blank for no change): ")
        author = input("Enter new Author (Leave blank for no change): ")
        isbn = input("Enter new ISBN (Leave blank for no change): ")
        status = input("Enter new Status (Leave blank for no change): ")

        if not title and not author and not isbn and not status:
            print("No changes made.")
            return

        update_queries = []

        if title:
            update_queries.append(f"Title = '{title}'")
        if author:
            update_queries.append(f"Author = '{author}'")
        if isbn:
            update_queries.append(f"ISBN = '{isbn}'")
        if status:
            update_queries.append(f"Status = '{status}'")

        update_query = ", ".join(update_queries)

        query = f"""
        UPDATE
          Books
        SET
          {update_query}
        WHERE
          BookID = '{book_id}';
        """

        execute_query(connection, query)

    elif choice == '2':
        status = input("Enter new Status: ")
        user_id = input("Enter UserID (Leave blank for no change): ")
        reservation_date = input("Enter ReservationDate (Leave blank for no change): ")

        book_update_query = f"""
        UPDATE
          Books
        SET
          Status = '{status}'
        WHERE
          BookID = '{book_id}';
        """

        execute_query(connection, book_update_query)

        if user_id and reservation_date:
            reservation_update_query = f"""
            UPDATE
              Reservations
            SET
              UserID = '{user_id}', ReservationDate = '{reservation_date}'
            WHERE
              BookID = '{book_id}';
            """

            execute_query(connection, reservation_update_query)


def delete_book(connection):
    book_id = input("Enter BookID: ")

    reservation_delete_query = f"""
    DELETE FROM Reservations WHERE BookID = '{book_id}';
    """
    execute_query(connection, reservation_delete_query)

    book_delete_query = f"""
    DELETE FROM Books WHERE BookID = '{book_id}';
    """
    execute_query(connection, book_delete_query)
    print(f"Book with BookID {book_id} and its reservations have been deleted.")


def main():
    connection = create_connection()
    create_tables(connection)

    while True:
        menu()

        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_book(connection)
        elif choice == '2':
            find_book_details(connection)
        elif choice == '3':
            find_reservation_status(connection)
        elif choice == '4':
            find_all_books(connection)
        elif choice == '5':
            update_book_details(connection)
        elif choice == '6':
            delete_book(connection)
        elif choice == '7':
            connection.close()
            print("Connection closed successfully.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()

