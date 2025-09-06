from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q

# Importamos todos los modelos necesarios de las otras apps
from members.models import Profile, MemberType, Role, Category
from billing.models import Invoice, BillableItem, Payment

# --- Función de Verificación ---
def is_superuser(user):
    """
    Comprueba si un usuario es superusuario. Se usa para proteger las vistas.
    """
    return user.is_superuser

# --- Vistas del Dashboard ---

@user_passes_test(is_superuser)
def dashboard_home(request):
    """
    Vista principal del Panel de Administración.
    Muestra accesos directos a los módulos de gestión.
    """
    # En el futuro, aquí podrías añadir estadísticas como "pagos pendientes", etc.
    pending_payments_count = Invoice.objects.filter(status='VER').count()
    context = {
        'pending_payments_count': pending_payments_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(is_superuser)
def member_list_view(request):
    """
    Muestra una lista de todos los socios con opciones de búsqueda.
    """
    profiles = Profile.objects.select_related('user', 'member_type').all()

    # Lógica de Búsqueda
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(dni__icontains=query)
        ).distinct()

    context = {
        'profiles': profiles,
    }
    return render(request, 'dashboard/member_list.html', context)

@user_passes_test(is_superuser)
def billing_dashboard_view(request):
    """
    Dashboard de facturación con lista de socios filtrable y acciones en masa.
    """
    profiles = Profile.objects.select_related('user', 'member_type').all()
    
    # --- Lógica de Filtros (GET) ---
    selected_member_type_id = request.GET.get('member_type')
    selected_category_id = request.GET.get('category')

    if selected_member_type_id:
        profiles = profiles.filter(member_type_id=selected_member_type_id)
    if selected_category_id:
        # Filtramos perfiles que tengan un rol en la categoría seleccionada
        profiles = profiles.filter(roles__category_id=selected_category_id).distinct()

    # --- Lógica de Asignación de Facturas (POST) ---
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
                    # Lógica de bonificación
                    status = 'PEN'
                    if profile.is_exempt and item.is_bonifiable:
                        status = 'BON'
                    
                    # Se crea la factura para el socio
                    Invoice.objects.create(
                        profile=profile, item=item, amount=item.amount,
                        due_date=due_date, status=status
                    )
                    count += 1
                
                messages.success(request, f"Se asignaron {count} facturas exitosamente.")
            except (BillableItem.DoesNotExist, ValueError):
                messages.error(request, "Hubo un error con los datos. Intenta de nuevo.")
        
        return redirect('dashboard_billing')

    # --- Datos para los formularios y filtros ---
    context = {
        'profiles': profiles,
        'billable_items': BillableItem.objects.all(),
        'member_types': MemberType.objects.all(),
        'categories': Category.objects.all(),
        'selected_member_type_id': selected_member_type_id,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'dashboard/billing_dashboard.html', context)

@user_passes_test(is_superuser)
def approve_payment(request, payment_id):
    """
    Aprueba un pago, cambiando el estado de la factura a 'Pagado'.
    """
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(id=payment_id)
            invoice = payment.invoice
            invoice.status = 'PAG'
            invoice.save()
            messages.success(request, f"Pago de {invoice.profile.user.get_full_name()} aprobado.")
        except Payment.DoesNotExist:
            messages.error(request, "El pago que intentas aprobar no existe.")
    return redirect('dashboard_billing') # Redirige de vuelta a la página principal de facturación
