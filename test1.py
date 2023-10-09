from pymongo import MongoClient


class Book:
	def __init__(self, db, ISBN, **kargs):
		self.title = kargs.get('title')
		self.authors = kargs.get('authors')
		self.page_number = kargs.get('page_number')
		self.conflicting_info_list = []
		self.db = db
		self.ISBN = ISBN
		self.params = kargs
		self.copynum = None
		self.stocknum = None
		self.borrowers = None

		self.addable = False  # a book is addable iif there is no corresponding ISBN
		self.editable = False
		self.conflicting = False
		self.deletable = False
		self.avail_to_borrower= False
		self.checkable = False

		self.update()
		self.printStatus()

	def __str__(self):
		self.update()
		if self.addable:
			return f"[Error] -- Book ISBN - {self.ISBN} does not exist in the library"
		elif self.conflicting:
			return f"[Error] -- Bad conflicting class input - Invalid Class"
		else:
			return f"[Book information] -- title: {self.title}; authors: {self.authors}; ISBN: {self.ISBN}; " \
				   f"Number Page: {self.page_number}; copies left: {self.get_field('copynum')}"

	def get_borrowers(self):
		self.update()
		if self.addable:
			print(f"[Error] -- Book ISBN - {self.ISBN} does not exist in the library")
			return

		beautiful_list = []
		for b in self.borrowers:
			if len(b.keys())!= 0:
				beautiful_list.append(b)
		return beautiful_list

	def return_book(self):
		self.update()
		if self.addable:
			print(f"[Error] -- Book ISBN - {self.ISBN} does not exist in the library")
			return
		else:
			self.db.books.update_one({"ISBN": self.ISBN},
									 {"$inc": {"stocknum":1}})


	def check_to_borrower(self):
		self.update()
		if self.addable:
			print(f"No such book ISBN-{self.ISBN}")
			return
		if self.conflicting:
			print(f"Conflicting input in check_to_borrower")
		if self.stocknum == 0:
			self.checkable = False
		else:
			self.checkable = True


	def check_addable(self):
		data = self.db.books.find_one({'ISBN': str(self.ISBN)})
		if data == None:
			self.addable = True  # ISBN is available; the book is addable
		else:
			self.addable = False

	def remove_attribute(self, attribute):
		if attribute == "ISBN":
			print("[Removing Attribute Error] Request to remove ISBN - Bad request failed")
		elif attribute == "copynum":
			print("[Removing Attribute Error] Request to remove copynum - Bad request failed")
		elif attribute == "stocknum":
			print("[Removing Attribute Error] Request to remove copynum - Bad request failed")
		elif attribute == "authors":
			self.db.books.update_one({"ISBN": self.ISBN}, {"$unset": {"authors": 1}})
			print(f"[Removing Attribute] removed authors from ISBN {self.ISBN}")
		elif attribute == "title":
			self.db.books.update_one({"ISBN": self.ISBN}, {"$unset": {"title": 1}})
			print(f"[Removing Attribute] removed title from ISBN {self.ISBN}")
		elif attribute == "page_number":
			self.db.books.update_one({"ISBN": self.ISBN}, {"$unset": {"page_number": 1}})
			print(f"[Removing Attribute] removed page_number from ISBN {self.ISBN}")
		else:
			print("[Removing Attribute] No attribute recognized")

	def update(self):
		self.check_addable()
		if self.addable == False:
			info = db.books.find_one({'ISBN': str(self.ISBN)})
			title = info.get('title')
			authors = info.get('authors')
			page_number = info.get('page_number')
			borrowers_unique = db.books.distinct( "borrowers",{'ISBN': str(self.ISBN)})
			borrowers = borrowers_unique

			for (key, value) in self.params.items():
				if key in info.keys():
					if key == 'authors':
						if set(value) != set(info.get('authors')):
							self.conflicting = True
							conflicting_info = f"Conflicting in {key}: exiting info -> {info.get(key)}; input -> {value}"
							self.conflicting_info_list.append(conflicting_info)
					# print(conflicting_info)
					else:
						if value != info.get(key):
							self.conflicting = True
							conflicting_info = f"Conflicting in {key}: exiting info -> {info.get(key)}; input -> {value} "
							self.conflicting_info_list.append(conflicting_info)
			# print(conflicting_info)

			self.title = title
			self.authors = authors
			self.page_number = page_number
			self.borrowers = borrowers
			self.deletable = True
			self.copynum = self.get_field('copynum')
			self.stocknum = self.get_field('stocknum')
			if not self.conflicting:
				self.editable = True
		else:
			self.deletable = False

	def get_field(self, fieldName):
		if self.conflicting:
			return "Invalid Class conflicting input"
		data = self.db.books.find_one({'ISBN': str(self.ISBN)})
		if data == None: return 0
		field = data.get(fieldName)
		return field



	def add_book(self):
		self.update()
		if not self.addable:  # not addable; i.e. there is exiting book
			if self.conflicting:
				print(
					f"[Adding a book] -- Found an exiting ISBN {self.ISBN}; Found conflicting information from input ->")
				print(self.conflicting_info_list)
				return False
			else:
				print(f"[Adding a book] -- There is exiting book associated with {self.ISBN}")
				self._add_book_()
				return False
		else:
			self._add_book_()

	def _add_book_(self):  # self.addable is True; i.e. you can add into the library; no book in the library
		if self.addable:
			if self.title == None:
				print(f"[Error] --  Missing title")
				return
			if self.ISBN == None:
				print(f"[Error] --  Missing ISBN")
				return
			if self.authors == None:
				print(f"[Error] -- Missing authors")
				return

			if self.page_number == None:
				print(f"[Error] Missing page number")
				return

			book_json = (
				{
					'title': self.title,
					'ISBN': self.ISBN,
					'authors': self.authors,
					'page_number': self.page_number,
					'copynum': 1,
					'stocknum': 1
				}
			)

			self.db.books.insert_one(book_json)

			print("Successfully added a new book with a new ISBN")
			self.update()
			print(self.__str__())
		else:
			self.db.books.update_one({"ISBN": self.ISBN},
									 {"$inc": {"copynum": 1, "stocknum":1}})

			print("Successfully added a copy book")
			self.update()
			print(self.__str__())

	def delete_book(self):
		if self.conflicting:
			print("Conflicting info - Invalid Class")
			return

		if not self.deletable:
			print(f"[Error] -- Book ISBN -{self.ISBN} cannot be delete")
			return
		self.db.books.delete_one({"ISBN": self.ISBN})
		print(f"Successfully deleted all book(s) for ISBN - {self.ISBN}")

	def delete_copy_book(self, output_copy_num=False):
		if self.conflicting:
			print("Conflicting info - Invalid Class")
			return

		if self.deletable:
			if self.get_field('copynum') == 1:
				print("Only one copy left")
				self.delete_book()
			else:
				self.db.books.update_one({"ISBN": self.ISBN},
										 {"$inc": {"copynum": -1,"stocknum": -1}})
				print(f"Successfully deleted one copy book for ISBN - {self.ISBN}")
		if output_copy_num:
			print(self.__str__())

	def printStatus(self):
		if self.addable:
			print(f"[Book Class Status] -- {self.ISBN} does not exit in the library")
		if self.conflicting:
			print(
				f"[Book Class Status] -- {self.ISBN} exists; and input information has conflicting context: {self.conflicting_info_list}")

	def ISBN_available(self, newISBN):
		data = self.db.books.find_one({'ISBN': str(newISBN)})
		if data == None:
			return True  # ISBN is available;
		else:
			return False

	def edit(self, kwarg: dict):
		for (k, v) in kwarg.items():
			if k == "ISBN":
				if v == self.ISBN:
					print("[Duplicate Editting on ISBN] -- OMG! Super Stress Test")
					return
				if self.ISBN_available(newISBN=v):
					self.db.books.update_one({"ISBN": self.ISBN},
											 {"$set": {k: v}})
					self.ISBN = v
				else:
					print(f"[Error] -- new ISBN {v} is not available!")
			else:
				self.db.books.update_one({"ISBN": self.ISBN},
										 {"$set": {k: v}})


	def add_author(self, author):
		self.db.books.update_one({"ISBN": self.ISBN}, {"$addToSet": {"authors": author}})
		return

	def remove_author(self, author):
		self.db.books.update_one({"ISBN": self.ISBN}, {"$pull": {"authors": author}})

	def add_borrower(self, name, username):
		self.db.books.update_one({"ISBN": self.ISBN}, {"$push": { "borrowers": {"name": name, "username":username }}})
		pass

	def remove_borrower(self, name, username):
		borrowers = db.books.find_one({'ISBN': str(self.ISBN)}).get('borrowers')
		print(borrowers)
		self.db.books.update_one({"ISBN": self.ISBN, "borrowers.name": name, "borrowers.username":username},
									 {"$unset": {"borrowers.$.name":1, "borrowers.$.username":1}}
									, False)

		# print(self.db.books.find_one({"ISBN": self.ISBN, "borrowers.name": name, "borrowers.username":username}))
		print("***")
		borrowers = db.books.find_one({'ISBN': str(self.ISBN)}).get('borrowers')
		print(borrowers)
		pass


class Borrower:
	def __init__(self, db, name, username, phone=None, search_user=False, output_connect = True):
		self.addable = False
		self.connected = False
		self.book_list = []
		self.name = name
		self.username = username
		self.phone = phone
		self.db = db
		if search_user:
			if self.get_borrower_info():
				self.connected = True
				if output_connect:print(f"[Borrower Connected] - {self.__str__()}")
			else:
				self.connected = False
				print(f"[Error] user does not exist")
		else:
			if name is None or name == '':
				print("[Borrower Class - Error] no name input")
				raise ValueError
			if username is None or username == '':
				print("[Borrower Class - Error] no username input")
				raise ValueError
			if phone is None or phone == '':
				print("[Borrower Class - Error] no phone input")
				raise ValueError
			self.check_addable()

	def add_to_booklist(self, ISBN):
		self.get_borrower_info()
		if not self.connected:
			print("[Add to booklist] Unconnected User")
			return
		if ISBN is None or ISBN == '':
			print("[Add to booklist] invalid ISBN ")
			return
		self.book_list.append(ISBN)
		self.db.books.update_one({"ISBN": ISBN},
									 {"$inc": {"stocknum": -1}})
		self.db.borrowers.update_one({"name": self.name, "username" : self.username},
									 {"$push": {"book_list": ISBN}})

		print(f"Add book ISBN - {ISBN} to Borrower {self.name}, {self.username}")

	def get_checked_book_num(self):
		self.get_borrower_info()
		if not self.connected:
			print(f"[Error] user {self.name}, {self.username} not connected")
			return
		return len(self.book_list)

	def get_borrower_info(self):
		info = self.db.borrowers.find_one({"name": self.name, "username": self.username})
		if info == None:
			print("[Error] no such pair or user and username")
			return False
		else:
			self.name = info.get('name')
			self.username = info.get('username')
			self.phone = info.get('phone')
			self.book_list = info.get('book_list')
			return True

	def edit(self, name=None, username=None, phone=None):
		if not self.connected:
			print("[Error] Borrower Class not connected - edit failed")
			return
		if name is not None and username is not None:
			if self.check_addable(name=name, username=username):
				if phone is not None:
					self.phone = phone
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": name, "username": username, "phone": phone}})
				else:
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": name, "username": username}})
				self.name = name
				self.username = username
				print("[Edit Borrower] - information updated")
				return
			else:
				print("[Error] - exiting pair input")
				return
		elif name is not None:
			if self.check_addable(name=name):
				if phone is not None:
					self.phone = phone
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": name, "username": self.username,
														   "phone": phone}})
				else:
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": name, "username": self.username}})
				self.name = name
				print("[Edit Borrower] - information updated")
				return
			else:
				print("[Error] - exiting pair input")
				return
		elif username is not None:
			if self.check_addable(username=username):
				if phone is not None:
					self.phone = phone
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": self.name, "username": username,
														   "phone": phone}})
				else:
					self.db.borrowers.update_one({"name": self.name, "username": self.username},
												 {"$set": {"name": self.name, "username": username}})
				self.username = username
				print("[Edit Borrower] - information updated")
				return
			else:
				print("[Error] - exiting pair input")
				return
		elif phone is not None:
			self.phone = phone
			self.db.borrowers.update_one({"name": self.name, "username": self.username},
										 {"$set": {"phone": phone}})
			print("[Edit Borrower] - information updated")
			return
		else:
			print("[Error] - update edit error")
			return

	def __str__(self):
		if not self.connected:
			return f"[Borrower Information] - name: {self.name}; username: {self.username} is not connected "
		else:
			return f"[Borrower Information] - name: {self.name}; username: {self.username}; phone: {self.phone}"

	def initiate(self):
		self.check_addable()
		if not self.addable:
			print("[Initiate] Borrower class is no addable")
			return
		borrower_json = (
			{
				'name': self.name,
				'username': self.username,
				'phone': self.phone,
				'book_list': self.book_list
			}
		)
		self.db.borrowers.insert_one(borrower_json)
		self.connected = True
		print(
			f"[Initiated Borrower] - successfully added a user - name: {self.name}, username: {self.username}, phone: {self.phone}")

	def check_addable(self, name=None, username=None):
		if name is not None and username is not None:
			num = self.db.borrowers.count_documents({"name": name, "username": username})
			if num == 0:
				return True
			else:
				print("[Check exiting (name, username)] the pair exits. Choose other pair")
				return False
		elif name is not None:
			num = self.db.borrowers.count_documents({"name": name, "username": self.username})
			if num == 0:
				# valid pair
				return True
			else:
				print("[Check exiting (name, username)] the pair exits. Choose other pair")
				return False
		elif username is not None:
			num = self.db.borrowers.count_documents({"name": self.name, "username": username})
			if num == 0:
				# valid pair
				return True
			else:
				print("[Check exiting (name, username)] the pair exits. Choose other pair")
				return False
		else:
			num = self.db.borrowers.count_documents({"name": self.name, "username": self.username})
			if num == 0:
				# print(self.__str__())
				self.addable = True
			# print("[Check exiting (name, username)] the pair is available")
			else:
				self.addable = False
				print("[Check exiting (name, username)] the pair exits. Choose other pair")

	def delete_borrower(self):
		if not self.connected:
			print("[Error] user is not connected or user does not exist")
			return
		else:
			self.db.borrowers.delete_one({"name": self.name, "username": self.username})
			self.connected = False
			print(f"[Delete user] - User {self.name}, {self.username} is deleted")


class SearchEngine:
	def __init__(self, db, collection, user_search=False, **kargs):
		self.db = db
		self.collection = collection
		self.cursor = db[collection].find(kargs)
		self.user_search = user_search

	def search_by_authors(self, authors):
		self.cursor = self.db[self.collection].find({"authors": {"$in": authors}})

	def get_result(self):
		if not self.user_search:
			for data in self.cursor:
				print("[Search Result]", Book(self.db, data.get('ISBN')))
		else:
			for data in self.cursor:
				print("[Search Result]", Borrower(self.db, name=data.get('name'),
												  username=data.get('username'),
												  search_user=True, output_connect=False))


class SortEngine:
	def __init__(self, db, collection, attribute):
		self.db = db
		self.collection = collection
		self.cursor = db[collection].find().sort(attribute)

	def get_result(self):
		i = 0
		for data in self.cursor:
			print("[Search Result- ", i, " ]", Book(self.db, data.get('ISBN')))
			i = i + 1

class BorrowingEngine:
	def __init__(self, borrower: Borrower, book: Book):
		self.borrower = borrower
		self.book = book

	def borrow_action(self, book: Book = None):
		if book is not None:
			self.book = book
		self.book.check_to_borrower()
		if self.book.checkable:
			#add to user list
			# print(self.book.ISBN)
			self.book.add_borrower(self.borrower.name, self.borrower.username)
			self.borrower.add_to_booklist(ISBN=self.book.ISBN)
			print(f"[Borrow Action] successfully borrowed the book {self.book.ISBN}")
		else:
			print(f"No available book for {self.book.ISBN}")

	def return_action(self, ISBN = None, book :Book = None):
		if not self.borrower.connected:
			print("[Return Action] Failed to return; borrower is not connneted")
			return
		if ISBN is not None:
			self.book = Book(self.borrower.db, ISBN)
			self.borrower.get_borrower_info()
			if ISBN in self.borrower.book_list:
				book_temp = Book(self.borrower.db, ISBN= ISBN)
				self.borrower.book_list.remove(ISBN)
				book_temp.return_book()
				self.borrower.db.borrowers.update_one({"name" : self.borrower.name, "username":self.borrower.username},
											 {"$set" : { "book_list" : self.borrower.book_list}})
				self.book.remove_borrower(self.borrower.name, self.borrower.username)

				print(f"[Return Action] Successfully returned book ISBN - {ISBN}")
			else:
				print(f"[Return Action] User did not borrow- {ISBN}")

		elif book is not None:
			self.borrower.get_borrower_info()
			if book.ISBN in self.borrower.book_list:
				self.borrower.book_list.remove(book.ISBN)
				self.book.return_book()
				self.borrower.db.borrowers.update_one({"name" : self.borrower.name, "username":self.borrower.username},
											 {"$set" : { "book_list" : self.borrower.book_list}})

				print(f"[Return Action] Successfully returned book ISBN - {self.book.ISBN}")
		else:
			self.borrower.get_borrower_info()
			if self.book.ISBN in self.borrower.book_list:
				self.borrower.book_list.remove(self.book.ISBN)
				self.book.return_book()
				self.borrower.db.borrowers.update_one({"name" : self.borrower.name, "username":self.borrower.username},
											 {"$set" : { "book_list" : self.borrower.book_list}})

				print(f"[Return Action] Successfully returned book ISBN - {self.book.ISBN}")




# document_number = db.books.count_documents({'ISBN': '9991-1021-2002'})
client = MongoClient()
db = client.mongo_lib
db.books.drop()
db.borrowers.drop()
# book_test = Book(db, '9991-1021-2002')
book_test1 = Book(db, ISBN='9991-1021-2002', title='Introduction to MongoDB',
				  authors=['Austin Niccum', '10Gen', 'Tim Hawkins'], page_number=899)
book_test1.add_book()
book_test1.add_book()
book_test1.add_book()
book_test1.add_book()
book_test1.add_book()
# book_test1.add_book()
# book_test1.add_book()
# book_test1.add_book()
# book_test1.delete_book()
# book_test1.delete_copy_book()
# book_test1.delete_copy_book()
# book_test1.delete_copy_book()
# book_test1.delete_copy_book()

# book_test = Book(db, ISBN = '9991-1021-2002', title = 'Introduction to MongoDB')
# book_test = Book(db, ISBN = '9991-1021-2002', page_number= 29)
# book_test = Book(db, ISBN = '9991-1021-2002', authors= ['jimuwhat'])
book_test2 = Book(db, ISBN='9999-1002-2005', title='Introduction to PDE', authors=['Austin Niccum', 'James Guan'],
				  page_number=233)
book_test2.add_book()

book_test3 = Book(db, ISBN='9999-1332-2005', title='Introduction to PDE', authors=['Austin Niccum', 'James Guan'],
				  page_number=233)
book_test3.add_book()
# book_test4 = Book(db, ISBN='9999-1232-2305', title='Introduction to PDE', authors=['Austin Niccum', 'Jimusi Guan'],
#                   page_number=233)
# book_test4.add_book()
# book_test5 = Book(db, ISBN='9999-1232-2399', title='ZZZZZ', authors=['A0', 'aaa'], page_number=23)
# book_test5.add_book()
# book_test6 = Book(db, ISBN='1001-1232', title='ZZZZZ', authors=['zzz12'], page_number=23)
# book_test6.add_book()

# book_test2 = Book(db, ISBN = '9999-1002-2005')
# book_test2 = Book(db, ISBN = '119')

# book_test1.add_book()
#
# book_test2.add_author('Hey')
# book_test2.remove_author('Austin Niccum')
# book_test2.add_book()

# book_test2.delete_book()
# book_test2.delete_copy_book(output_copy_num=True)

# book_test.delete_copy_book(output_copy_num=True)

# book_test2.edit({'authors': ['A0', 'A3']})
# book_test2.edit({'title': 'Intro 101'})
# book_test2.edit({'ISBN': '9999-1002-2005'})
# book_test2.edit({'page_number': 399})
# book_test2.edit({'ISBN': '119'})

# book_test2.add_book()
# print(book_test2)

# searchBook = SearchEngine(db, 'books', title = 'Introduction to PDE')
# searchBook = SearchEngine(db,'books', page_number = 899)
# searchBook = SearchEngine(db)
# searchBook.search_by_authors(["James Guan", "Austin"])
# searchBook.get_result()

# book_test1.remove_attribute(attribute="authors")
# book_test1.remove_attribute(attribute="title")
# book_test1.remove_attribute(attribute="ISBN")
# book_test1.remove_attribute(attribute="page_number")
# book_test1.add_book()
# db.books.find_many

# sortBook = SortEngine(db, 'books', attribute= 'title')
# sortBook = SortEngine(db, 'books', attribute= 'ISBN')
# sortBook = SortEngine(db, 'books', attribute= 'page_number')
# sortBook = SortEngine(db, 'books', attribute='authors')
# sortBook.get_result()


alice = Borrower(db=db, name='alice', username='aliceUser', phone=8122346408)
alice.initiate()
bob = Borrower(db=db, name='bob', username='bobUser', phone=8122346408)
bob.initiate()
# bob2 = Borrower(db=db, name='bob2', username='bobUser', phone=8122346408)
# bob3 = Borrower(db=db, name='bob3', username='bobUser', phone=8122346408)

# borrowers = [alice, bob, bob2, bob3]

# for b in borrowers:
# 	b.initiate()
# b.delete_borrower()

# alice.delete_borrower()
# user_test = Borrower(db=db, name='bob', username='bobUser', search_user= True)
# user_test.edit(name = 'James')
# user_test.edit(username = 'James')
# user_test.edit(name = 'James',username = 'JamesUser')
# user_test.edit(name = 'James',username = 'JamesUser2', phone= 123456)

# print(user_test)

# search_user = SearchEngine(db, 'borrowers', user_search=True, username='bobUser')
# search_user = SearchEngine(db, 'borrowers', user_search=True, phone=8122346408)

# search_user.get_result()

borrowEngine = BorrowingEngine(borrower=alice, book=book_test1)
borrowEngine.borrow_action()
borrowEngine.borrow_action()
borrowEngine.borrow_action(book_test2)
borrowEngine.borrow_action()
#
# book_not_exit = Book(db, ISBN = '00101')
bobBorrow = BorrowingEngine(borrower=bob, book=book_test1)
bobBorrow.borrow_action()
# bobBorrow.borrow_action(book = book_test2)
# bobBorrow.borrow_action(book = book_test2)
#
# bobBorrow.borrow_action(book = book_test1)
# bobBorrow.return_action(ISBN= '00101')
# # bobBorrow.return_action(ISBN='9999-1002-2005')
#

# print(bob.get_checked_book_num())
# print(book_test1.get_borrowers())

# borrowEngine.return_action()
# borrowEngine.return_action()
borrowEngine.return_action(ISBN='9991-1021-2002')

# print(bob.get_checked_book_num())
# print(book_test1.get_borrowers())



