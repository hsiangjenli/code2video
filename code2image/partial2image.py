import os
import argparse
from concurrent.futures import ThreadPoolExecutor

# Setup argument parsing
args = argparse.ArgumentParser()
args.add_argument("--input_dir", default="partial_code", help="Directory containing the partial code files")
args.add_argument("--output_dir", default="raw_images", help="Directory to save the generated images")

# Function to generate image from a code file
def generate_image(file, input_dir, output_dir):
    file_path = os.path.join(input_dir, file)
    output_image_path = os.path.join(output_dir, file.replace(".py", ".png"))
    command = f"carbon-now {file_path} --width 1080 --line-numbers -t '{output_image_path}' --headless --no-open"
    os.system(command)

# Function to move generated images to the output directory
def move_images(output_dir):
    for file in os.listdir("."):
        if file.startswith("code_") and file.endswith(".png"):
            os.rename(file, os.path.join(output_dir, file))

# Main function to generate images
def generate_images(partial_code_dir="partial_code", raw_image_dir="raw_images", max_workers=8):
    os.makedirs(raw_image_dir, exist_ok=True)
    files = sorted(os.listdir(partial_code_dir))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file in files:
            executor.submit(generate_image, file, partial_code_dir, raw_image_dir)

    move_images(raw_image_dir)

if __name__ == "__main__":
    # Parse the arguments
    args = args.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate images from the code files
    generate_images(partial_code_dir=args.input_dir, raw_image_dir=args.output_dir)