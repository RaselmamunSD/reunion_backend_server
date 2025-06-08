from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

class ReunionAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _('Reunion Admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('Reunion Administration')

    # Text to put at the top of the admin index page.
    index_title = _('Reunion Dashboard')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'

admin_site = ReunionAdminSite(name='admin')

# Custom CSS for admin
class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = """
            :root {
                --primary: #2E7D32;
                --secondary: #FFC107;
                --accent: #1B5E20;
                --primary-fg: #fff;
                --body-fg: #333;
                --body-bg: #f8f9fa;
                --header-color: #fff;
                --header-bg: var(--primary);
                --header-link-color: #fff;
                --breadcrumbs-fg: #666;
                --breadcrumbs-link-fg: var(--primary);
                --link-fg: var(--primary);
                --link-hover-color: var(--accent);
                --link-selected-fg: var(--primary);
                --button-fg: #fff;
                --button-bg: var(--primary);
                --button-hover-bg: var(--accent);
                --default-button-bg: var(--primary);
                --default-button-hover-bg: var(--accent);
                --close-button-bg: #888;
                --close-button-hover-bg: #666;
                --delete-button-bg: #ba2121;
                --delete-button-hover-bg: #a41515;
                --object-tools-fg: var(--button-fg);
                --object-tools-bg: var(--primary);
                --object-tools-hover-bg: var(--accent);
            }

            /* Header styling */
            #header {
                background: var(--header-bg);
                color: var(--header-color);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            #branding h1 {
                font-weight: 600;
            }

            /* Sidebar styling */
            #content-related {
                background: #fff;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }

            /* Card styling */
            .module {
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }

            .module h2, .module caption {
                background: var(--primary);
                color: var(--primary-fg);
                font-weight: 600;
                padding: 12px;
                border-radius: 4px 4px 0 0;
            }

            /* Button styling */
            .button, input[type=submit], input[type=button], .submit-row input {
                background: var(--button-bg);
                color: var(--button-fg);
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
                transition: all 0.2s ease;
            }

            .button:hover, input[type=submit]:hover, input[type=button]:hover {
                background: var(--button-hover-bg);
            }

            /* Table styling */
            #changelist table thead th {
                background: var(--primary);
                color: var(--primary-fg);
                font-weight: 600;
            }

            #changelist table tbody tr:hover {
                background: rgba(46, 125, 50, 0.05);
            }

            /* Form styling */
            .form-row {
                padding: 12px;
                border-bottom: 1px solid #eee;
            }

            .form-row label {
                font-weight: 500;
                color: var(--body-fg);
            }

            /* Login page styling */
            .login {
                background: var(--body-bg);
            }

            .login #container {
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            /* Dashboard styling */
            .dashboard .module table th {
                width: 100%;
            }

            .dashboard .module table td {
                white-space: nowrap;
            }

            /* Recent actions module */
            .module ul.actionlist {
                padding-left: 0;
            }

            .module ul.actionlist li {
                padding: 8px 12px;
                border-bottom: 1px solid #eee;
            }

            .module ul.actionlist li:last-child {
                border-bottom: none;
            }
        """
        return context

# Create custom admin site instance
admin_site = CustomAdminSite(name='admin')

# Register your models with the custom admin site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class CustomModelAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        """
        Override the response_change method to ensure proper state management
        """
        if "_continue" in request.POST:
            # If continuing to edit, redirect to the same page
            return super().response_change(request, obj)
        
        # For all other cases, redirect to the changelist view
        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)
        
        msg_dict = {
            "name": opts.verbose_name,
            "obj": str(obj),
        }
        
        msg = format_html(
            _("The {name} '{obj}' was changed successfully."),
            **msg_dict
        )
        self.message_user(request, msg, messages.SUCCESS)
        
        # Redirect to the changelist view
        redirect_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_changelist",
            current_app=self.admin_site.name,
        )
        
        # Add preserved filters if any
        if preserved_filters:
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts},
                redirect_url
            )
        
        return HttpResponseRedirect(redirect_url)

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin) 