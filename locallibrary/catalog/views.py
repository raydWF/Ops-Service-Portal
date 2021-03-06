from django.shortcuts import render, redirect
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from .forms import *
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory



# Create your views here.

def index(request):
	"""
	View function for home page of site.
	"""
	
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
	)
def construction(request):
 
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'under_construction.html',
    )


def KeyAgreement(request):

    return render(
        request,
        'catalog/roomkey_agreement.html',
    )
# ===================================== KEYS ====================================================

class KeyListView(generic.ListView):
    model = RoomKey
    fields = '__all__'
    template_name = 'catalog/roomkey_list.html'

    
class KeyDetailView(generic.DetailView):
    model = RoomKey

# view for making a key request
class KeyRequestCreate(CreateView):
    model = KeyRequest
    fields = ['roomkey', 'requester', 'borrower', 'request_comments']
    template_name = 'catalog/roomkey_request_form.html'

class KeyAgreement111(CreateView):
    model = KeyRequest
    fields = ['roomkey', 'requester', 'borrower', 'request_comments']
    template_name = 'catalog/roomkey_agreement.html'

class LoanedKeysByUserListView(LoginRequiredMixin,generic.ListView):
    model = KeyInstance
    template_name = 'catalog/roomkey_list_borrowed_user.html'

    def get_queryset(self):
        return KeyInstance.objects.filter(requester=self.request.user).filter(status__exact='o').order_by('date_out')

class LoanedKeysAllListView(PermissionRequiredMixin,generic.ListView):
    
    model = KeyInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/roomkey-all-borrowed.html'
        
    def get_queryset(self):
        return KeyInstance.objects.filter(status__exact='o').order_by('date_in')  

class KeyRequestListView(PermissionRequiredMixin, generic.ListView):
    model = KeyRequest
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/roomkey_requests_all.html'

class KeyRequestUpdate(UpdateView):
    model = KeyRequest
    inline_model = KeyInstance
    fields = ['request_status', 'request_comments', ]
    # initial = {'date_in': datetime.date.today()}
    template_name = 'catalog/roomkey_request_form.html'

class KeyRequestDetailView(generic.DetailView):
    model = KeyRequest
    template_name = "catalog/roomkey_request_detail.html"

    def RequestDetail(request):
        num_keyinstances_available = KeyInstance.objects.filter(status__exact='a').count()

        return render(
            request,
            'key-request-detail',
            context = {'num_key_available':num_keyinstances_available},
        )
        
@permission_required('catalog.can_mark_returned')
def renew_key_user(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    key_inst=get_object_or_404(KeyInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewKeyForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            key_inst.date_in = form.cleaned_data['renewal_date']
            key_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed-keys') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewKeyForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/roomkey_renew_user.html', {'form': form, 'keyinst':key_inst})

def add_poll(request):
    if request.POST():
        keyinst_valid = KeyInstanceForm.is_valid()
        keyreq_valid = KeyRequestForm.is_valid()

        # we do this since 'and' short circuits and we want to check to whole page for form errors
        if keyinst_valid and keyreq_valid:
            KeyInstance = KeyInstanceForm.save()
            KeyRequest = KeyRequestForm.save(commit=False)  
       
            return HttpResponseRedirect('all-requested-keys')


# =================================== MAINTENANCE REQUESTS=============================================================
# view for maintenance home page
class MaintenanceListView(generic.ListView):
    model = MaintenanceRequest
    template_name = 'catalog/maintenance-home.html'

# view for pending maintenance requests
class MaintenanceRequestListView(LoginRequiredMixin,generic.ListView):
    model = MaintenanceRequest
    template_name = 'catalog/maintenancerequest_list.html'

    def get_queryset(self):
        return MaintenanceRequest.objects.order_by('urgency', 'status')

# view for completed maintenance requests
class CompletedMaintenanceListView(LoginRequiredMixin,generic.ListView):
    model = MaintenanceRequest
    template_name = 'catalog/maintenance_list_completed.html'

    def get_queryset(self):
        return MaintenanceRequest.objects.filter(status__exact='c').order_by('-date_completed')

# view for individual maintenance request details
class MaintenanceRequestDetailView(generic.DetailView):
    model = MaintenanceRequest

# view for creating maintenacne request
class MaintenanceRequestCreate(CreateView):
    model = MaintenanceRequest
    fields = ['requester', 'office', 'urgency', 'status', 'request_comments']

class MaintenanceRequestUpdate(UpdateView):
    model = MaintenanceRequest
    fields = ['status', 'date_completed', 'request_comments']
    initial = {'date_completed': datetime.date.today()}




# =========================================MOVE REQUESTS=========================================================
class MoveRequestListView(generic.ListView):
    model = MoveRequest
    template_name = 'catalog/move-home.html'


def move_request(request):

    MoveFormSet = formset_factory(MoveForm, formset=BaseMoveFormSet)

    if request.method == 'POST':
        move_formset = BaseMoveFormSet(request.POST)

