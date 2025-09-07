from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

# Importamos todos los modelos y formularios necesarios
from members.models import Profile, MemberType, Role, Category
from billing.models import Invoice, BillableItem, Payment
from billing.forms import BillableItemForm

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def dashboard_home(request):
    """
    Vista principal del Panel de Administración.
    """
    pending_payments_count = Invoice.objects.filter(status='VER').count()
    context = {'pending_payments_count': pending_payments_count}
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(is_superuser)
def member_list_view(request):
    """
    Muestra una lista de todos los socios con opciones de búsqueda y filtro.
    """
    profiles = Profile.objects.select_related('user', 'member_type').all().order_by('member_id')
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(dni__icontains=query)
        ).distinct()
    context = {'profiles': profiles}
    return render(request, 'dashboard/member_list.html', context)

@user_passes_test(is_superuser)
def billing_dashboard_view(request):
    """
    Dashboard de facturación unificado con todas las herramientas de gestión.
    """
    # --- Lógica de Asignación de Facturas (cuando se envía el formulario) ---
    if request.method == 'POST':
        profile_ids = request.POST.getlist('profile_ids')
        item_id = request.POST.get('billable_item')
        due_date = request.POST.get('due_date')

        if not profile_ids:
            messages.warning(request, "Error: No seleccionaste ningún socio.")
        elif not item_id or not due_date:
            messages.warning(request, "Error: Debes seleccionar un ítem a cobrar y una fecha de vencimiento.")
        else:
            try:
                item = BillableItem.objects.get(id=item_id)
                selected_profiles = Profile.objects.filter(id__in=profile_ids)
                count = 0
                for profile in selected_profiles:
                    status = 'PEN'
                    if profile.is_exempt and item.is_bonifiable:
                        status = 'BON'
                    Invoice.objects.create(
                        profile=profile, item=item, amount=item.amount,
                        due_date=due_date, status=status
                    )
                    count += 1
                messages.success(request, f"Se asignaron {count} facturas exitosamente.")
            except (BillableItem.DoesNotExist, ValueError):
                messages.error(request, "Hubo un error con los datos.")
        
        return redirect('dashboard_billing')

    # --- Datos para las Plantillas (cuando se carga la página) ---
    
    # Pestaña "Verificar Pagos"
    pending_payments = Invoice.objects.filter(status='VER').select_related('profile__user', 'item', 'payment')
    
    # Pestaña "Asignar Cobros"
    profiles = Profile.objects.select_related('user', 'member_type').all().order_by('member_id')
    selected_member_type_id = request.GET.get('member_type')
    selected_category_id = request.GET.get('category')
    if selected_member_type_id:
        profiles = profiles.filter(member_type_id=selected_member_type_id)
    if selected_category_id:
        profiles = profiles.filter(roles__category_id=selected_category_id).distinct()

    # Pestaña "Registro de Facturas"
    invoices = Invoice.objects.select_related('profile__user', 'item').prefetch_related('payment').all()
    search_query = request.GET.get('q_invoice')
    status_query = request.GET.get('status_invoice')
    if search_query:
        invoices = invoices.filter(Q(profile__user__first_name__icontains=search_query) | Q(profile__user__last_name__icontains=search_query))
    if status_query:
        invoices = invoices.filter(status=status_query)
    
    context = {
        'pending_payments': pending_payments,
        'profiles': profiles,
        'invoices': invoices,
        'billable_items': BillableItem.objects.all(),
        'member_types': MemberType.objects.all(),
        'categories': Category.objects.all(),
        'all_statuses': Invoice.Status.choices,
        'selected_member_type_id': selected_member_type_id,
        'selected_category_id': selected_category_id,
        'search_query': search_query,
        'status_query': status_query,
    }
    return render(request, 'dashboard/billing_dashboard.html', context)

@user_passes_test(is_superuser)
def approve_payment(request, invoice_id):
    if request.method == 'POST':
        try:
            invoice = Invoice.objects.get(id=invoice_id, status='VER')
            invoice.status = 'PAG'
            invoice.save()
            messages.success(request, f"Pago de {invoice.profile.user.get_full_name()} aprobado.")
        except Invoice.DoesNotExist:
            messages.error(request, "La factura no existe o ya no está en verificación.")
    return redirect(f"{reverse('dashboard_billing')}?tab=verify")

@user_passes_test(is_superuser)
def reject_payment(request, invoice_id):
    if request.method == 'POST':
        try:
            invoice = Invoice.objects.get(id=invoice_id, status='VER')
            invoice.status = 'PEN'
            if hasattr(invoice, 'payment'):
                invoice.payment.delete()
            invoice.save()
            messages.warning(request, f"Pago de {invoice.profile.user.get_full_name()} rechazado.")
        except Invoice.DoesNotExist:
            messages.error(request, "La factura no existe o ya no está en verificación.")
    return redirect(f"{reverse('dashboard_billing')}?tab=verify")

# --- Vistas CRUD para Ítems Facturables ---
@user_passes_test(is_superuser)
def billable_item_create(request):
    if request.method == 'POST':
        form = BillableItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem facturable creado con éxito.")
            return redirect(f"{reverse('dashboard_billing')}?tab=items")
    else:
        form = BillableItemForm()
    context = {'form': form, 'title': 'Crear Nuevo Ítem Facturable'}
    return render(request, 'dashboard/billable_item_form.html', context)

@user_passes_test(is_superuser)
def billable_item_update(request, pk):
    item = get_object_or_404(BillableItem, pk=pk)
    if request.method == 'POST':
        form = BillableItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem facturable actualizado con éxito.")
            return redirect(f"{reverse('dashboard_billing')}?tab=items")
    else:
        form = BillableItemForm(instance=item)
    context = {'form': form, 'title': 'Editar Ítem Facturable'}
    return render(request, 'dashboard/billable_item_form.html', context)

@user_passes_test(is_superuser)
def billable_item_delete(request, pk):
    item = get_object_or_404(BillableItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Ítem facturable eliminado con éxito.")
        return redirect(f"{reverse('dashboard_billing')}?tab=items")
    context = {'item': item}
    return render(request, 'dashboard/billable_item_confirm_delete.html', context)

