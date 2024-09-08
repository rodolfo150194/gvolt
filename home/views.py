# def contacto(request):
#     home_page = HomePage.objects.live().first()
#     galeria = GaleriaPage.objects.live().first()
#     if request.method == 'POST':
#         form = ContactForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             # instancia = MensajeContacto(
#             #     nombre=form.cleaned_data['nombre'],
#             #     tipo_mensaje=request.POST.get('tipo_mensaje'),
#             #     correo=form.cleaned_data['correo'],
#             #     telefono=form.cleaned_data['telefono'],
#             #     especialidad=form.cleaned_data['especialidad'],
#             #     asunto=form.cleaned_data['asunto'],
#             #     mensaje=form.cleaned_data['mensaje'],
#             #     adjunto=form.cleaned_data['adjunto']
#             # )
#             form.save()
#             # instancia.save()
#             messages.success(request, '¡Su mensaje ha sido enviado. Gracias!')
#             return redirect('home:contacto')
#     else:
#         form = ContactForm()
#
#     context = {}
#     context['home_page'] = home_page
#     context['galeria'] = galeria
#     context['form'] = form
#     return render(request, 'contacto.html', context)
