from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
import random
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.


def homePage(request):
    return render(request, 'base/home.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
 
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'base/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    images = product.images.all().order_by('order')  # obtenemos las 3 imágenes ordenadas
    return render(request, 'base/detail.html', {'product': product, 'images': images})

def about(request):
    return render(request, 'base/about.html')

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        reason = request.POST.get("reason")
        description = request.POST.get("description")

        # ========== 1) MAIL QUE RECIBÍS VOS ==========
        subject_admin = f"Consulta desde la Web - {reason}"
        message_admin = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Motivo: {reason}\n\n"
            f"Descripción:\n{description}"
        )

        try:
            # Enviar correo a tu casilla
            send_mail(
                subject=subject_admin,
                message=message_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # ========== 2) MAIL AUTOMÁTICO EN HTML PARA EL CLIENTE ==========
            html_content = render_to_string("emails/auto_reply.html", {
                "name": name,
                "reason": reason,
                "description": description,
            })

            msg = EmailMultiAlternatives(
                subject="Hemos recibido tu consulta",
                body="Tu cliente de correo no soporta HTML.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # ========== MENSAJE ÉXITO ==========
            messages.success(request, "Tu consulta fue enviada correctamente.")
            return redirect("contact")  

        except Exception as e:
            print("ERROR EN EL ENVÍO:", e)
            messages.error(request, "Ocurrió un error al enviar el correo. Intente nuevamente.")

    # Render del formulario
    return render(request, "base/contact.html")

def all_products_random(request):
    products = list(Product.objects.all())
    random.shuffle(products)
    return render(request, 'base/all_products.html', {'products': products})


