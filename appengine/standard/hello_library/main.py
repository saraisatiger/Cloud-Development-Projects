# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import ndb
import webapp2
import json


class Book(ndb.Model):
    id = ndb.StringProperty()
    title = ndb.StringProperty(required = True)
    author = ndb.StringProperty()
    isbn = ndb.StringProperty(required = True)
    genre = ndb.StringProperty(repeated = True)
    checkedIn = ndb.BooleanProperty()
    '''
    {
        "title": "The Hitchhikers guide to the galaxy",
        "author": "Douglas Adams",
        "isbn": "0345391802" ,
        "genre": ["sci-fi", "humor"],
        "checkedIn": false
    }
    {
        "title": "The Name of the Rose",
        "author": "Umberto Eco",
        "isbn": "0343215043",
        "genre": ["mistery"],
        "checkedIn": true
    }
    '''

class Customer(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required = True)
    balance = ndb.FloatProperty()
    checked_out = ndb.StringProperty(repeated = True)
    '''
    {
        "id": 100,
         "name": "Arthur Dent",
         "balance": 0.50,
         "checked_out": ["/book/5", "/book/10"]
    }
    {
        "name": "John Smith",
        "balance": 0.0,
        "checked_out": []
    }
    {
        "name": "Gogi Pie",
        "balance": 2.75,
        "checked_out": []
    }
    '''


class AllBooksHandler(webapp2.RequestHandler):
    # Create a new Book
    # POST /books
    def post(self):
        book_data = json.loads(self.request.body)

        new_book = Book(
            title = book_data['title'],
            author = book_data['author'],
            isbn = book_data['isbn'],
            genre = book_data['genre'],
            checkedIn = book_data['checkedIn']
        )
        new_book.put()
        new_book.id = new_book.key.urlsafe()

        book_dict = new_book.to_dict()
        book_dict['self'] = '/books/' + new_book.id

        self.response.write(json.dumps(book_dict))

    # Get all Books
    # GET /books
    def get(self):
        books = []

        if self.request.query_string:
            query = []
            bool = self.request.GET['checkedIn']
            book_query = Book.query()
            all_books = book_query.fetch()

            for book in all_books:
                book.id = book.key.urlsafe()
                book_dict = book.to_dict()
                book_dict['self'] = '/books/' + book.id
                books.append(book_dict)

            for book_obj in books:
                if bool == 'True' or bool == 'true':
                    if book_obj['checkedIn']:
                        query.append(book_obj)

                elif bool == 'False' or bool == 'false':
                    if not book_obj['checkedIn']:
                        query.append(book_obj)

            self.response.write(query)


        else:
            book_query = Book.query()
            all_books = book_query.fetch()

            for book in all_books:
                book.id = book.key.urlsafe()
                book_dict = book.to_dict()
                book_dict['self'] = '/books/' + book.id
                books.append(book_dict)

            self.response.write(books)

    # Delete all Books
    # DELETE /books
    def delete(self):
        book_query = Book.query()
        all_books = book_query.fetch()
        for book in all_books:
            book.key.delete()


class BookHandler(webapp2.RequestHandler):
    # Get Book by id
    # GET /books/:book_id
    def get(self, id = None):
        if id:
            book = ndb.Key(urlsafe = id).get()
            book.id = id
            book.put()

            book_dict = book.to_dict()
            book_dict['self'] = '/books/' + id
            self.response.write(json.dumps(book_dict))

    # Delete Book by id
    # DELETE /books/:book_id
    def delete(self, id = None):
        if id:
            book = ndb.Key(urlsafe = id).get()
            book.key.delete()

    # Update Book by id
    # PATCH /books/:book_id
    # ===TODO
    def patch(self, id = None):
        book_data = json.loads(self.request.body)

        # if id:
        #     book = ndb.Key(urlsafe = id).get()
        #     book.id = id

        self.response.write(book_data)


class AllCustomersHandler(webapp2.RequestHandler):
    # Create new Customer
    # POST /customers
    def post(self):
        customer_data = json.loads(self.request.body)

        new_customer = Customer(
            name = customer_data['name'],
            balance = customer_data['balance'],
            checked_out = customer_data['checked_out']
        )
        new_customer.put()
        new_customer.id = new_customer.key.urlsafe()

        customer_dict = new_customer.to_dict()
        customer_dict['self'] = '/customers/' + new_customer.id

        self.response.write(json.dumps(customer_dict))

    # Get all Customers
    # GET /customers
    def get(self):
        customers = []
        customer_query = Customer.query()
        all_customers = customer_query.fetch()

        for customer in all_customers:
            customer.id = customer.key.urlsafe()
            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + customer.id
            customers.append(customer_dict)

        self.response.write(customers)

    # Delete all Customers
    # DELETE /customers
    def delete(self):
        customer_query = Customer.query()
        all_customers = customer_query.fetch()
        for customer in all_customers:
            customer.key.delete()


class CustomerHandler(webapp2.RequestHandler):
    # Get Customer by id
    # GET /customers/:customer_id
    def get(self, id = None):
        if id:
            customer = ndb.Key(urlsafe = id).get()
            customer.id = id
            customer.put()

            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + id
            self.response.write(json.dumps(customer_dict))

    # Delete Customer by id
    # DELETE /customers/:customer_id
    def delete(self, id = None):
        if id:
            customer = ndb.Key(urlsafe = id).get()
            customer.key.delete()

    # Replace Customer
    # PUT /customers/:customer_id
    # ===TODO Not updating!
    def put(self, id = None):
        if id:
            customer = ndb.Key(urlsafe = id).get()
            customer.id = id
            customer.put()

            customer_data = json.loads(self.request.body)

            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + customer.id

            customer_dict['name'] = customer_data['name']
            customer_dict['balance'] = customer_data['balance']
            customer_dict['checked_out'] = customer_data['checked_out']

            self.response.write(json.dumps(customer_dict))

    # Check out a Book to a Customer
    # PUT /customers/:customer_id/books/:book_id
    def put(self, customer_id = None, book_id = None):
        if customer_id and book_id:
            customer = ndb.Key(urlsafe = customer_id).get()
            book = ndb.Key(urlsafe = book_id).get()

            # Update Book's checked in status
            book.checkedIn = False
            book.put()
            book_dict = book.to_dict()
            book_dict['self'] = '/books/' + book_id

            # Update Customer's checked out list
            customer.checked_out.append(book_dict['self'])
            customer.id = customer_id
            customer.put()

            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + customer_id
            self.response.write(json.dumps(customer_dict))

    # Check in a Book from a Customer
    # DELETE /customers/:customer_id/books/:book_id
    def delete(self, customer_id = None, book_id = None):
        if customer_id and book_id:
            customer = ndb.Key(urlsafe = customer_id).get()
            book = ndb.Key(urlsafe = book_id).get()

            # Update Book's checked in status
            book.checkedIn = True
            book.put()
            book_dict = book.to_dict()
            book_dict['self'] = '/books/' + book_id

            # Update Customer's checked out list
            customer.checked_out.remove(book_dict['self'])
            customer.id = customer_id
            customer.put()

            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + customer_id
            self.response.write(json.dumps(customer_dict))

    # Get Customer's checked out Books
    # GET /customers/:customer_id/books
    def get(self, id = None):
        if id:
            customer = ndb.Key(urlsafe = id).get()
            customer.id = id
            customer.put()

            customer_dict = customer.to_dict()
            customer_dict['self'] = '/customers/' + id
            self.response.write(json.dumps(customer_dict['checked_out']))


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, Library! It\'s me, REST Implementation!')

    def delete(self):
        book_query = Book.query()
        all_books = book_query.fetch()
        for book in all_books:
            book.key.delete()

        customer_query = Customer.query()
        all_customers = customer_query.fetch()
        for customer in all_customers:
            customer.key.delete()


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/books', AllBooksHandler),
    ('/books/([a-zA-Z0-9\_\-]+)', BookHandler),
    ('/books?checkedIn=(.*)', BookHandler),
    ('/customers', AllCustomersHandler),
    ('/customers/([a-zA-Z0-9\_\-]+)', CustomerHandler),
    ('/customers/([a-zA-Z0-9\_\-]+)/books', CustomerHandler),
    ('/customers/([a-zA-Z0-9\_\-]+)/books/([a-zA-Z0-9\_\-]+)', CustomerHandler)
], debug=True)
