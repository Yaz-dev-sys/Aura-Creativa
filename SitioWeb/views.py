from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from .models import info

def hello(request):
    """Vista para mostrar la página principal"""
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["POST"])
def guardar_contacto(request):
    """Vista para procesar el formulario de contacto vía AJAX"""
    try:
        # Obtener los datos del POST
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        empresa_proyecto = request.POST.get('empresa_proyecto', '').strip()
        servicio = request.POST.get('servicio', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        # Validar que todos los campos requeridos estén presentes
        if not all([nombre, email, empresa_proyecto, servicio, descripcion]):
            return JsonResponse({
                'success': False, 
                'message': 'Todos los campos son obligatorios'
            }, status=400)
        
        # Validar que el servicio sea una opción válida
        servicios_validos = [choice[0] for choice in info.SERVICIOS_CHOICES]
        if servicio not in servicios_validos:
            return JsonResponse({
                'success': False, 
                'message': 'Servicio no válido'
            }, status=400)
        
        # Crear y guardar el registro
        nuevo_contacto = info(
            nombre=nombre,
            email=email,
            empresa_proyecto=empresa_proyecto,
            servicio=servicio,
            descripcion=descripcion
        )
        nuevo_contacto.save()
        
        # 🚀 ENVIAR NOTIFICACIÓN POR EMAIL
        try:
            # Obtener el nombre del servicio completo
            servicio_nombre = dict(info.SERVICIOS_CHOICES).get(servicio, servicio)
            
            # Asunto del email
            asunto = f"🚀 Nuevo contacto desde AURA Creativa - {nombre}"
            
            # Mensaje del email
            mensaje = f"""
¡Hola! 👋

Has recibido un nuevo contacto desde tu sitio web de AURA Creativa:

📋 INFORMACIÓN DEL CONTACTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Nombre: {nombre}
📧 Email: {email}
🏢 Empresa/Proyecto: {empresa_proyecto}
🎯 Servicio de interés: {servicio_nombre}

💬 DESCRIPCIÓN DEL PROYECTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{descripcion}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¡Es hora de crear algo increíble! ✨

Saludos,
Sistema de notificaciones AURA Creativa
            """
            
            # Enviar email
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            print(f"✅ Email enviado correctamente a {settings.ADMIN_EMAIL}")
            
        except Exception as email_error:
            print(f"❌ Error al enviar email: {email_error}")
            # No fallar la operación si el email falla
        
        return JsonResponse({
            'success': True, 
            'message': '¡Gracias por tu interés! Te contactaremos en las próximas 24 horas.'
        })
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return JsonResponse({
            'success': False, 
            'message': 'Ocurrió un error al procesar tu solicitud. Inténtalo nuevamente.'
        }, status=500)


# FUNCIÓN AUXILIAR PARA EMAILS HTML (OPCIONAL)
def enviar_email_html(nuevo_contacto):
    """Función para enviar emails con formato HTML"""
    try:
        servicio_nombre = dict(info.SERVICIOS_CHOICES).get(nuevo_contacto.servicio, nuevo_contacto.servicio)
        
        # Contexto para el template
        context = {
            'nombre': nuevo_contacto.nombre,
            'email': nuevo_contacto.email,
            'empresa_proyecto': nuevo_contacto.empresa_proyecto,
            'servicio': servicio_nombre,
            'descripcion': nuevo_contacto.descripcion,
        }
        
        # Generar HTML y texto plano
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 650px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 25px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            padding: 40px 20px;
            text-align: center;
            color: white;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: bold;
        }}
        .header p {{
            margin-top: 8px;
            font-size: 16px;
        }}
        .content {{
            padding: 30px;
            color: #333;
        }}
        .section {{
            background: #f4f6f8;
            border-left: 5px solid #2575fc;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        .section h3 {{
            margin-top: 0;
            color: #2575fc;
        }}
        .section p {{
            margin: 6px 0;
            font-size: 15px;
        }}
        .cta {{
            text-align: center;
            margin-top: 30px;
        }}
        .button {{
            background: #2575fc;
            color: white !important;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
        }}
        .button:hover {{
            background: #1a5ed8;
        }}
        .footer {{
            background: #1c1c1e;
            color: #ccc;
            padding: 20px;
            text-align: center;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Nuevo Contacto</h1>
            <p>Has recibido una nueva solicitud en <strong>AURA Creativa</strong></p>
        </div>
        <div class="content">
            <div class="section">
                <h3>📋 Información del Cliente</h3>
                <p><strong>👤 Nombre:</strong> {nuevo_contacto.nombre}</p>
                <p><strong>📧 Email:</strong> {nuevo_contacto.email}</p>
                <p><strong>🏢 Empresa/Proyecto:</strong> {nuevo_contacto.empresa_proyecto}</p>
                <p><strong>🎯 Servicio:</strong> {servicio_nombre}</p>
            </div>
            <div class="section">
                <h3>💬 Descripción del Proyecto</h3>
                <p>{nuevo_contacto.descripcion}</p>
            </div>
            <div class="cta">
                <a href="mailto:{nuevo_contacto.email}" class="button">Responder al Cliente</a>
            </div>
        </div>
        <div class="footer">
            ✨ Es hora de crear algo increíble ✨ <br>
            Sistema de notificaciones AURA Creativa
        </div>
    </div>
</body>
</html>
"""

        
        send_mail(
            subject=f"🚀 Nuevo contacto desde AURA Creativa - {nuevo_contacto.nombre}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email HTML: {e}")
        return False


# Vista alternativa si prefieres manejar con formularios de Django
from django import forms

class ContactoForm(forms.ModelForm):
    class Meta:
        model = info
        fields = ['nombre', 'email', 'empresa_proyecto', 'servicio', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Tu nombre *',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Tu email *',
                'class': 'form-control',
                'required': True
            }),
            'empresa_proyecto': forms.TextInput(attrs={
                'placeholder': 'Empresa/Proyecto',
                'class': 'form-control',
                'required': True
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos sobre tu proyecto y objetivos...',
                'rows': 5,
                'class': 'form-control',
                'required': True
            })
        }

def contacto_form_view(request):
    """Vista alternativa usando formularios de Django con email"""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nuevo_contacto = form.save()
            
            # Enviar notificación por email
            try:
                enviar_email_html(nuevo_contacto)
            except Exception as e:
                print(f"❌ Error al enviar email: {e}")
            
            return JsonResponse({
                'success': True,
                'message': '¡Gracias por tu interés! Te contactaremos en las próximas 24 horas.'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Por favor, corrige los errores en el formulario.',
                'errors': form.errors
            })
    
    form = ContactoForm()
    return render(request, 'home.html', {'form': form})