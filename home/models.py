from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels.field_panel import FieldPanel
from wagtail.admin.panels.group import MultiFieldPanel
from wagtail.admin.panels.inline_panel import InlinePanel
from wagtail.fields import RichTextField, StreamField

from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet

from blocks.models import *


class HomePage(Page):
    max_count = 1
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('body'),
            FieldPanel('logo'),
        ], heading="Información General"),
        MultiFieldPanel([
            InlinePanel('carousel_items', label="Carrusel de Imágenes"),
        ], heading="Carrusel"),

    ]


class AboutPage(Page):
    template = 'about/about_page.html'
    max_count = 1
    intro = models.CharField(max_length=255, blank=True, verbose_name='Texto primario')
    texto_secundario = RichTextField(verbose_name='Texto secundario', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True)
    licencia = models.CharField(max_length=255,blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    contenido_extra = StreamField([
        ('texto_imagen_arriba', TextImageTopBlock()),
        ('texto_imagen_abajo', TextImageBottomBlock()),
        ('texto_imagen_derecha', TextImageRightBlock()),
        ('texto_imagen_izquierda', TextImageLeftBlock()),
        ('texto_primario_y_secundario', TextPrimarySecondaryBlock()),
        ('cita', QuoteBlock()),
        ('galeria', GalleryBlock()),
        ('video_embebido', VideoEmbedBlock()),
        ('boton_mas_accion', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('caracteristica', FeatureListBlock()),
        ('estadisticas', CounterBlock()),
        ('documento', DocumentBlock()),
        ('pestanna', TabBlock()),
        # Puedes agregar más bloques aquí
    ], null=True, blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('texto_secundario'),
        FieldPanel('image'),
        FieldPanel('phone'),
        FieldPanel('address'),
        FieldPanel('email'),
        MultiFieldPanel([
            InlinePanel('social_media_links', label="Enlaces de Redes Sociales"),
        ], heading="Redes Sociales"),
        FieldPanel('contenido_extra', classname="full"),
    ]

    class Meta:
        verbose_name = "Información de la empresa"


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
    caption = models.CharField(max_length=250, blank=True, verbose_name='Texto alternativo')

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return self.caption or "Carousel Item"


# [Carrusel de imagenes] - Fin


# [Preguntas y Respuestas] - Inicio
class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = RichTextField()
    page = ParentalKey('FaqPage', related_name='faq_items', on_delete=models.CASCADE)

    panels = [
        FieldPanel('pregunta'),
        FieldPanel('respuesta'),
    ]

    def __str__(self):
        return self.pregunta

class FaqPage(Page):
    max_count = 1

    content_panels = Page.content_panels + [
        InlinePanel('faq_items', label="FAQs"),
    ]

    class Meta:
        verbose_name = "Preguntas Frecuentes"

# [Preguntas y Respuestas] - Fin


# [Estadistica importante] - Inicio
class Estadistica(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    page = ParentalKey('EstadisticaPage', related_name='stats_items', on_delete=models.CASCADE)

    panels = [
        FieldPanel('nombre'),
        FieldPanel('cantidad'),
    ]

    def __str__(self):
        return self.nombre


class EstadisticaPage(Page):
    max_count = 1

    content_panels = Page.content_panels + [
        InlinePanel('stats_items', label="Estadisticas"),
    ]

    class Meta:
        verbose_name = "Estadisticas"


# [Estadistica Importante] - Fin

# [Programas] - Inicio
@register_snippet
class Partner(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='Imagen'
    )
    nombre = models.CharField(max_length=255, blank=True, verbose_name='Nombre')
    url = models.URLField(blank=True, verbose_name='URL del Partner')

    panels = [
        FieldPanel('image'),
        FieldPanel('nombre'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.nombre or "Patrocinadores"
# [Programas] - Fin


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


class CustomPage(Page):
    template = 'custom/custom_page.html'
    nombre = models.CharField(max_length=255)
    body = StreamField([
        ('texto_imagen_arriba', TextImageTopBlock()),
        ('texto_imagen_abajo', TextImageBottomBlock()),
        ('texto_imagen_derecha', TextImageRightBlock()),
        ('texto_imagen_izquierda', TextImageLeftBlock()),
        ('texto_primario_y_secundario', TextPrimarySecondaryBlock()),
        ('cita', QuoteBlock()),
        ('galeria', GalleryBlock()),
        ('video_embebido', VideoEmbedBlock()),
        ('boton_mas_accion', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('caracteristica', FeatureListBlock()),
        ('estadisticas', CounterBlock()),
        ('documento', DocumentBlock()),
        ('pestannas', TabBlock()),
        # Puedes agregar más bloques aquí
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('nombre'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Página personalizada"


    def get_context(self, request):
        context = super().get_context(request)
        home_page = HomePage.objects.live().first()
        galeria = GaleriaPage.objects.first()
        context['galeria'] = galeria
        context['home_page'] = home_page

        return context


