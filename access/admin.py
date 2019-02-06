import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import CustomUser, Agency, UserAgency, PreRecordedUser


class UserAgencyInline(admin.TabularInline):
    model = UserAgency

class PreRecordedUserAdmin(admin.ModelAdmin):
    list_display = ('identity_number', 'first_name', 'last_name',
                    'date_of_birth', 'gender', 'is_registered')
    search_fields = ['identity_number', 'first_name', 'last_name']
    list_filter = ['is_registered']
    ordering = ['identity_number']
    actions = ['mark_as_registered', 'export_users', 'import_users']

    def mark_as_registered(self, request, queryset):
        queryset.update(is_registered=True)
    mark_as_registered.short_description = "Mark selected users as registered"

    def export_users(self, request, queryset):
        # Create a CSV response with appropriate headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pre_recorded_users.csv"'

        # Create a CSV writer object
        csv_writer = csv.writer(response)

        # Write header row
        csv_writer.writerow(['identity_number', 'first_name', 'last_name', 'date_of_birth', 'gender', 'is_registered'])

        # Write data rows
        for user in queryset:
            csv_writer.writerow([user.identity_number, user.first_name, user.last_name, user.date_of_birth, user.gender, user.is_registered])

        return response
    export_users.short_description = "Export selected users as CSV"

    def import_users(self, request, queryset):
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            # Ensure the uploaded file is a CSV
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('File is not a CSV', status=400)

            # Decode and process the CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                # Create or update PreRecordedUser objects based on CSV data
                PreRecordedUser.objects.update_or_create(
                    identity_number=row['identity_number'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'date_of_birth': row['date_of_birth'],
                        'gender': row['gender'],
                        'is_registered': row['is_registered'],
                    }
                )

            self.message_user(request, "CSV file imported successfully.")
            return None

        return HttpResponse('No CSV file uploaded', status=400)

    import_users.short_description = "Import users from CSV"


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'active_agency')
    inlines = [UserAgencyInline]

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'role', 'active_agency'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'identity_number', 'nationality', 'mob_number', 'father_name', 'mother_name'),
        }),
        ('Address Information', {
            'fields': ('perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag'),
        }),
        ('Gyalsuung Information', {
            'fields': ('is_gyalsung', 'academy_code'),
        }),
    )

    def active_agency(self, obj):
        try:
            active_agency = obj.agency.filter(is_active=True).first()
            return active_agency.agency_name if active_agency else None
        except AttributeError:
            return None

    active_agency.short_description = 'Active Agency'


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name',)
    inlines = [UserAgencyInline]


class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'get_is_active')

    def get_is_active(self, obj):
        # Check if the associated user is active
        return obj.user.is_active if obj.user else False
    get_is_active.short_description = 'Is Active'


admin.site.register(PreRecordedUser, PreRecordedUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(UserAgency, UserAgencyAdmin)
