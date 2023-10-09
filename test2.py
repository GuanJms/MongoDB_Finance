from test1 import Book, Borrower, \
    SearchEngine, SortEngine, BorrowingEngine
from pymongo import MongoClient

client = MongoClient()
db = client.mongo_lib
db.books.drop()
db.borrowers.drop()
# Testing book
# book_test1 = Book(db, ISBN='123', title='Introduction to MongoDB',
#                   authors=['Austin Niccum', '10Gen', 'Tim0'], page_number='899')
# book_test1.add_book()
# book_test1.add_book()
# book_test1.add_book()
#
# book_test1 = Book(db, ISBN='123123', title='Introduction to 123',
#                   authors=['10Austin Niccum', '10Gen', 'Tim1'], page_number='123')
# book_test1.add_book()
# book_test1.add_book()
#
# alice = Borrower(db=db, name='alice', username='aliceUser', phone=8122346408)
# alice.initiate()
# bob = Borrower(db=db, name='bob', username='bobUser', phone=8122346408)
# bob.initiate()
# bob = Borrower(db=db, name='bob', username='bobUse2r', phone=8122346408)
# bob.initiate()

while True:
    print("\nPlease input number for instruction.")
    print("\n1 - Add a new book(Title, Author, ISBN, #of Pages). \n"
          "1.1 - Add a exiting book by ISBN. \n"
          "2 - Delete all book(s) from library \n"
          "     2.2 - Delete one copy book from library \n"
          "     2.3 - delete one attribute from a book \n"
          "3 - Edit book information \n"
          "4 - Search by title, author, or isbn \n"
          "5 - Sort by title, author, # of pages or isbn\n"
          "6 - Add Borrower's (Name, Username, Phone) to library \n"
          "7 - Delete Borrowers from library\n"
          "8 - Search and Edit Borrower information\n"
          "9 - Search by name, username \n"
          "10 - Borrower borrows a book\n"
          "     10.1 -Borrower returns a book\n"
          "11 - Track number of books checked out by a given user\n"
          "     11.1 - Track which user has checked out a book \n"
          )
    instruction_id = input('Let us wait for user input.\n')

    if instruction_id == '1':

        ISBN = input('Please input ISBN \n')
        page_number = input('Please input page number \n')
        title = input('Please input title \n')
        authors = []
        while True:
            author_input = input('Please input one author name - or press enter to exit author inputting \n')
            if author_input == '':
                print('Input authors: ', authors)
                if len(author_input) == 0:
                    authors.append('unknown')
                    print('No author input ,set to unknown')
                break
            else:
                authors.append(author_input)
        book = Book(db, ISBN=ISBN, title=title,
                    authors=authors, page_number=page_number)
        book.add_book()

    if instruction_id == '1.1':
        ISBN = input('Please input ISBN \n')
        book = Book(db, ISBN=ISBN)
        book.add_book()

    if instruction_id == '2':
        ISBN_input = input('Please input ISBN \n')
        book = Book(db, ISBN = ISBN_input)
        book.delete_book()

    if instruction_id == '2.2':
        ISBN_input = input('Please input ISBN \n')
        book = Book(db, ISBN = ISBN_input)
        book.delete_copy_book()

    if instruction_id == '2.3':
        ISBN_input = input('Please input ISBN \n')
        attribute_input = input('Please input attribute - do not input ISBN\n')
        book = Book(db, ISBN = ISBN_input)
        book.remove_attribute(attribute=attribute_input)

    if instruction_id == '3':
        ISBN_input = input('Please input ISBN\n')
        book = Book(db, ISBN = ISBN_input)
        print(book)

        while True:
            if not book.editable: break
            print('Input instruction ID \n'
                  '1 - new title \n'
                  '2 - new author \n'
                  '3 - remove author \n'
                  '4 - new ISBN \n'
                  'exit - exit')

            temp = input('Please input instructionID\n')
            if temp == '1':
                input_value = input('Please input new title value \n')
                book.edit({'title' : input_value})
            if temp == '2':
                input_value = input('Please input new author value\n')
                book.add_author(input_value)
            if temp == '3':
                input_value = input('Please input remove author value\n')
                book.remove_author(input_value)

            if temp == '4':
                input_value = input('Please input new ISBN value\n')
                book.edit({'ISBN': input_value})

            if temp == 'exit':
                print(book)
                break

    if instruction_id == '4':
        while True:
            print('\n1 - search by title \n'
                  '2 - search by author \n'
                  '3 - search by ISBN \n'
                  '4 - search by page number \n'
                  'exit - exit\n')

            search_instuction_ID = input("Input search instruction ID \n")
            if search_instuction_ID == '1':
                input_value = input('Input search title value \n')
                searchBook = SearchEngine(db, 'books', title = input_value)
                searchBook.get_result()

            if search_instuction_ID == '2':
                input_value = input('Input search author value \n')
                searchBook = SearchEngine(db, 'books')
                searchBook.search_by_authors([input_value])
                searchBook.get_result()

            if search_instuction_ID == '3':
                input_value = input('Input ISBN value \n')
                searchBook = SearchEngine(db,'books', ISBN = input_value)
                searchBook.get_result()

            if search_instuction_ID == '4':
                input_value = input('Input page number value \n')
                searchBook = SearchEngine(db,'books', page_number = input_value)
                searchBook.get_result()

            if search_instuction_ID == 'exit':
                break

    if instruction_id == '5':
        while True:
            print('1 - sort by title \n'
                  '2 - sort by author \n'
                  '3 - sort by page number \n'
                  '4 - sort by ISBN\n'
                  'exit - exit\n')

            sort_instruction_id = input('Input sort instruction ID\n')

            if sort_instruction_id == '1':
                sort_book = SortEngine(db, 'books', attribute= 'title')
                sort_book.get_result()

            if sort_instruction_id == '2':
                sort_book = SortEngine(db, 'books', attribute= 'authors')
                sort_book.get_result()

            if sort_instruction_id == '3':
                sort_book = SortEngine(db, 'books', attribute= 'page_number')
                sort_book.get_result()

            if sort_instruction_id == '4':
                sort_book = SortEngine(db, 'books', attribute='ISBN')
                sort_book.get_result()

            if sort_instruction_id == 'exit':
                break

    if instruction_id == '6':
        while True:
            borrower_name = input('Input borrower name \n')
            borrower_username = input('Input borrower username \n')
            borrower_phone_number = input('Input borrower phone number \n')
            borrower = Borrower(db=db, name = borrower_name, username=borrower_username, phone=borrower_phone_number)
            borrower.initiate()

            exit_flag = input('exit - exit otherwise press any \n')
            if exit_flag == 'exit':
                break

    if instruction_id == '7':
        while True:
            borrower_name = input('Input borrower name to delete (or type exit)\n')
            if borrower_name == 'exit': break
            borrower_username = input('Input borrower username to delete (or type exit)\n')
            if borrower_username =='exit':break
            else:
                borrower = Borrower(db, borrower_name,borrower_username,search_user=True)
                borrower.delete_borrower()

    if instruction_id == '8':
        while True:
            borrower_name = input('Input borrower name to edit (or type exit)\n')
            if borrower_name == 'exit': break
            borrower_username = input('Input borrower username to edit (or type exit)\n')
            if borrower_username =='exit':break
            borrower = Borrower(db, borrower_name,borrower_username,search_user=True)
            if not borrower.connected: break

            while True:
                print("\n1 - edit name \n"
                      "2 - edit username \n"
                      "3 - edit name and username \n"
                      "4 - edit phone number\n"
                      "exit - exit\n")

                edit_instrunctionID = input('Input edit instruction ID\n')
                if edit_instrunctionID == '1':
                    input_value = input('Input new name\n')
                    borrower.edit(name = input_value)

                if edit_instrunctionID == '2':
                    input_value = input('Input new username\n')
                    borrower.edit(username = input_value)

                if edit_instrunctionID == '3':
                    input_value_name = input('Input new name\n')
                    input_value_username = input('Input new username\n')
                    borrower.edit(name= input_value_name, username= input_value_username)

                if edit_instrunctionID == '4':
                    input_value = input('Input new phone\n')
                    borrower.edit(phone = input_value)

                print("Current borrower Info: ", print(borrower))

                if edit_instrunctionID == 'exit': break

    if instruction_id == '9':
        while True:
            print("\n1 - search by name \n"
                  "2 - search by username \n"
                  "exit - exit\n")

            search_attribute = input('Input search attribute id \n')
            input_value = input('Input search value \n')
            if search_attribute == 'exit':
                break
            if search_attribute == '1':
                search_user = SearchEngine(db, 'borrowers', user_search=True, name=input_value)
                search_user.get_result()
            elif search_attribute == '2':
                search_user = SearchEngine(db, 'borrowers', user_search=True, username=input_value)
                search_user.get_result()

    if instruction_id == '10':
        name = input('Input borrower name\n')
        username = input('Input borrower name\n')
        borrower = Borrower(db=db, name=name, username=username,search_user=True)
        if borrower.connected:
            ISBN = input('Input book ISBN\n')
            book = Book(db, ISBN)
            borrower_engine = BorrowingEngine(borrower=borrower, book=book)
            borrower_engine.borrow_action()

    if instruction_id == '10.1':
        name = input('Input borrower name\n')
        username = input('Input borrower username\n')
        borrower = Borrower(db=db, name=name, username=username,search_user=True)
        if borrower.connected:
            ISBN = input('Input book ISBN\n')
            book = Book(db, ISBN)
            borrower_engine = BorrowingEngine(borrower=borrower, book=book)
            borrower_engine.return_action(ISBN=ISBN)

    if instruction_id == '11':
        name = input('Input borrower name\n')
        username = input('Input borrower username\n')
        borrower = Borrower(db=db, name=name, username=username,search_user=True)
        if borrower.connected:
            print(f"User {name}, {username} has {borrower.get_checked_book_num()}")

    if instruction_id == '11.1':
        ISBN = input('Input book ISBN\n')
        book = Book(db, ISBN)
        if not book.addable:
            print("Current User list are: ",book.get_borrowers())