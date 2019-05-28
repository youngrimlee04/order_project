from django.forms import ModelForm
from .models import Partner

class PartnerForm(ModelForm):
    class Meta:
        model=Partner
        fields=(
            "name",
            "contact",
            "address",
            "description"
        )
