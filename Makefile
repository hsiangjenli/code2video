RAW_CODE := demo.py

GENERATED_CODE_FOLDER := generated_code
GENERATED_IMAGE_FOLDER := generated_image
GENERATED_FRAMES_FOLDER := generated_frame

c2p:
	@echo "Generating partial code..."
	python code2image/code2partial.py --code_path demo.py --output_dir $(GENERATED_CODE_FOLDER)

p2i:
	@echo "Generating image..."
	python code2image/partial2image.py --input_dir $(GENERATED_CODE_FOLDER) --output_dir $(GENERATED_IMAGE_FOLDER)

i2f:
	@echo "Generating frames..."
	python code2image/image2frame.py --input_dir $(GENERATED_IMAGE_FOLDER) --output_dir $(GENERATED_FRAMES_FOLDER)

i2v:
	@echo "Generating video..."
	ffmpeg -loop 1 -t 1 -i cover.png -framerate 10 -i $(GENERATED_FRAMES_FOLDER)/%d.png -filter_complex "[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[v0];[1:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[v1];[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" -c:v libx264 -r 10 output.mp4

cover:
	@echo "Generating cover image..."
	python code2image/cover.py --input_path $(GENERATED_FRAMES_FOLDER)/48.png --output_path cover.png --title "This is a title\nthat spans multiple lines"

all: c2p p2i i2f cover i2v

clean:
	rm -rf $(GENERATED_CODE_FOLDER) $(GENERATED_IMAGE_FOLDER) $(GENERATED_FRAMES_FOLDER) output.mp4
	rm code_*.png