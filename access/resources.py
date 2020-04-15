# your_app_name/resources.py
from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import PreRecordedUser

class PreRecordedUserResource(resources.ModelResource):
    date_of_birth = fields.Field(
        column_name='date_of_birth',
        attribute='date_of_birth',
        widget=DateWidget(format='%Y-%m-%d')
    )

    class Meta:
        model = PreRecordedUser
        fields = (
            'username',
            'identity_number',
            'nationality',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'email',
            'mob_number',
            'perm_add_village',
            'perm_add_gewog',
            'perm_add_dzongkhag',
            'father_name',
            'mother_name',
            'profile_picture',
            'is_gyalsung',
            'academy_code',
            'role',
            'access_level',
            'agency_name',
            'agency_code',
            'user_code',
            'parent_occupation',
            'guardian_name',
            'guardian_occupation',
            'parent_status',
            'current_living_with',
            'user_role_agency',
            'user_class',
            'user_sub_class',
        )
        import_id_fields = ('username', 'identity_number', 'email')
        export_order = fields
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # Ensure required fields are present
        required_fields = [
            'username', 'identity_number', 'nationality', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'email', 'mob_number', 'perm_add_village',
            'perm_add_gewog', 'perm_add_dzongkhag'
        ]
        for field in required_fields:
            if field not in row or not row[field]:
                raise ValueError(f"Missing or empty required field: {field}")

    def after_import_instance(self, instance, new, row, **kwargs):
        # Set default values for non-nullable fields if not provided
        instance.is_active = row.get('is_active', True)
        instance.is_staff = row.get('is_staff', False)
        instance.date_joined = row.get('date_joined', timezone.now())