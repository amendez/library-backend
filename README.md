# Library API

## How to run the project for the first time
1. Clone the repository.
2. Run `docker-compose up db -d` to start an empty PostgreSQL database.
3. Run `docker-compose run web python manage.py migrate` to create the tables.
4. Run `docker-compose run web python manage.py createsuperuser` to create a super user (this is optional, but it's useful to be able to use Django Admin)
5. Run `docker-compose run web python manage.py import book_data.csv` to import the books provided in the CSV file to the DB. (also optional).
6. Run `docker-compose up` to start the django server and stay attached to container to see the logs.

## How to run the project for the second time
* Run `docker-compose up`

## How to run the tests
* Run `docker-compose run web python manage.py test`

## How to use the API
### Books
#### List all books
* Run `curl "http://localhost:8000/books/"`
#### List books searching for a word
* Run `curl "http://localhost:8000/books/?search=Great%20Alone"`
#### List books searching for an author name
* Run `curl "http://localhost:8000/books/?search=Tayari%20Jones"`
#### List books searching for an genre name
* Run `curl "http://localhost:8000/books/?search=horror"`
#### List books ordering by the ones with most reviews
* Run `curl "http://localhost:8000/books/?ordering=-review_count"`
#### Get details of a book
* Run `curl "http://localhost:8000/books/1/"`

### Customers
#### Create a customer
* Run `curl -X POST -H "Content-Type: application/json" -d '{"full_name": "Lionel Messi", "email": "leomessi@gmail.com"}' "http://localhost:8000/customers/"`
#### List all customers
* Run `curl "http://localhost:8000/customers/"`
#### Get details of a customer
* Run `curl "http://localhost:8000/customers/1/"`

### Check out / Return a book
#### Checkout a book
* Run `curl -X POST -H "Content-Type: application/json" -d '{"customer": 1}' "http://localhost:8000/books/1/checkout/"`
#### Return a book
* Run `curl -X POST -H "Content-Type: application/json" -d '{"customer": 1}' "http://localhost:8000/books/1/return/"`
#### Check user history
* Run `curl "http://localhost:8000/customers/1/history/"`

Alternatively, you can use the browsable api by accessing `http://localhost:8000/` in your browser. All the endpoints can be hit from there too.