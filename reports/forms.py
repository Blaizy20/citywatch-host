from django import forms
from .models import Announcement, Report, ReportFeedback


class AnnouncementForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image must be 5 MB or smaller.')
        return image

    class Meta:
        model = Announcement
        fields = ['title', 'announcement_type', 'content', 'image', 'event_date', 'is_published', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-outline-variant bg-surface px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary',
            }),
            'announcement_type': forms.Select(attrs={
                'class': 'w-full border border-outline-variant bg-surface px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary',
            }),
            'content': forms.Textarea(attrs={
                'rows': 6,
                'class': 'w-full resize-y border border-outline-variant bg-surface px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary',
            }),
            'event_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full border border-outline-variant bg-surface px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary',
                },
            ),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-on-surface-variant file:mr-3 file:border-0 file:bg-surface-container-low file:px-3 file:py-2 file:text-sm file:font-medium file:text-primary hover:file:bg-surface-container',
                'accept': 'image/*',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'mt-0.5 h-4 w-4 border-outline-variant text-primary focus:ring-primary',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'mt-0.5 h-4 w-4 border-outline-variant text-primary focus:ring-primary',
            }),
        }

class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [
            choice for choice in self.fields['category'].choices if choice[0]
        ]

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Photo must be 5 MB or smaller.')
        return photo

    class Meta:
        model = Report
        fields = ['title', 'description', 'category', 'urgency', 'photo', 'barangay', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ReportFeedbackForm(forms.ModelForm):
    class Meta:
        model = ReportFeedback
        fields = ['rating', 'comment']