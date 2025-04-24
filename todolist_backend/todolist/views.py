from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .models import Todo

@csrf_exempt
def todo_list_create(request):
    if request.method == 'GET':
        todos = Todo.objects.all().order_by('-created_at')
        todos_list = [model_to_dict(todo) for todo in todos]
        return JsonResponse(todos_list, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            todo = Todo.objects.create(text=text)
            return JsonResponse(model_to_dict(todo), status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required field: text'}, status=400)

@csrf_exempt
def todo_detail_update_delete(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(model_to_dict(todo))
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            todo.text = data.get('text', todo.text)
            todo.completed = data.get('completed', todo.completed)
            todo.save()
            return JsonResponse(model_to_dict(todo))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'DELETE':
        todo.delete()
        return JsonResponse({}, status=204)