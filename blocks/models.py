from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

class SimpleTextBlock(blocks.CharBlock):

    class Meta:
        icon = "text"
        label = "Simple Text"

class RichTextBlock(blocks.RichTextBlock):

    class Meta:
        icon = "image"
        label = "Rich Text"

# Create your models here.
class TextImageTopBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="Image")
    texto_primario = blocks.CharBlock(help_text="Primary Text")
    texto_secundario = blocks.RichTextBlock(help_text="Secondary Text")

    class Meta:
        template = "blocks/text_image_top.html"
        icon = "image"
        label = "Text and image above"


class TextImageBottomBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="Image")
    texto_primario = blocks.CharBlock(help_text="Primary Text")
    texto_secundario = blocks.RichTextBlock(help_text="Secondary Text")

    class Meta:
        template = "blocks/text_image_bottom.html"
        icon = "image"
        label = "Text and Image below"


class TextPrimarySecondaryBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(help_text="Primary Text")
    texto_secundario = blocks.RichTextBlock(help_text="Secondary Text")

    class Meta:
        template = 'blocks/text_primary_secondary.html'
        icon = "image"
        label = "Primary and secondary text"


class SimpleTextBlock(blocks.CharBlock):
    class Meta:
        icon = "image"
        label = "Simple Text"


class TextImageRightBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(help_text="Primary Text")
    texto_secundario = blocks.RichTextBlock(help_text="Secondary Text")
    image = ImageChooserBlock(help_text="Image")

    class Meta:
        template = "blocks/text_image_right.html"
        icon = "image"
        label = "Text and Image Right"


class TextImageLeftBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="Image")
    texto_primario = blocks.CharBlock(help_text="Primary Text")
    texto_secundario = blocks.RichTextBlock(help_text="Secondary Text")

    class Meta:
        template = "blocks/text_image_left.html"
        icon = "image"
        label = "Text and Image Left"


class QuoteBlock(blocks.StructBlock):
    author = blocks.CharBlock(help_text="Header")
    cita = blocks.TextBlock(help_text="Quote")

    class Meta:
        template = "blocks/quote.html"
        icon = "openquote"
        label = "Quote"


class GalleryBlock(blocks.StructBlock):
    texto = blocks.CharBlock(help_text="Text")
    images = blocks.ListBlock(ImageChooserBlock(), help_text="Image gallery")

    class Meta:
        template = "blocks/gallery.html"
        icon = "image"
        label = "Image gallery"


class VideoEmbedBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Texto primario")
    url = blocks.URLBlock(required=True, help_text="URL del video")

    class Meta:
        template = "blocks/video_embed.html"
        icon = "media"
        label = "Video Embebido"


class CallToActionBlock(blocks.StructBlock):
    texto_primario = blocks.CharBlock(required=True, help_text="Call to action text")
    url = blocks.URLBlock(required=True, help_text="URL")

    class Meta:
        template = "blocks/call_to_action.html"
        icon = "plus"
        label = "Call to action"


class AccordionBlock(blocks.StructBlock):
    items = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True, help_text="Title")),
        ('content', blocks.RichTextBlock(required=True, help_text="Content"))
    ]))

    class Meta:
        template = "blocks/accordion.html"
        icon = "collapse-down"
        label = "Accordion"


class DocumentBlock(blocks.StructBlock):
    docs = blocks.ListBlock(blocks.StructBlock([
        ('nombre', blocks.CharBlock(required=True, help_text="Name")),
        ('documento', DocumentChooserBlock(required=True, help_text="Document")),
    ]))

    class Meta:
        template = 'blocks/document.html'
        icon = 'doc-full'
        label = 'Document'


class FeatureListBlock(blocks.StructBlock):
    features = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True, help_text="Title")),
        ('description', blocks.TextBlock(required=True, help_text="Description")),
        ('image', ImageChooserBlock(help_text="Image"))
    ]))

    class Meta:
        template = "blocks/feature_list.html"
        icon = "list-ul"
        label = "Feature List"


class CounterBlock(blocks.StructBlock):
    contadores = blocks.ListBlock(blocks.StructBlock([
        ('cantidad', blocks.IntegerBlock(required=True, help_text="Number")),
        ('nombre', blocks.CharBlock(required=True, help_text="Name Counter"))
    ]))

    class Meta:
        template = "blocks/counter.html"
        icon = "plus"
        label = "Counter"

class TablaCustomBlock(TypedTableBlock):
    class Meta:
        icon = 'table'
        label = 'Table'
        template = 'blocks/custom_table_block.html'

class TabBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Títle Tab")
    content = blocks.StreamBlock([
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
        ]))
    ], label="Content Tab")

    class Meta:
        icon = "form"
        label = "Tab"



