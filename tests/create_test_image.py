from PIL import Image
import os

def create_test_image():
    # Create directory if it doesn't exist
    os.makedirs('tests/data', exist_ok=True)
    
    # Create a white image
    img = Image.new('RGB', (100, 100), color='white')
    
    # Save the image
    img.save('tests/data/test.png')

if __name__ == '__main__':
    create_test_image() 