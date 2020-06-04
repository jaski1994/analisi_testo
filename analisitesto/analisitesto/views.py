from django.shortcuts import render, redirect


# Create your views here.

def homepage(request):
    """
        homepage Main
    """

    logged_user_username = request.user.username
    context = {'logged_user_username': logged_user_username}

    #return render(request, 'login.html', context)
    return redirect('testo:login')
