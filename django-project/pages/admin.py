from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from .forms import PageAdminForm
from .models import Page
from .widgets import FilerImagePreviewWidget


class PageImageInline(admin.TabularInline):
    model = Page.images.through
    extra = 0
    fields = ('image', 'preview')
    raw_id_fields = ('image',)
    readonly_fields = ('preview',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            preview_url = reverse(
                'admin:pages_page_filer_image_preview',
                kwargs={'image_id': 0},
                current_app=self.admin_site.name,
            ).replace('/0/', '/__image_id__/')
            kwargs['widget'] = FilerImagePreviewWidget(
                db_field.remote_field,
                self.admin_site,
                preview_url,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Preview')
    def preview(self, page_image):
        if not page_image.image_id:
            return '—'
        return format_html(
            '<img src="{}" alt="" width="120" height="80" style="object-fit: contain;">',
            page_image.image.url,
        )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    exclude = ('images',)
    inlines = (PageImageInline,)
    list_display = ('title', 'slug', 'author', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated')
    search_fields = ('title', 'content')

    def get_urls(self):
        return [
            path(
                'filer-image-preview/<int:image_id>/',
                self.admin_site.admin_view(self.filer_image_preview),
                name='pages_page_filer_image_preview',
            ),
            *super().get_urls(),
        ]

    def filer_image_preview(self, request, image_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        image = get_object_or_404(Page.images.field.remote_field.model, pk=image_id)
        return JsonResponse({'url': image.url})
