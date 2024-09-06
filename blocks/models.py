from django.db import models

# Create your models here.
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


# Create your models here.
class TextImageTopBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Imagen")
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    texto_secundario = blocks.RichTextBlock(required=True, help_text="Texto secundario")

    class Meta:
        template = "blocks/text_image_top.html"
        icon = "image"
        label = "Texto e Imagen arriba "

class TextImageBottomBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Imagen")
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    texto_secundario = blocks.RichTextBlock(required=True, help_text="Texto secundario")

    class Meta:
        template = "blocks/text_image_bottom.html"
        icon = "image"
        label = "Texto e Imagen debajo "

class TextPrimarySecondaryBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    texto_secundario = blocks.RichTextBlock(required=True, help_text="Texto secundario")

    class Meta:
        template = 'blocks/text_primary_secondary.html'
        icon = "image"
        label = "Texto primario y secundario"


class SimpleTextBlock(blocks.CharBlock):

    class Meta:
        icon = "image"
        label = "Texto Simple"


class TextImageRightBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    texto_secundario = blocks.RichTextBlock(required=True, help_text="Texto secundario")
    image = ImageChooserBlock(required=True, help_text="Imagen")

    class Meta:
        template = "blocks/text_image_right.html"
        icon = "image"
        label = "Texto e Imagen Derecha"


class TextImageLeftBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Imagen")
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    texto_secundario = blocks.RichTextBlock(required=True, help_text="Texto secundario")

    class Meta:
        template = "blocks/text_image_left.html"
        icon = "image"
        label = "Texto e Imagen Izquierda"


class QuoteBlock(blocks.StructBlock):
    author = blocks.CharBlock(required=True, help_text="Autor")
    cita = blocks.TextBlock(required=True, help_text="Cita")

    class Meta:
        template = "blocks/quote.html"
        icon = "openquote"
        label = "Cita"


class GalleryBlock(blocks.StructBlock):
    texto = blocks.CharBlock(required=True, help_text="Texto")
    images = blocks.ListBlock(ImageChooserBlock(), help_text="Galería de imágenes")

    class Meta:
        template = "blocks/gallery.html"
        icon = "image"
        label = "Galería de Imágenes"


class VideoEmbedBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    url = blocks.URLBlock(required=True, help_text="URL del video")

    class Meta:
        template = "blocks/video_embed.html"
        icon = "media"
        label = "Video Embebido"


class CallToActionBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Texto de la llamada a la acción")
    url = blocks.URLBlock(required=True, help_text="URL a la que se dirige")

    class Meta:
        template = "blocks/call_to_action.html"
        icon = "plus"
        label = "Llamada a la Acción"


class AccordionBlock(blocks.StructBlock):
    items = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True, help_text="Título del acordeón")),
        ('content', blocks.RichTextBlock(required=True, help_text="Contenido del acordeón"))
    ]))

    class Meta:
        template = "blocks/accordion.html"
        icon = "collapse-down"
        label = "Acordeón"


class DocumentBlock(blocks.StructBlock):
    docs = blocks.ListBlock(blocks.StructBlock([
        ('nombre', blocks.CharBlock(required=True, help_text="Nombre del documento")),
        ('documento', DocumentChooserBlock(required=True, help_text="Documento")),
    ]))
    class Meta:
        template = 'blocks/document.html'
        icon = 'doc-full'
        label = 'Document'


class FeatureListBlock(blocks.StructBlock):
    features = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True, help_text="Título de la característica")),
        ('description', blocks.TextBlock(required=True, help_text="Descripción de la característica")),
        ('image', ImageChooserBlock(help_text="Imagen de la característica"))
    ]))

    class Meta:
        template = "blocks/feature_list.html"
        icon = "list-ul"
        label = "Lista de Características"


class CounterBlock(blocks.StructBlock):
    contadores = blocks.ListBlock(blocks.StructBlock([
        ('cantidad', blocks.IntegerBlock(required=True, help_text="Número a mostrar")),
        ('nombre', blocks.CharBlock(required=True, help_text="Etiqueta del contador"))
    ]))

    class Meta:
        template = "blocks/counter.html"
        icon = "plus"
        label = "Contador"



class TabBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Título de la pestaña")
    content = blocks.StreamBlock([
        # ('infografia', InfografiaBlock()),
        ('texto_imagen_arriba', TextImageTopBlock()),
        ('texto_imagen_abajo', TextImageBottomBlock()),
        ('texto_simple', SimpleTextBlock()),
        ('texto_imagen_derecha', TextImageRightBlock()),
        ('texto_imagen_izquierda', TextImageLeftBlock()),
        ('texto_primario_y_secundario', TextPrimarySecondaryBlock()),
        ('cita', QuoteBlock()),
        ('galeria', GalleryBlock()),
        ('video_embebido', VideoEmbedBlock()),
        ('boton_mas_accion', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        ('caracteristica', FeatureListBlock()),
        ('contador', CounterBlock()),
    ], label="Contenido de la pestaña")

    class Meta:
        icon = "form"
        label = "Pestaña"
