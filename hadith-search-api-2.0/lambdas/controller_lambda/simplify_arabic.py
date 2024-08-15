import re

def simplify_arabic_text(text: str):
    # Mapping of complex letters to simple ones
    complex_to_simple = {
        'أ': 'ا',  # Alif with hamza above to Alif
        'إ': 'ا',  # Alif with hamza below to Alif
        'آ': 'ا',  # Alif madda to Alif
        'ٱ': 'ا',  # Alif wasl to Alif
        'ؤ': 'و',  # Waw with hamza above to Waw
        'ئ': 'ي',  # Ya with hamza above to Ya
        'ة': 'ه',  # Tah marbuta to Ha
        'ى': 'ي',  # Alif maksura to Ya
    }
    
    # Create a translation table
    trans_table = str.maketrans(complex_to_simple)
    
    # Translate the text
    simplified_text = text.translate(trans_table)
    
    # Remove diacritics
    simplified_text = re.sub(r'[\u064B-\u065F\u0670]', '', simplified_text)
    
    return simplified_text

# Example usage
text = 'ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ'
simplified = simplify_arabic_text(text)
print("Original:", text)
print("Simplified:", simplified)