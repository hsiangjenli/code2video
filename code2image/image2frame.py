import os
import argparse
from PIL import Image

args = argparse.ArgumentParser()

args.add_argument("--input_dir", default="raw_images", help="Directory containing the raw images")
args.add_argument("--output_dir", default="frames", help="Directory to save the frames")

args.add_argument("--background_color", default="#272822", help="Background color for the frames")
args.add_argument("--frame_ratio", default="(9, 16)", help="Aspect ratio of the frames")

def reconstruct_image_to_frame(image_dir: str, output_dir: str, background_color: str, frame_ratio: tuple):
    """
    Reconstruct the images to frames.

    Args:
        image_dir (str): The directory containing the images.
        output_dir (str): The directory to save the frames.
        background_color (str): The background color for the frames.
        frame_ratio (tuple): The aspect ratio of the frames.
    """
    os.makedirs(output_dir, exist_ok=True)

    files = sorted(os.listdir(image_dir))

    # get the image width
    first_file = files[0]
    first_image_path = os.path.join(image_dir, first_file)
    first_image = Image.open(first_image_path)
    first_image_width = first_image.size[0]

    # generate a new image with the specified aspect ratio
    frame_ratio = eval(frame_ratio)
    image_height = first_image_width * frame_ratio[1] / frame_ratio[0]
    image_size = (first_image_width, int(image_height))

    new_image = Image.new("RGB", image_size, background_color)

    # save the new image
    for i, file in enumerate(files):
        file_path = os.path.join(image_dir, file)
        image = Image.open(file_path)
        new_image.paste(image, (0, 0))
        new_image.save(os.path.join(output_dir, f"{i}.png"))

if __name__ == "__main__":
    args = args.parse_args()
    reconstruct_image_to_frame(image_dir=args.input_dir, output_dir=args.output_dir, background_color=args.background_color, frame_ratio=args.frame_ratio)