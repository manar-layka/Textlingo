from django import forms


class TranslationForm(forms.Form):
    content_type = forms.ChoiceField(
        choices=[("HTML", "HTML"), ("plain text", "Plain Text")],
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Content Type",
    )
    original_text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), label="Original Text")
