from django.db import models

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Qustion {question_id}',
        'text': f'Text voprosa nomer {question_id}',
        'answers': question_id % 2,
        'likes': question_id % 5,
        'tags': ['tag' for i in range(question_id % 3)],
        'img': f'img/avatar-{(question_id % 3) + 1}.jpg'
    } for question_id in range(10)
]


ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text otveta nomer {answer_id}',
        'likes': answer_id % 5,
        'img': f'img/avatar-{(answer_id % 3) + 1}.jpg'
    } for answer_id in range(5)
]
