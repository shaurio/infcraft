import json
from asyncio import FIRST_EXCEPTION

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from icapp.models import Btn
from openai import OpenAI

secret = 'replace with your chatgpt secret'


@csrf_exempt
def call_chatgpt(message):

    client = OpenAI(api_key=secret)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message,
        max_tokens=150,
        temperature=0.7,
    )

    return response.choices[0].message.content

@csrf_exempt
def pat_ppt(item1, item2):

    prompt = [{
        "role": "system",
        "content": "Realistically, in exactly one word what is the combination of:" + item1 + "+" + item2 + "." + "Then add ONE emoji that best matches that word.",
    }]

    chat_response = call_chatgpt(prompt)
    print(chat_response)
    return chat_response

# Create your views here.
@csrf_exempt
def home(request):
    data = dict()

    if request.method == 'POST':
        data = json.loads(request.body)
        item1 = data['item1']
        item2 = data['item2']
        # response = pat_ppt(question)
        response = pat_ppt(item1, item2)
        show_toast = True
        return JsonResponse({'response': response, 'data': data})

    else:
        response = "Ask away!"



    btns = Btn.objects.all() # list of object buttons

    print(btns)

    context = {
        "btns": btns,
        "response": response,
    }
    return render(request, 'home.html', context=context)



@csrf_exempt
def refreshBtnItems(request):

    data = dict()
    if request.method == 'POST':
        btns = Btn.objects.all()
        context = {
            "btns": btns,
        }
        data['btns_html'] = render_to_string(
            template_name='includes/btnItems.html',
            context=context,
        )
    else:
        data = {"status": "its working!"}

    return JsonResponse(data)


