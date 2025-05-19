import google.generativeai as genai
import PIL.Image
import os
import sys
from dotenv import load_dotenv
load_dotenv()
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable.")
    print("Get your key from: https://aistudio.google.com/app/apikey")
    sys.exit(1)

MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

def get_image_description(image_path, prompt="""
You are an image quality analyst for YouTube video production, specializing in horror content.

Evaluate the given image and return your assessment in the following JSON format:

{
  "image_quality": "good" or "bad",
  "image_relevance": 1-10 (how well it fits a horror theme and the provided caption),
  "image_description": "A concise two-line description of what is visually present in the image."
}

Assessment Criteria:

- Watermarks and Overlays: Reject the image if there are obvious or multiple watermarks. A small, subtle watermark may be acceptable if the image is otherwise excellent.
- Relevance to Horror: Evaluate if the image evokes fear, suspense, or unease and fits horror themes.
- Technical Quality: Assess clarity, composition, and the absence of technical flaws.
- Context and Caption: Consider the caption when rating the relevance and describing the image.

Return only the JSON result as your final output.
"""):
    print(f"Processing image: {image_path}")

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return None

    try:
        img = PIL.Image.open(image_path)
        print("Image loaded successfully.")
    except Exception as e:
        print(f"Error opening or reading image file: {e}")
        return None

    prompt_parts = [
        prompt,
        img,
    ]
    try:
        print("Sending request to Gemini API...")
        response = model.generate_content(prompt_parts)
        print("Response received.")
        return response.text
    except genai.types.generation_types.BlockedPromptException as e:
        print(f"Error: The prompt was blocked. Reason: {e}")
        return "Error: Prompt blocked by safety settings."
    except Exception as e:
        print(f"An error occurred during API communication: {e}")
        return None

# --- Main execution ---
if __name__ == "__main__":
    image_file_path = input("Enter the path to your local image file: ")
    description = get_image_description(image_file_path)
    if description:
        print("\n--- Image Description ---")
        print(description)
        print("-------------------------\n")
    else:
        print("\nFailed to get image description.")