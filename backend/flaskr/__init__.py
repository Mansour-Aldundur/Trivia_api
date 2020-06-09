import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"*": {"origins": "*"}})


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  def paginate_questions(questions, page):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current_questions = questions[start:end]
    return current_questions

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():

    try:
      categories = Category.query.all()
      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully fetched all categories',
        'categories':[c.format() for c in categories]
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    error = None

    try:
      questions = Question.query.all()
      categories = Category.query.all()
      formatted_questions = [q.format() for q in questions]

      results = paginate_questions(formatted_questions, page)

      if len(results) == 0:
        error = 404
        abort(404)

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully fetched questions',
        'questions': results,
        'total_questions': len(formatted_questions),
        'categories': [c.format() for c in categories]
      })
    except:
      if error == 404:
        abort(404)
      else:
        abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = None
    try:
      question = Question.query.filter_by(id=question_id).one_or_none()

      if question is None:
        error = 404
        abort(404)
      else:
        question.delete()

        return jsonify({
          'success':True,
          'status':200,
          'message':'successfully deleted question'
        })
    except:
      if error == 404:
        abort(404)
      else:
        abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    fresh_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')

    if fresh_question is None  or new_answer is None \
      or new_category is None or new_difficulty is None: 
        abort(400)

    new_question = Question(
      question=fresh_question,
      answer=new_answer,
      category=new_category,
      difficulty=new_difficulty
    )

    try:
      new_question.insert()

      return jsonify({
        'success':True,
        'status':201,
        'message':'successfully created a question',
        'created_question': new_question.id
      }), 201
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm')

    try:
      found_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully found questions',
        'questions':[q.format() for q in found_questions]
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    page = request.args.get('page', 1)

    try:
      questions = Question.query.filter_by(category=category_id).all()
      formatted_questions = [q.format() for q in questions]

      results = paginate_questions(formatted_questions, page)

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully returned questions by category',
        'questions': results
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    category = body.get('quiz_category')

    try:
      questions = Question.query.filter_by(category=category['id']).all()

      formatted_questions = [q.format() for q in questions]

      available_questions = []

      for q in formatted_questions:
        
        if q['id'] not in previous_questions:
          available_questions.append(q)

      next_question = None

      if len(available_questions) > 0:
        random_index = random.randint(0, len(available_questions) - 1)
        next_question = available_questions[random_index]

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully returned questions by category',
        'question': next_question
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(e):
    return jsonify({
      'success':False,
      'status':400,
      'message':'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(e):
    return jsonify({
      'success':False,
      'status':404,
      'message':'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessible(e):
    print(e)
    return jsonify({
      'success':False,
      'status':422,
      'message':'unprocessible request'
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(e):
    return jsonify({
      'success':False,
      'status':405,
      'message':'method not allowed'
    }), 405
    
  return app

    