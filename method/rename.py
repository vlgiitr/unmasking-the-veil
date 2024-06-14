import os
import argparse

# Function to rename images based on prompts
def rename_images(prompt_file_path, images_folder_path):
    with open(prompt_file_path, 'r') as prompt_file:
        prompts = prompt_file.readlines()

    image_files = os.listdir(images_folder_path)
    image_files.sort()  # Sort to match with the order of prompts

    if len(prompts) != len(image_files):
        print("Number of prompts and images don't match.")
        return

    for i, prompt in enumerate(prompts):
        prompt = prompt.strip()
        old_name = os.path.join(images_folder_path, image_files[i])
        new_name = os.path.join(images_folder_path, f"{prompt}.jpg")  # Assuming images are in jpg format
        os.rename(old_name, new_name)
        print(f"Renamed '{old_name}' to '{new_name}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename images based on prompts.")
    parser.add_argument('prompt_file_path', type=str, help='Path to the prompt file')
    parser.add_argument('images_folder_path', type=str, help='Path to the folder containing images')

    args = parser.parse_args()

    rename_images(args.prompt_file_path, args.images_folder_path)
