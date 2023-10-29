import sqlite3

def create_database_table():
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                      movieID INTEGER PRIMARY KEY,
                      movieName TEXT,
                      movieYear INTEGER,
                      imdbRating REAL
                    )''')

    conn.commit()
    conn.close()

def insert_data_into_table(data_list):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    for movie in data_list:
        cursor.execute("INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)",
                       (movie[1], movie[2], movie[3]))

    conn.commit()
    conn.close()

def search_movies():
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    while True:
        print("\nSearch Options:")
        print("1. Movie name")
        print("2. Movie year")
        print("3. Movie rating")
        print("4. STOP")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            movie_name = input("Enter the name of the movie: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
            movie = cursor.fetchone()
            if movie:
                print(f"Movie Name: {movie[1]}")
                print(f"Movie Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
            else:
                print("No such movie exists in our database.")
        elif choice == "2":
            movie_year = input("Enter the year: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
            movies = cursor.fetchall()
            if movies:
                for movie in movies:
                    print(f"Movie Name: {movie[1]}")
                    print(f"Movie Year: {movie[2]}")
                    print(f"IMDB Rating: {movie[3]}")
            else:
                print("No movies were found for that year in our database.")
        elif choice == "3":
            rating_limit = float(input("Enter the minimum rating: "))
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating_limit,))
            movies = cursor.fetchall()
            if movies:
                for movie in movies:
                    print(f"Movie Name: {movie[1]}")
                    print(f"Movie Year: {movie[2]}")
                    print(f"IMDB Rating: {movie[3]}\n")
            else:
                print("No movies at or above that rating were found in the database.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select a valid option.")

    conn.close()


with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = [line.strip().split(",") for line in file]

create_database_table()

insert_data_into_table(stephen_king_adaptations_list)

search_movies()
