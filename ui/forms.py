from django import forms
from ui.models import LanguageModel
from dal import autocomplete
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, ngettext as n_

model_name_field = forms.ModelChoiceField(
    required=False,
    queryset=LanguageModel.objects.all(),
    widget=autocomplete.ModelSelect2(url=reverse_lazy("user_interface:model_name-autocomplete"),
                                    attrs={"data-placeholder": _("model_name-placeholder")},
                                    )
)

class QuestionForm(forms.Form):
    question = forms.CharField()
    
class ModelSelectForm(forms.Form):
    model_name = model_name_field
