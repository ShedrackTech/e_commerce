from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from django.utils.timezone import localtime

from .models import Category, Product, CustomUser, ContactMessage


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


# ── Contact Messages ──────────────────────────────────────────────────────────

class IsReadFilter(admin.SimpleListFilter):
    title = 'read status'
    parameter_name = 'is_read'

    def lookups(self, request, model_admin):
        return [
            ('unread', '🔴 Unread'),
            ('read',   '✅ Read'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'unread':
            return queryset.filter(is_read=False)
        if self.value() == 'read':
            return queryset.filter(is_read=True)


class IsRepliedFilter(admin.SimpleListFilter):
    title = 'reply status'
    parameter_name = 'is_replied'

    def lookups(self, request, model_admin):
        return [
            ('yes', '💬 Replied'),
            ('no',  '⏳ Awaiting reply'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(replied_at__isnull=False)
        if self.value() == 'no':
            return queryset.filter(replied_at__isnull=True)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # ── List view ──
    list_display   = ['status_badge', 'reply_badge', 'name', 'email_link',
                      'subject_display', 'received_at', 'reply_action']
    list_filter    = [IsReadFilter, IsRepliedFilter, 'subject', 'created_at']
    search_fields  = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    ordering       = ['-created_at']
    list_per_page  = 25

    # ── Detail view ──
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at',
                       'reply', 'replied_at', 'replied_by']
    fieldsets = (
        ('Sender', {
            'fields': ('name', 'email'),
        }),
        ('Message', {
            'fields': ('subject', 'message', 'created_at'),
        }),
        ('Reply', {
            'fields': ('reply', 'replied_at', 'replied_by'),
            'classes': ('collapse',),
            'description': 'Use the "Send Reply" button at the top to compose and send a reply.',
        }),
        ('Status', {
            'fields': ('is_read',),
        }),
    )
    actions = ['mark_as_read', 'mark_as_unread']

    # ── Extra URL for the reply view ──
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:pk>/reply/',
                self.admin_site.admin_view(self.reply_view),
                name='shop_contactmessage_reply',
            ),
        ]
        return custom + urls

    # ── Reply view ──
    def reply_view(self, request, pk):
        obj = get_object_or_404(ContactMessage, pk=pk)
        change_url = reverse('admin:shop_contactmessage_change', args=[pk])

        if request.method == 'POST':
            reply_body = request.POST.get('reply_body', '').strip()

            if not reply_body:
                messages.error(request, 'Reply cannot be empty.')
                return redirect(request.path)

            # Send the email
            try:
                send_mail(
                    subject=f'Re: {obj.get_subject_display()} — {settings.SITE_NAME if hasattr(settings, "SITE_NAME") else "Our Store"}',
                    message=(
                        f'Hi {obj.name},\n\n'
                        f'{reply_body}\n\n'
                        f'—\nThe Support Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'Failed to send email: {e}')
                return redirect(request.path)

            # Save reply to the model
            obj.reply      = reply_body
            obj.replied_at = timezone.now()
            obj.replied_by = request.user
            obj.is_read    = True
            obj.save(update_fields=['reply', 'replied_at', 'replied_by', 'is_read'])

            messages.success(request, f'Reply sent to {obj.email}.')
            return redirect(change_url)

        # GET — render the reply form
        context = {
            **self.admin_site.each_context(request),
            'title': f'Reply to {obj.name}',
            'obj': obj,
            'change_url': change_url,
            'opts': self.model._meta,
            # Pre-fill with previous reply if editing
            'reply_body': obj.reply,
        }
        return TemplateResponse(request, 'admin/shop/contactmessage/reply.html', context)

    # ── Custom columns ──

    @admin.display(description='')
    def status_badge(self, obj):
        if obj.is_read:
            return mark_safe('<span title="Read">&#x2705;</span>')
        return mark_safe('<span title="Unread" style="color:#dc3545;">&#9679;</span>')

    @admin.display(description='')
    def reply_badge(self, obj):
        if obj.is_replied:
            return mark_safe('<span title="Replied" style="color:#28a745;">&#x1F4AC;</span>')
        return mark_safe('<span title="No reply yet" style="opacity:.3;">&#x1F4AC;</span>')

    @admin.display(description='Email')
    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    @admin.display(description='Subject')
    def subject_display(self, obj):
        return obj.get_subject_display()

    @admin.display(description='Received')
    def received_at(self, obj):
        return localtime(obj.created_at).strftime('%d %b %Y, %H:%M')

    @admin.display(description='Reply')
    def reply_action(self, obj):
        url = reverse('admin:shop_contactmessage_reply', args=[obj.pk])
        if obj.is_replied:
            return format_html(
                '<a href="{}" style="color:#6c757d;">Edit reply</a>', url
            )
        return format_html(
            '<a href="{}" style="color:#007bff;font-weight:600;">Send reply</a>', url
        )

    # ── Bulk actions ──

    @admin.action(description='✅ Mark selected as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')

    @admin.action(description='🔴 Mark selected as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')

    # Auto-mark as read when admin opens a message
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])

        reply_url = reverse('admin:shop_contactmessage_reply', args=[object_id])
        extra_context = extra_context or {}
        extra_context['reply_url'] = reply_url
        extra_context['is_replied'] = obj.is_replied if obj else False
        return super().change_view(request, object_id, form_url, extra_context)