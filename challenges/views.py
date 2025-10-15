from django.shortcuts import render

def challenge_list(request):
    return render(request, 'challenges/challenge_list.html')
