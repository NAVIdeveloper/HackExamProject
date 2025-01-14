from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .bot import *
import os
from .models import *
# Create your views here.
@csrf_exempt
def TelegramBot_Webhook(request,bot_token):
    if bot_token == config.BOT_TOKEN and request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse("ok")
    
    return HttpResponse('error')

@csrf_exempt
def Api_Create_Question(request):
    if request.method == 'POST':
        info = Info.objects.last()
        question = request.POST['question']
        query = Question.objects.create(
            text=question
        )
        message = bot.send_message(
            info.telegram_group,f"<b>Savol:</b>\n{question}"
        )
        query.message_id = message.message_id
        query.save()
        return HttpResponse(f'{query.id}')
    
    return HttpResponse('error')

@csrf_exempt
def Api_Get_Answer(request,query):
    filtered = Question.objects.filter(id=query)
    if filtered.exists():
        question = filtered.first()
        if question.is_answered:
            answer = question.answer
            question.delete()
            return HttpResponse(f'{answer}')
        else:
            return HttpResponse('wait')

    return HttpResponse('error')

@csrf_exempt
def DownloadFile(request):
    info = Info.objects.last()
    return FileResponse(info.program.open('rb'), as_attachment=True, filename=info.program.name)
