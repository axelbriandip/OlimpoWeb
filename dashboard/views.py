from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from news.models import Article
from news.forms import ArticleForm
# Importamos los modelos y formularios de las otras apps
from members.models import Profile, MemberType, Role, Category
from billing.models import Invoice, BillableItem, Payment
from members.forms import UserUpdateForm, ProfileAdminUpdateForm, RoleForm, MemberCreationForm
from billing.forms import BillableItemForm
from gallery.models import Album, Photo
from gallery.forms import AlbumForm
from core.models import TimelineEvent
from core.forms import TimelineEventForm

# --- Función de Verificación ---
def is_superuser(user):
    return user.is_superuser

# --- Vistas del Dashboard ---

@user_passes_test(is_superuser)
def dashboard_home(request):
    """
    Vista principal del Panel de Administración.
    """
    pending_payments_count = Invoice.objects.filter(status='VER').count()
    context = {
        'pending_payments_count': pending_payments_count
    }
    return render(request, 'dashboard/dashboard.html', context)

# --- Vistas para la Gestión de Socios (CRUD) ---

@user_passes_test(is_superuser)
def member_create_view(request):
    """
    Vista para Crear un nuevo socio (User + Profile + Roles).
    """
    RoleFormSet = inlineformset_factory(Profile, Role, form=RoleForm, extra=1, can_delete=False)

    if request.method == 'POST':
        user_form = MemberCreationForm(request.POST)
        profile_form = ProfileAdminUpdateForm(request.POST, request.FILES)
        
        # Primero, validamos los dos formularios principales
        if user_form.is_valid() and profile_form.is_valid():
            # 1. Creamos el User y hasheamos la contraseña
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save() # Al guardar, la señal (si está activa) se dispara y crea el Profile vacío.

            # 2. Re-vinculamos el profile_form a la instancia recién creada y guardamos los datos del perfil
            profile_form_instance = ProfileAdminUpdateForm(request.POST, request.FILES, instance=user.profile)
            if profile_form_instance.is_valid():
                profile_form_instance.save()

                # 3. Vinculamos y guardamos los roles asociados al perfil
                role_formset = RoleFormSet(request.POST, instance=user.profile)
                if role_formset.is_valid():
                    role_formset.save()
                
                messages.success(request, f"Socio {user.get_full_name()} creado con éxito.")
                return redirect('dashboard_member_list')
        
        # Si los formularios principales no son válidos, preparamos un formset vacío para mostrar la página de nuevo con los errores
        role_formset = RoleFormSet()
            
    else: # Si es un GET request
        user_form = MemberCreationForm()
        profile_form = ProfileAdminUpdateForm()
        role_formset = RoleFormSet()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'role_formset': role_formset,
        'title': 'Añadir Nuevo Socio'
    }
    return render(request, 'dashboard/member_form.html', context)


@user_passes_test(is_superuser)
def member_list_view(request):
    """
    Muestra una lista de todos los socios con opciones de búsqueda.
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
def member_update_view(request, pk):
    """
    Vista para ver (Leer) y editar (Actualizar) un socio y sus roles.
    """
    profile = get_object_or_404(Profile, pk=pk)
    user = profile.user
    
    RoleFormSet = inlineformset_factory(Profile, Role, form=RoleForm, extra=1, can_delete=True)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileAdminUpdateForm(request.POST, request.FILES, instance=profile)
        role_formset = RoleFormSet(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid() and role_formset.is_valid():
            user_form.save()
            profile_form.save()
            role_formset.save()
            messages.success(request, f"Perfil de {user.get_full_name()} actualizado con éxito.")
            return redirect('dashboard_member_list')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileAdminUpdateForm(instance=profile)
        role_formset = RoleFormSet(instance=profile)

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'role_formset': role_formset,
        'title': 'Editar Socio'
    }
    return render(request, 'dashboard/member_form.html', context)

@user_passes_test(is_superuser)
def member_delete_view(request, pk):
    """
    Vista para eliminar un socio (su Usuario y Perfil).
    """
    profile = get_object_or_404(Profile, pk=pk)
    user_to_delete = profile.user
    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, f"El socio {user_to_delete.get_full_name()} ha sido eliminado.")
        return redirect('dashboard_member_list')
    
    context = {'profile': profile}
    return render(request, 'dashboard/member_confirm_delete.html', context)


# --- Vistas para la Gestión de Facturación ---
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
    
    # Pestaña "Asignar Cobros" (con sus filtros)
    profiles = Profile.objects.select_related('user', 'member_type').all().order_by('member_id')
    selected_member_type_id = request.GET.get('member_type')
    selected_category_id = request.GET.get('category')
    if selected_member_type_id:
        profiles = profiles.filter(member_type_id=selected_member_type_id)
    if selected_category_id:
        profiles = profiles.filter(roles__category_id=selected_category_id).distinct()

    # Pestaña "Registro de Facturas" (con sus filtros)
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

@user_passes_test(is_superuser)
def news_list_view(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'dashboard/news_list.html', context)

@user_passes_test(is_superuser)
def news_create_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Noticia creada con éxito.")
            return redirect('dashboard_news_list')
    else:
        form = ArticleForm()
    context = {'form': form, 'title': 'Crear Nueva Noticia'}
    return render(request, 'dashboard/news_form.html', context)

@user_passes_test(is_superuser)
def news_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Noticia actualizada con éxito.")
            return redirect('dashboard_news_list')
    else:
        form = ArticleForm(instance=article)
    context = {'form': form, 'title': 'Editar Noticia'}
    return render(request, 'dashboard/news_form.html', context)

@user_passes_test(is_superuser)
def news_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Noticia eliminada con éxito.")
        return redirect('dashboard_news_list')
    context = {'article': article}
    return render(request, 'dashboard/news_confirm_delete.html', context)

@user_passes_test(is_superuser)
def gallery_list_view(request):
    """Muestra una lista de todos los álbumes."""
    albums = Album.objects.all()
    context = {'albums': albums}
    return render(request, 'dashboard/gallery_list.html', context)

@user_passes_test(is_superuser)
def gallery_update_view(request, pk=None):
    """
    Crea un nuevo álbum (si pk es None) o edita uno existente.
    """
    # Definimos el formset para manejar las fotos del álbum
    PhotoFormSet = inlineformset_factory(Album, Photo, fields=('image', 'title'), extra=1, can_delete=True)

    if pk: # Si es para editar, buscamos el álbum
        album = get_object_or_404(Album, pk=pk)
        title = "Editar Álbum"
    else: # Si es para crear, creamos una instancia vacía
        album = Album()
        title = "Crear Nuevo Álbum"

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        formset = PhotoFormSet(request.POST, request.FILES, instance=album)
        
        if form.is_valid() and formset.is_valid():
            album = form.save()
            formset.instance = album
            formset.save()
            messages.success(request, f"Álbum guardado con éxito.")
            return redirect('dashboard_gallery_list')
    else:
        form = AlbumForm(instance=album)
        formset = PhotoFormSet(instance=album)

    context = {'form': form, 'formset': formset, 'title': title, 'album': album}
    return render(request, 'dashboard/gallery_form.html', context)

@user_passes_test(is_superuser)
def gallery_delete_view(request, pk):
    """Elimina un álbum y todas sus fotos."""
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, "Álbum eliminado con éxito.")
        return redirect('dashboard_gallery_list')
    context = {'album': album}
    return render(request, 'dashboard/gallery_confirm_delete.html', context)

# --- VISTAS CRUD PARA GESTIONAR HISTORIA ---

@user_passes_test(is_superuser)
def history_list_view(request):
    """
    Muestra una lista de todos los hitos principales y sus sub-hitos.
    """
    # Usamos prefetch_related para cargar los sub-hitos de forma eficiente
    main_events = TimelineEvent.objects.filter(parent__isnull=True).prefetch_related('sub_events')
    context = {'main_events': main_events}
    return render(request, 'dashboard/history_list.html', context)

@user_passes_test(is_superuser)
def history_update_view(request, pk=None):
    """
    Crea un nuevo Hito/Sub-Hito o edita uno existente.
    """
    if pk:
        instance = get_object_or_404(TimelineEvent, pk=pk)
        title = "Editar Hito"
    else:
        instance = None
        title = "Crear Nuevo Hito / Sub-Hito"

    if request.method == 'POST':
        form = TimelineEventForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Hito guardado con éxito.")
            return redirect('dashboard_history_list')
    else:
        form = TimelineEventForm(instance=instance)

    context = {'form': form, 'title': title}
    return render(request, 'dashboard/history_form.html', context)

@user_passes_test(is_superuser)
def history_delete_view(request, pk):
    """
    Elimina un Hito y todos sus sub-hitos asociados.
    """
    event = get_object_or_404(TimelineEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Hito eliminado con éxito.")
        return redirect('dashboard_history_list')
    context = {'event': event}
    return render(request, 'dashboard/history_confirm_delete.html', context)