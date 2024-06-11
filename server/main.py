import random
import json

# Sample lists of names and author names
book_names = [
    "The Silent Patient", "The Night Circus", "Where the Crawdads Sing", "The Goldfinch",
    "The Girl on the Train", "All the Light We Cannot See", "The Great Alone", "Educated",
    "Becoming", "The Immortalists", "The Overstory", "Circe", "Little Fires Everywhere",
    "Normal People", "Eleanor Oliphant Is Completely Fine", "An American Marriage", "Big Little Lies",
    "The Underground Railroad", "The Handmaid's Tale", "The Hunger Games", "Harry Potter and the Sorcerer's Stone",
    "The Catcher in the Rye", "To Kill a Mockingbird", "1984", "Pride and Prejudice", "The Book Thief",
    "The Fault in Our Stars", "Gone Girl", "The Road", "The Kite Runner", "Life of Pi", "The Da Vinci Code",
    "The Girl with the Dragon Tattoo", "Memoirs of a Geisha", "The Shining", "The Hobbit", "The Chronicles of Narnia",
    "A Game of Thrones", "The Maze Runner", "Divergent", "The Giver", "The Outsiders", "The Perks of Being a Wallflower",
    "The Alchemist", "Brave New World", "Lord of the Flies", "Animal Farm", "Jane Eyre", "Wuthering Heights"
]

author_names = [
    "Alex Michaelides", "Erin Morgenstern", "Delia Owens", "Donna Tartt",
    "Paula Hawkins", "Anthony Doerr", "Kristin Hannah", "Tara Westover",
    "Michelle Obama", "Chloe Benjamin", "Richard Powers", "Madeline Miller",
    "Celeste Ng", "Sally Rooney", "Gail Honeyman", "Tayari Jones", "Liane Moriarty",
    "Colson Whitehead", "Margaret Atwood", "Suzanne Collins", "J.K. Rowling",
    "J.D. Salinger", "Harper Lee", "George Orwell", "Jane Austen", "Markus Zusak",
    "John Green", "Gillian Flynn", "Cormac McCarthy", "Khaled Hosseini", "Yann Martel",
    "Dan Brown", "Stieg Larsson", "Arthur Golden", "Stephen King", "J.R.R. Tolkien",
    "C.S. Lewis", "George R.R. Martin", "James Dashner", "Veronica Roth", "Lois Lowry",
    "S.E. Hinton", "Stephen Chbosky", "Paulo Coelho", "Aldous Huxley", "William Golding",
    "Agatha Christie", "Charlotte Bronte", "Emily Bronte"
]

# Generate 50 random book entries
random_books = []

for _ in range(50):
    book = {
        "name": random.choice(book_names),
        "author_name": random.choice(author_names),
        "price": round(random.uniform(5, 100), 2),  # Random price between 5 and 100
        "stock": random.randint(1, 50),            # Random stock between 1 and 50
        "publish_year": random.randint(1900, 2024)  # Random publish year between 1900 and 2024
    }
    random_books.append(book)


data = [
  {
    "name": "To Kill a Mockingbird",
    "author_name": "Michelle Obama",
    "price": 77.27,
    "stock": 29,
    "publish_year": 2003
  }
]

for book in data:
    print(book['name'])


# Print the result as a JSON array
# print(json.dumps(random_books, indent=2))
