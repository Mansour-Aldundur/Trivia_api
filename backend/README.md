# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Endpoints
```
GET '/categories'
GET '/questions'
DELETE '/questions/<question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<category_id>/questions'
POST '/quizzes'
```

GET '/categories'
- Fetches all question categories
- Request Arguments: None
- Response:
```
{
  "success": true,
  "status": 200,
  "message": successfully fetched all categories
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ]
}
```
GET '/questions'
- Fetches all questions and categories
- Request Arguments: None
- Response: 
```
{
  "success": true,
  "status': 200,
  "message": "successfully fetched questions",
  "questions": [
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
  ],
  "total_questions": 2,
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
  ]
}
```

DELETE '/questions/<question_id>'
- Deletes the question with the specified id
- Request Arguments: question_id
- Response:
```
{
  "success": true,
  "status": 200,
  "message": "successfully deleted question"
}
```

POST '/questions'
- Creates a new question based on the request body
- Request Body:
```
 {
    "question": "Name an antiviral medicine used for a clinical trial by Gilead Sciences for COVID-19 treatment?",
    "answer": "Remdesivir",
    "difficulty": 5,
    "category": 1
  }
```
- Response:
```
{
  "success": true,
  "status": 201,
  "message": "successfully created a question",
  "created_question": 28 #new question id
}
```
POST '/questions/search'
- Fetches all questions that contain the search term
- Request Body: 
```
{
    'searchTerm': 'Clay'
}
```
- Response: 
```
{
  "success": true,
  "status": 200,
  "message": "successfully found questions",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ]
}
```
GET '/categories/<category_id>/questions'
- Fetches all questions for the specified category
- Request Arguments: category_id
- Response:
```
{
  "success": true,
  "status": 200,
  "message": "successfully returned questions by category",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ]
}
```

POST '/quizzes'
- Fetches a random question when playing the trivia
- Request Body:
```
 {
	"previous_questions": [],
	"quiz_category": {
		"type": "History",
		"id": 4
	}
} 
```
- Response:
```
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  }
}
```

The server returns these types of errors
```
400 - Bad Request
  {
    "success": false, 
    "error": 400,
    "message": "bad request"
  }

404 - Resource Not Found
  {
    "success": false, 
    "error": 404,
    "message": "resource not found"
  }

422 - Unprocessable entity
  {
    "success": false, 
    "error": 422,
    "message": "unprocessable
  }

405 - Method not allowed
  {
    "success": false, 
    "error": 405,
    "message": "Method not allowed"
  }
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```