import os
import argparse

def read_prompts(prompt_file_path):
    with open(prompt_file_path, 'r') as prompt_file:
        prompts = prompt_file.readlines()
    return [prompt.strip() for prompt in prompts]

def create_prompts_folder(prompts_folder):
    if not os.path.exists(prompts_folder):
        os.makedirs(prompts_folder)

def create_prompt_files(prompts, prompts_folder):
    for i, prompt in enumerate(prompts):
        file_name = os.path.join(prompts_folder, f"{prompt}.txt")
        with open(file_name, 'w') as f:
            f.write(prompt)
        print(f"Created file '{file_name}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read prompts from a file and create individual prompt files.")
    parser.add_argument('prompt_file_path', type=str, help='Path to the prompt file')
    parser.add_argument('prompts_folder', type=str, help='Path to the folder where prompt files will be created')

    args = parser.parse_args()

    prompts = read_prompts(args.prompt_file_path)
    create_prompts_folder(args.prompts_folder)
    create_prompt_files(prompts, args.prompts_folder)
