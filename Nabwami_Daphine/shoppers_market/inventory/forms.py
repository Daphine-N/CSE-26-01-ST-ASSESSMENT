from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product', 'category', 'price', 'quantity', 'color', 'image']
        widgets = {
            'product': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '#645341'
            }),
            'product': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': ' product name (letters only)'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control', 
               'placeholder': 'e.g., Smart Phones, Fashion'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter price in UGX'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter quantity'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Black, White, Blue'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            }),
        }
    
    def clean_product(self):
        product= self.cleaned_data.get('product')
        
        # Validation 1: Required
        if not product:
            raise ValidationError(' Product ID is required')
        
        # Validation 2: Must start with #
        if not product.startswith('#'):
            raise ValidationError(' Product ID must start with # (e.g., #645341)')
        
        # Validation 3: After # must be numbers only (no letters allowed)
        id_number = product[1:]
        if not id_number:
            raise ValidationError(' Please enter numbers after #')
        
        if not id_number.isdigit():
            raise ValidationError(' Product ID must contain ONLY numbers after # (no letters allowed)')
        
        # Validation 4: Check unique
        if Product.objects.filter(product=product).exists():
            raise ValidationError(' Product ID already exists')
        
        return product
    
    def clean_product(self):
        product = self.cleaned_data.get('product')
        
        # Validation 1: Required
        if not product:
            raise ValidationError(' Product name is required')
        
        # Validation 2: Minimum length
        if len(product) < 2:
            raise ValidationError(' Product name must be at least 2 characters')
        
        # Validation 3: Maximum length
        if len(product) > 200:
            raise ValidationError(' Product name must be less than 200 characters')
        
        # Validation 4: No numbers allowed in name
        if any(char.isdigit() for char in product):
            raise ValidationError(' Product name cannot contain numbers (letters and spaces only)')
        
        # Validation 5: Only letters, spaces, and basic punctuation
        if not all(char.isalpha() or char.isspace() or char in ".-'" for char in product):
            raise ValidationError(' Product name can only contain letters, spaces, dots, hyphens, and apostrophes')
        
        return product  
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        
        # Validation 1: Required
        if not category:
            raise ValidationError(' Category is required')
        
        # Validation 2: Minimum length
        if len(category) < 2:
            raise ValidationError(' Category must be at least 2 characters')
        
        # Validation 3: Maximum length
        if len(category) > 100:
            raise ValidationError(' Category must be less than 100 characters')
        
        # Validation 4: No numbers allowed in category
        if any(char.isdigit() for char in category):
            raise ValidationError('Category cannot contain numbers (letters and spaces only)')
        
        # Validation 5: Only letters and spaces
        if not all(char.isalpha() or char.isspace() for char in category):
            raise ValidationError('Category can only contain letters and spaces')
        
        return category
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        
        # Validation 1: Required
        if not price:
            raise ValidationError(' Price is required')
        
        # Validation 2: Must be positive number
        if price <= 0:
            raise ValidationError(' Price must be greater than 0')
        
        # Validation 3: Maximum price limit
        if price > 999999999:
            raise ValidationError(' Price is too high (max 999,999,999)')
        
        # Validation 4: Must be integer (no decimals)
        if isinstance(price, float) and not price.is_integer():
            raise ValidationError(' Price must be a whole number (no decimals)')
        
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        
        # Validation 1: Required
        if quantity is None:
            raise ValidationError(' Quantity is required')
        
        # Validation 2: Cannot be negative
        if quantity < 0:
            raise ValidationError(' Quantity cannot be negative')
        
        # Validation 3: Maximum quantity limit
        if quantity > 999999:
            raise ValidationError(' Quantity is too high (max 999,999)')
        
        # Validation 4: Must be integer
        if isinstance(quantity, float) and not quantity.is_integer():
            raise ValidationError(' Quantity must be a whole number')
        
        return quantity
    
    def clean_color(self):
        color = self.cleaned_data.get('color')
        
        # Validation: If provided, check it's valid
        if color:
            # No numbers in color name
            if any(char.isdigit() for char in color):
                raise ValidationError('Color cannot contain numbers')
            
            # Only letters allowed
            if not all(char.isalpha() for char in color.replace(' ', '')):
                raise ValidationError(' Color can only contain letters and spaces')
        
        return color if color else None
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Validation 1: Check file size (max 5MB = 5 * 1024 * 1024 bytes)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError(' Image file size must be less than 5MB')
            
            # Validation 2: Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            file_extension = None
            for ext in valid_extensions:
                if image.name.lower().endswith(ext):
                    file_extension = ext
                    break
            
            if not file_extension:
                raise ValidationError(' Only image files (JPG, PNG, GIF, WEBP, BMP) are allowed')
            
            # Validation 3: Check file type by content (basic check)
            if not image.content_type.startswith('image/'):
                raise ValidationError(' File must be an image')
        
        return image