from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {"contacts": contacts}
    return render(request, "contact.html", context)

@login_required
def search_contacts(request):

    query = request.GET.get("search", "")

    # use query to filter user by email or name
    contacts = request.user.contacts.filter(
        Q(email__icontains=query) | Q(name__icontains=query)
    )
    context = {"contacts": contacts}
    return render(request, "partials/contact-list.html", {
        "contacts": contacts
    })