import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
from time import sleep
import os

# --- Minimal safety/diagnostics additions ---
# Ensure "Data" folder exists for storing images
os.makedirs(r"Data", exist_ok=True)

# Path to the trigger file that controls when image generation should start
TRIGGER_FILE = r"C:\Users\saraw\OneDrive\Desktop\FRIDAY\Frontend\Files\ImageGeneration.data"


# Function to open and display generated images
def open_images(prompt):
    folder_path = r"Data"
    # Replace spaces in prompt with underscores for safe filenames
    prompt = prompt.replace(" ", "_")

    # Expected filenames of generated images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    # Try opening each image file and displaying it
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image : {image_path}")
            img.show()  # Open the image in default viewer
        except IOError:
            print(f"Unable to open {image_path}")


# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env','HuggingFaceAPIKey')}"}


# Asynchronous function to send prompt to Hugging Face API
async def query(payload):
    try:
        # Run the HTTP POST request in a background thread (non-blocking)
        response = await asyncio.to_thread(
            requests.post, API_URL, headers=headers, json=payload, timeout=120
        )
    except Exception as e:
        print("HTTP request failed:", e)
        raise

    # Log response details for debugging
    print("HF response status:", response.status_code, "content-type:", response.headers.get("Content-Type"))
    ctype = response.headers.get("Content-Type", "")
    if "application/json" in ctype or "text/" in ctype:
        print("HF response text (first 500 chars):", response.text[:500])
    print("response content length:", len(response.content))

    # Return raw bytes (should be image data)
    return response.content


# Asynchronous function to generate multiple images
async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, ultra detailed, 4k resolution, sharp focus, realistic lighting"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_byte in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}_{i + 1}.jpg", "wb") as f:
            f.write(image_byte)


    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks, return_exceptions=True)

    # Save each generated image to disk
    safe_prompt = prompt.replace(" ", "_")
    for i, image_byte in enumerate(image_bytes_list, start=1):
        if isinstance(image_byte, Exception):  # Handle failures
            print(f"[{i}] generation failed:", image_byte)
            continue
        with open(fr"Data\{safe_prompt}{i + 1}.jpg", "wb") as f:
            f.write(image_byte)
        print(f"Saved Data\\{safe_prompt}{i + 1}.jpg")


# Wrapper function to run async image generation and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


# --- MAIN LOOP ---
# Continuously checks the trigger file for instructions
while True:
    try:
        # Read contents of trigger file
        with open(TRIGGER_FILE, "r", encoding="utf-8") as f:
            Data: str = f.read().strip()
            print("Trigger file content:", repr(Data))

        # File format: "prompt,Status"
        prompt, Status = Data.split(",", 1)
        prompt = prompt.strip()
        Status = Status.strip()

        # If Status is "True", start image generation
        if Status == "True":
            print("Generating Images.....")
            GenerateImages(prompt=prompt)

            # Reset trigger file to prevent infinite loop
            with open(TRIGGER_FILE, "w", encoding="utf-8") as f:
                f.write("False,False")
            break  # Exit after one round of generation
        else:
            # If Status is not True, wait and check again
            sleep(1)

    except Exception as e:
        # Catch and log errors, then retry
        print("Main loop error:", e)
        sleep(1)
