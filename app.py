#Imports
from flask import Flask, render_template
from datetime import datetime
import uuid 
from flask import Flask, render_template, request


# --- Data Classes ---
class Book:
    def __init__(self, title, author, genre, price, stock_quantity):
        self.id = str(uuid.uuid4())  # Unique ID for each book
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.stock_quantity = stock_quantity

class Customer:
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email

class Sale:
    def __init__(self, customer, book, quantity):
        self.id = str(uuid.uuid4())
        self.customer = customer
        self.book = book
        self.quantity = quantity
        self.date = datetime.now()
        self.total_price = book.price * quantity

class ManufacturerOrder:
    def __init__(self, book_title, quantity):
        self.id = str(uuid.uuid4())
        self.book_title = book_title
        self.quantity = quantity
        self.date = datetime.now()

class Inventory:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def update_stock(self, book_title, quantity):
        book = self.find_book(book_title)
        if book:
            book.stock_quantity += quantity

    def list_inventory(self):
        for book in self.books:
            print(f"{book.title} by {book.author} | Genre: {book.genre} | Price: ${book.price} | Stock: {book.stock_quantity}")

#Creating Website
app = Flask(__name__)

registered_customers = []


#Defining Routes

#--HOMEPAGE-
@app.route('/')
def home():
    return render_template("home.html")

#--INVENTORY--
@app.route('/inventory')
def inventory_page():
    inventory = Inventory()
    inventory.add_book(Book("1984", "George Orwell", "Dystopian", 12.99, 5))
    inventory.add_book(Book("To Kill a Mockingbird", "Harper Lee", "Classic", 10.50, 3))
    inventory.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 8.99, 8))

    return render_template("inventory.html", books=inventory.books)

#--REGISTRATION--
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Check if email is already used
        for customer in registered_customers:
            if customer.email == email:
                return "Email already registered."

        new_customer = Customer(name, email)
        registered_customers.append(new_customer)
        return redirect('/login')

    return render_template('register.html')

#--LOGIN--
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        # Validate email
        for customer in registered_customers:
            if customer.email == email:
                return f"Welcome back, {customer.name}!"

        return "User not found. Please register first."

    return render_template('login.html')



#Run
if __name__ == '__main__':
    app.run(debug=True)



