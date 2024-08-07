from datetime import datetime, timedelta

# Define the Book class
class Book:
    def __init__(self, title, author, genre, quantity):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__quantity = quantity

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_genre(self):
        return self.__genre

    def get_quantity(self):
        return self.__quantity

    def increase_quantity(self, amount):
        self.__quantity += amount

    def decrease_quantity(self):
        if self.__quantity > 0:
            self.__quantity -= 1

    def __str__(self):
        return f"Title: {self.__title}, Author: {self.__author}, Genre: {self.__genre}, Quantity: {self.__quantity}"

# Define the Member class
class Member:
    def __init__(self, member_id, name):
        self.__member_id = member_id
        self.__name = name
        self.__rented_books = []

    def get_member_id(self):
        return self.__member_id

    def get_name(self):
        return self.__name

    def get_rented_books(self):
        return self.__rented_books

    def rent_book(self, book):
        if book.get_quantity() > 0:
            self.__rented_books.append(book)
            book.decrease_quantity()
        else:
            print(f"Book '{book.get_title()}' is out of stock.")

    def return_book(self, book):
        if book in self.__rented_books:
            self.__rented_books.remove(book)
            book.increase_quantity(1)

    def __str__(self):
        return f"Member ID: {self.__member_id}, Name: {self.__name}, Rented Books: {[book.get_title() for book in self.__rented_books]}"

# Define the Rental class
class Rental:
    def __init__(self, book, member):
        self.__book = book
        self.__member = member
        self.__rented_on = datetime.now()
        self.__due_date = self.__rented_on + timedelta(days=10)
        self.__returned_on = None

    def get_due_date(self):
        return self.__due_date

    def get_returned_on(self):
        return self.__returned_on

    def set_returned_on(self, returned_on):
        self.__returned_on = returned_on

    def get_rented_on(self):
        return self.__rented_on

    def is_late(self):
        return self.__returned_on and self.__returned_on > self.__due_date

    def calculate_fee(self):
        if self.is_late():
            late_days = (self.__returned_on - self.__due_date).days
            return late_days * 5.0  # $5 per day
        return 0.0

    def __str__(self):
        return (f"Book: {self.__book.get_title()}, Member: {self.__member.get_name()}, "
                f"Rented On: {self.__rented_on}, Due Date: {self.__due_date}, Returned On: {self.__returned_on}")

# Define the Library class
class Library:
    def __init__(self):
        self.__books = []
        self.__members = []
        self.__rented_books = []

    def add_book(self, book):
        self.__books.append(book)

    def increase_book_count(self, book_title, quantity):
        for book in self.__books:
            if book.get_title() == book_title:
                book.increase_quantity(quantity)
                break

    def search_book(self, title, author="", genre=""):
        for book in self.__books:
            if (book.get_title() == title and
                (author == "" or book.get_author() == author) and
                (genre == "" or book.get_genre() == genre)):
                return book
        return None

    def add_member(self, member):
        self.__members.append(member)

    def rent_book(self, book_title, member_id):
        book = self.search_book(book_title)
        if book and book.get_quantity() > 0:
            for member in self.__members:
                if member.get_member_id() == member_id:
                    rental = Rental(book, member)
                    self.__rented_books.append(rental)
                    member.rent_book(book)
                    print(f"Book '{book_title}' rented successfully. Due date: {rental.get_due_date()}")
                    return  # Exit after successful rental
        else:
            print(f"Book '{book_title}' is not available.")

    def get_rental_status(self):
        return [str(rental) for rental in self.__rented_books]

    def evaluate_late_fee(self, days_late):
        return days_late * 5.0  # $5 per day for late returns

# Define the menu system
def library_menu(library):
    while True:
        print("\nLibrary Man Menu:")
        print("1. Add Book")
        print("2. Increase Book Count")
        print("3. Add Member")
        print("4. Exit")

        choice = input("Select an option: ").strip()
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author: ")
            genre = input("Enter genre: ")
            quantity = int(input("Enter quantity: "))
            book = Book(title, author, genre, quantity)
            library.add_book(book)
            print("Book added successfully.")
        elif choice == '2':
            title = input("Enter book title: ")
            quantity = int(input("Enter quantity to add: "))
            library.increase_book_count(title, quantity)
            print("Book count increased successfully.")
        elif choice == '3':
            member_id = int(input("Enter member ID: "))
            name = input("Enter member name: ")
            member = Member(member_id, name)
            library.add_member(member)
            print("Member added successfully.")
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

def member_menu(library):
    while True:
        member_id = int(input("Enter your member ID: "))
        member = next((m for m in library._Library__members if m.get_member_id() == member_id), None)
        if not member:
            print("Member not found.")
            continue

        while True:
            print("\nMember Menu:")
            print("1. Rent Book")
            print("2. Search Book")
            print("3. View Rented Books")
            print("4. Back to Library Man Menu")
            print("5. Exit")

            choice = input("Select an option: ").strip()
            if choice == '1':
                title = input("Enter book title to rent: ")
                library.rent_book(title, member_id)
            elif choice == '2':
                title = input("Enter book title to search: ")
                book = library.search_book(title)
                if book:
                    print(f"Book Details - Title: {book.get_title()}, Author: {book.get_author()}, Genre: {book.get_genre()}, Quantity: {book.get_quantity()}")
                else:
                    print("Book not found.")
            elif choice == '3':
                if not member.get_rented_books():
                    print("No rented books.")
                else:
                    for book in member.get_rented_books():
                        rental = next((r for r in library._Library__rented_books if r._Rental__book == book and r._Rental__member == member), None)
                        if rental:
                            print(f"Rented Book - Title: {book.get_title()}, Author: {book.get_author()}, Genre: {book.get_genre()}, Quantity: {book.get_quantity()}")
                            print(f"Rental Date: {rental.get_rented_on()}, Due Date: {rental.get_due_date()}")
                            if rental.is_late():
                                days_late = (datetime.now() - rental.get_due_date()).days
                                print(f"Late Fee: ${rental.calculate_fee()} (Overdue by {days_late} days)")
                            else:
                                print("No late fee.")
            elif choice == '4':
                return  # Return to the library man menu
            elif choice == '5':
                exit()  # Exit the program
            else:
                print("Invalid option. Please try again.")
def main():
    library = Library()

    while True:
        role = input("Are you a 'library man' or 'member'? ").strip().lower()
        if role == 'library man':
            library_menu(library)
        elif role == 'member':
            if not library._Library__members:
                print("No members exist. Please add members through the library man menu.")
            else:
                member_menu(library)
        else:
            print("Invalid role. Please enter 'library man' or 'member'.")

if __name__ == "__main__":
    main()
