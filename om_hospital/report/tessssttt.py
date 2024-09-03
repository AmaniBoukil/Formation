import barcode
from barcode.writer import ImageWriter

# Generate a barcode
def generate_barcode(data):
    ean = barcode.get('ean13', data, writer=ImageWriter())
    filename = ean.save('barcode')
    return filename

# Example usage
if __name__ == "__main__":
    barcode_data = "123456789012"  # This should be a 12-digit number for EAN-13
    barcode_filename = generate_barcode(barcode_data)
    print(f"Barcode saved as: {barcode_filename}")



