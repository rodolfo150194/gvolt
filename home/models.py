from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from modelcluster.fields import ParentalKey
from wagtail.admin.panels.field_panel import FieldPanel
from wagtail.admin.panels.group import MultiFieldPanel, FieldRowPanel
from wagtail.admin.panels.inline_panel import InlinePanel
from wagtail.blocks import ChoiceBlock
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm, AbstractFormSubmission
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField

from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet

from blocks.models import *
from mysite.settings.base import EMAIL_HOST_USER


class HomePage(Page):
    max_count = 1
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('logo'),
        ], heading="Información General"),
        MultiFieldPanel([
            InlinePanel('carousel_items', label="Carrusel de Imágenes"),
        ], heading="Carrusel"),

    ]

    def get_context(self, request):
        context = super().get_context(request)
        about = AboutPage.objects.live().first()
        services = ServicesPage.objects.live()
        context['about'] = about
        context['services'] = services
        return context


class Estadistica(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    page = ParentalKey('AboutPage', related_name='stats_items', on_delete=models.CASCADE)

    panels = [
        FieldPanel('name'),
        FieldPanel('amount'),
    ]

    def __str__(self):
        return self.nombre


class AboutPage(Page):
    template = 'about/about_page.html'
    max_count = 1
    intro_first = models.CharField(max_length=255, blank=True, verbose_name='Primer Texto')
    intro_second = models.CharField(max_length=255, blank=True, verbose_name='Segundo Texto')
    description_short = RichTextField(blank=True)
    body = RichTextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True)
    licence = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_extra = StreamField([
        ('simple_text', SimpleTextBlock()),
        ('rich_text', RichTextBlock()),
        ('text_image_above', TextImageTopBlock()),
        ('text_image_below', TextImageBottomBlock()),
        ('text_image_right', TextImageRightBlock()),
        ('text_image_left', TextImageLeftBlock()),
        ('primary_and_secondary_text', TextPrimarySecondaryBlock()),
        ('quote', QuoteBlock()),
        ('gallery', GalleryBlock()),
        ('embed_video', VideoEmbedBlock()),
        ('call_to_action', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('feature_list', FeatureListBlock()),
        ('counter', CounterBlock()),
        ('table', TablaCustomBlock([
            ('text', blocks.CharBlock()),
            ('numeric', blocks.FloatBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
        ])),
        ('tab', TabBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_first'),
        FieldPanel('intro_second'),
        FieldPanel('description_short'),
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('phone'),
        FieldPanel('address'),
        FieldPanel('email'),
        MultiFieldPanel([
            InlinePanel('social_media_links', label="Enlaces de Redes Sociales"),
        ], heading="Redes Sociales"),
        InlinePanel('fragments_information', label="Fragmentos de Información"),
        InlinePanel('stats_items', label="Estadisticas"),
        FieldPanel('content_extra', classname="full"),
    ]

    class Meta:
        verbose_name = "Información de la empresa"


class FragmentoInformacion(Orderable):
    page = ParentalKey(AboutPage, related_name='fragments_information', on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Orden')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    descripcion = RichTextField(max_length=1000, verbose_name='Descripción')
    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('order'),
        FieldPanel('name'),
        FieldPanel('descripcion'),
        FieldPanel('imagen'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class IconSocialWeb(models.Model):
    name = models.CharField(max_length=255)
    icon_class = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
        FieldPanel('icon_class'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Clases Fontawesome'


class SocialMediaLink(models.Model):
    page = ParentalKey('home.AboutPage', related_name='social_media_links', on_delete=models.CASCADE)
    icon = models.ForeignKey(IconSocialWeb, verbose_name='Icono', on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    url = models.URLField()

    panels = [
        FieldPanel('icon'),
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.name


# [Carrusel de imagenes] - Inicio
class CarouselItem(models.Model):
    page = ParentalKey('home.HomePage', related_name='carousel_items', on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='Imagen'
    )
    caption = models.CharField(max_length=250, blank=True, verbose_name='Texto primario')
    caption_2 = models.CharField(max_length=250, blank=True, verbose_name='Texto alternativo')

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
        FieldPanel('caption_2'),
    ]

    def __str__(self):
        return self.caption or "Carousel Item"


# [Carrusel de imagenes] - Fin


# [Preguntas y Respuestas] - Inicio
class FAQ(models.Model):
    ask = models.CharField(max_length=255)
    answer = RichTextField()
    page = ParentalKey('FaqPage', related_name='faq_items', on_delete=models.CASCADE)

    panels = [
        FieldPanel('ask'),
        FieldPanel('answer'),
    ]

    def __str__(self):
        return self.ask


class FaqPage(Page):
    max_count = 1

    content_panels = Page.content_panels + [
        InlinePanel('faq_items', label="FAQs"),
    ]

    class Meta:
        verbose_name = "Frequently Asked Questions"


# [Preguntas y Respuestas] - Fin


# [Partner] - Inicio
@register_snippet
class Partner(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='Imagen'
    )
    name = models.CharField(max_length=255, blank=True, verbose_name='Nombre')
    url = models.URLField(blank=True, verbose_name='URL del Partner')

    panels = [
        FieldPanel('image'),
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.name or "Partners"


# [Partner] - Fin


# [Galeria] - Fin
@register_snippet
class CategoriaGaleria(models.Model):
    nombre = models.CharField(max_length=255, blank=True, verbose_name='Nombre')

    panels = [
        FieldPanel('nombre'),
    ]

    def __str__(self):
        return self.nombre or "Categoría de la Galería"


class GaleriaPage(Page):
    template = "galeria/galeria_page.html"
    max_count = 1

    intro = models.CharField(blank=True, max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('galeria_items', label="Items de la Galería")
    ]

    class Meta:
        verbose_name = "Galería"
        verbose_name_plural = "Galería"

    def get_context(self, request):
        context = super().get_context(request)
        home_page = HomePage.objects.live().first()
        categorias_galeria = CategoriaGaleria.objects.all()
        context['home_page'] = home_page
        context['categorias_galeria'] = categorias_galeria
        return context


class GaleriaItem(Orderable):
    page = ParentalKey(GaleriaPage, on_delete=models.CASCADE, related_name='galeria_items')
    categoria = models.ForeignKey(CategoriaGaleria, verbose_name='Categoría de la Categoría', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image', verbose_name='Imagen Galería', on_delete=models.CASCADE, related_name='+'
    )
    url = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('categoria'),
        FieldPanel('titulo'),
        FieldPanel('image'),
        FieldPanel('url')
    ]

    def __str__(self):
        return self.titulo


# [Galeria] - Fin
class CustomIndexPage(Page):
    max_count = 1
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    subpage_types = ['CustomPage']


class CustomPage(Page):
    template = 'custom/custom_page.html'
    name = models.CharField(max_length=255)
    content_extra = StreamField([
        ('simple_text', SimpleTextBlock()),
        ('rich_text', RichTextBlock()),
        ('text_image_above', TextImageTopBlock()),
        ('text_image_below', TextImageBottomBlock()),
        ('text_image_right', TextImageRightBlock()),
        ('text_image_left', TextImageLeftBlock()),
        ('primary_and_secondary_text', TextPrimarySecondaryBlock()),
        ('quote', QuoteBlock()),
        ('gallery', GalleryBlock()),
        ('embed_video', VideoEmbedBlock()),
        ('call_to_action', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('feature_list', FeatureListBlock()),
        ('counter', CounterBlock()),
        ('table', TablaCustomBlock([
            ('text', blocks.CharBlock()),
            ('numeric', blocks.FloatBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
        ])),
        ('tab', TabBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('content_extra'),
    ]

    class Meta:
        verbose_name = "Custom Page"

    def get_context(self, request):
        context = super().get_context(request)
        about = AboutPage.objects.live().first()
        galeria = GaleriaPage.objects.first()
        context['galeria'] = galeria
        context['about'] = about

        return context


class ServicesIndexPage(Page):
    template = "services/services_index_page.html"

    max_count = 1
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    subpage_types = ['ServicesPage']


class ServicesPage(Page):
    template = "services/services_page.html"

    name = models.CharField(max_length=255)
    order = models.IntegerField(verbose_name='Orden')
    estado = models.BooleanField(default=True)
    description_short = RichTextField(blank=True)
    description = RichTextField(blank=True)
    icono = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_extra = StreamField([
        ('simple_text', SimpleTextBlock()),
        ('rich_text', RichTextBlock()),
        ('text_image_above', TextImageTopBlock()),
        ('text_image_below', TextImageBottomBlock()),
        ('text_image_right', TextImageRightBlock()),
        ('text_image_left', TextImageLeftBlock()),
        ('primary_and_secondary_text', TextPrimarySecondaryBlock()),
        ('quote', QuoteBlock()),
        ('gallery', GalleryBlock()),
        ('embed_video', VideoEmbedBlock()),
        ('call_to_action', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('feature_list', FeatureListBlock()),
        ('counter', CounterBlock()),
        ('table', TablaCustomBlock([
            ('text', blocks.CharBlock()),
            ('numeric', blocks.FloatBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
        ])),
        ('tab', TabBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('order'),
            FieldPanel('estado'),
            FieldPanel('description_short'),
            FieldPanel('description'),
            FieldPanel('icono'),
            FieldPanel('image'),
        ], heading="Services Infomation"),
        FieldPanel('content_extra', classname="full"),
    ]

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def get_context(self, request):
        context = super().get_context(request)
        about = AboutPage.objects.live().first()
        context['about'] = about
        return context


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    template = "form/form_page.html"
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        about = AboutPage.objects.live().first()
        context['about'] = about
        return context

    # intervenir form_save
    def process_form_submission(self, form):
        try:
            submition = self.get_submission_class().objects.create(
                form_data=form.cleaned_data,
                page=self
            )
        except Exception as e:
            raise Exception("There was a problem saving your data. Please try again later.")

        try:
            template = render_to_string('mail.html', {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'services': form.cleaned_data['services'],
                'message': form.cleaned_data['message'],

            })
            email_sender = EmailMessage(
                'Message for services',
                template,
                EMAIL_HOST_USER,
                [self.to_address]
            )
            email_sender.content_subtype = 'html'
            email_sender.send(fail_silently=False)
            print('Email sent successfully')
        except Exception as e:
            raise Exception("Your data has been saved, but there was a problem sending the email. We will contact you.")

        return submition