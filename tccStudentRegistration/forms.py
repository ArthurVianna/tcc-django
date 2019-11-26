from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class EditarUsuarioForm(UserChangeForm):
    """EditarUsuarioForm."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )
