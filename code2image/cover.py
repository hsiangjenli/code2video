from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse

args = argparse.ArgumentParser()

args.add_argument("--input_path", default="demo.png", help="Path to the image")
args.add_argument("--output_path", default="output.png", help="Path to save the output image")

args.add_argument("--title", default="Demo Image", help="Title to add to the image")

args.add_argument("--radius", default=20, help="Radius of the blur effect")

def read_image(image_path: str):
    """
    Read the image from the specified path.

    Args:
        image_path (str): The path to the image.

    Returns:
        Image: The image object.
    """
    return Image.open(image_path)

def make_image_blurry(image: Image, radius: int = 5):
    """
    Make the image blurry.

    Args:
        image (Image): The image object.
        radius (int): The radius of the blur effect.
    """
    return image.filter(ImageFilter.GaussianBlur(radius=radius))

def add_title_to_image(image: Image, title: str):
    """
    Add a title to the image.

    Args:
        image (Image): The image object.
        title (str): The title to add.
    """
    draw = ImageDraw.Draw(image)
    
    # Initialize font and start with a small font size
    font_size = 1
    font = ImageFont.truetype("Verdana Bold.ttf", font_size)
    
    # Split title into multiple lines based on available width
    max_width = image.size[0] * 0.8  # Use 80% of image width for text
    lines = title.split("\\n")

    # Adjust font size baed on the maximum width of the text block
    # return the maximum line in the list
    max_line = max(lines, key=lambda line: font.getbbox(line)[2])
    while font.getbbox(max_line)[2] < max_width and font_size < image.size[1] // len(lines):
        font_size += 1
        font = ImageFont.truetype("Verdana Bold.ttf", font_size)
    
    # Calculate total height of the text block
    line_height = font.getbbox("A")[3]  # Use "A" to calculate line height
    total_height = line_height * len(lines)
    
    # Start drawing the text block vertically centered
    y = (image.size[1] - total_height) // 2
    for line in lines:
        line_width = font.getbbox(line)[2]
        x = (image.size[0] - line_width) // 2  # Center each line horizontally
        draw.text((x, y), line, font=font, fill="white")
        y += line_height

    return image
    
def save_image(image: Image, output_path: str):
    """
    Save the image to the specified path.

    Args:
        image (Image): The image object.
        output_path (str): The path to save the image.
    """
    image.save(output_path)


if __name__ == "__main__":

    args = args.parse_args()

    # Read the image
    image = read_image(args.input_path)

    # Make the image blurry
    image = make_image_blurry(image, radius=args.radius)

    # Add a title to the image
    image = add_title_to_image(image, args.title)

    # Save the image
    save_image(image, args.output_path)