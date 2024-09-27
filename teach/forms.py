from typing import Any
from django import forms
from .models import Course
import cv2

class CourseAddForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New Course *', 'class' : ''},), help_text='Title should be less than 300 charecter.')
    short_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Describe somthing about your course *'}), label='About Course', help_text='Course description should be less than 600 charecter.')
    
    class Meta:
        model = Course
        fields = ('title', 'short_desc', 'category', 'price', 'off_price', 'thumbnail', 'preview_video')
        widgets = {
            'category' : forms.Select(attrs={'class' : 'w-100'}),
            'price' : forms.NumberInput(attrs={'placeholder' : '$ Regular Price'}),
            'off_price' : forms.NumberInput(attrs={'placeholder' : '$ Discounted Price'}),
            'thumbnail' : forms.FileInput(attrs={'class' : 'inputfile', 'id': 'createinputfile', 'required' : True})
        }

    def clean(self):
        # Call the parent clean method first to populate cleaned_data
        cleaned_data = super().clean()  
        price = cleaned_data.get('price')
        off_price = cleaned_data.get('off_price')
        image = cleaned_data.get('thumbnail')
        video = cleaned_data.get('preview_video')

        # Validate the prices
        if price is not None and off_price is not None:
            if off_price > price:
                self.add_error('off_price', 'Offer price can’t be greater than the original price.')

        # Check if the image size exceeds 100 KB
        if image:
            if image.size > 100 * 1024:
                self.add_error('thumbnail', 'Image size must be less than 100 KB.')

        # if video:
        #     data = cv2.VideoCapture(video)
        #     if not data.isOpened():
        #         self.add_error('preview_video', 'Unable to open video file.')
        #         return cleaned_data
            
        #     frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        #     fps = data.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if not available
        #     seconds = round(frames / fps)
        #     if seconds > 10:
        #         self.add_error('preview_video', 'Video should be less than 10 seconds.')

        return cleaned_data
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if args and args[0]:
            if not self.data.get('title'):
                self.fields['title'].widget.attrs['class'] = 'field-error'
            if not self.data.get('short_desc'):
                self.fields['short_desc'].widget.attrs['class'] = 'field-error'
            if not self.data.get('category'):
                self.fields['category'].widget.attrs.update({'class' : 'w-100 field-error'})
            if not self.data.get('price'):
                self.fields['price'].widget.attrs.update({'class' : 'field-error'})


