from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from django.db.models import Q
import time
from .forms import ContactForm
from .models import Contact

# Create your views here.

@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        "contacts": contacts,
        "form": ContactForm()
        }
    return render(request, "contact.html", context)

@login_required
def search_contacts(request):

    time.sleep(2)
    query = request.GET.get("search", "")

    # use query to filter user by email or name
    contacts = request.user.contacts.filter(
        Q(email__icontains=query) | Q(name__icontains=query)
    )
    context = {
        "contacts": contacts
        }
    return render(request, "partials/contact-list.html", {
        "contacts": contacts
    })
    
    
@login_required
@require_http_methods(["POST"])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES, initial={"user": request.user})
    
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()

        # return partial containing new row we can add to the table
        context = {"contact": contact}
        response = render(request, "partials/contact-row.html", context)
        response['HX-Trigger'] = 'success'
        return response
    
    else:
        response = render(request, "partials/add-contact-modal.html", {"form": form})
        response["HX-Retarget"] = '#contact_modal'
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger-After-Settle"] = "fail"

        return response

@login_required
@require_http_methods(['DELETE'])
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'contact-deleted'
    return response