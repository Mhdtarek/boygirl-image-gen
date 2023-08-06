import os
import random
import cv2
import moviepy.editor as mp
import json

def get_random_image(image_dir):
    images = os.listdir(image_dir)
    return os.path.join(image_dir, random.choice(images))

def wrap_text(text, max_line_length):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return '\n'.join(lines)

def get_random_music(music_dir):
    music_files = [file for file in os.listdir(music_dir) if file.endswith('.mp3')]
    return os.path.join(music_dir, random.choice(music_files))

def create_video(image_dir, music_dir, output_path, type_text, fact_text, max_duration=30):
    image_file = get_random_image(image_dir)
    image = cv2.imread(image_file)

    # Downscale the image to speed up processing
    image = cv2.resize(image, (1080, 1920))

    height, width, _ = image.shape

    # Set text based on the input parameters
    text = fact_text
    text = wrap_text(text, 20)  # Maximum 20 characters per line
    text_size = 1.5  # Decrease the font size
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Calculate text size and position for proper centering
    text_lines = text.split('\n')
    total_text_height = sum([cv2.getTextSize(line, font, text_size, 2)[0][1] for line in text_lines])
    y = (height + total_text_height) // 2 - total_text_height // 2

    # Draw black box behind the type text (e.g., "Girls Facts" or "Boys Facts")
    type_text_size = 1.2
    type_text_width, type_text_height = cv2.getTextSize(type_text, font, type_text_size, 2)[0]
    type_text_x = (width - type_text_width) // 2
    type_text_y = y - total_text_height - type_text_height - 10  # 10 is the spacing between type text and the main text
    type_text_box_x1 = type_text_x - 10
    type_text_box_y1 = type_text_y - 10
    type_text_box_x2 = type_text_x + type_text_width + 10
    type_text_box_y2 = type_text_y + type_text_height + 10
    cv2.rectangle(image, (type_text_box_x1, type_text_box_y1), (type_text_box_x2, type_text_box_y2), (0, 0, 0), -1)
    cv2.putText(image, type_text, (type_text_x, type_text_y + type_text_height), font, type_text_size, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw black box behind the main text
    main_text_x = (width - max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in text_lines])) // 2
    main_text_y = y
    main_text_box_x1 = main_text_x - 10
    main_text_box_y1 = main_text_y - 45
    main_text_box_x2 = main_text_x + max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in text_lines]) + 10
    main_text_box_y2 = main_text_y + total_text_height + 25
    cv2.rectangle(image, (main_text_box_x1, main_text_box_y1), (main_text_box_x2, main_text_box_y2), (0, 0, 0), -1)

    # Draw the main text on the image
    for line in text_lines:
        text_width, text_height = cv2.getTextSize(line, font, text_size, 2)[0]
        x = (width - text_width) // 2
        cv2.putText(image, line, (x, y), font, text_size, (255, 255, 255), 2, cv2.LINE_AA)
        y += text_height + 10  # Adjust the multiplier to control line spacing

    cv2.imwrite("temp_image.jpg", image)

    # Set video duration based on audio duration or a specified maximum duration (30 seconds)
    audio_path = get_random_music(music_dir)
    audio = mp.AudioFileClip(audio_path)
    max_duration = min(max_duration, 30)  # Limit video duration to 30 seconds

    # Create a subclip of the audio to match the video duration
    audio = audio.subclip(0, max_duration)

    clip = mp.VideoFileClip("temp_image.jpg")
    clip = clip.set_duration(max_duration)

    video = clip.set_audio(audio)
    output_filename = f"{fact_text.replace(' ', ' ').lower()}.mp4"
    output_path = os.path.join("output_videos", output_filename)
    video.write_videofile(output_path, codec='libx264', fps=15, audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

    # Remove temporary files
    os.remove("temp_image.jpg")
    if os.path.exists("temp_audio.m4a"):
        os.remove("temp_audio.m4a")

if __name__ == "__main__":
    image_directory = "./images"  # Assuming "images" is in the same directory as the script.
    music_directory = "./music"  # Assuming "music" is in the same directory as the script.
    
    # Create the "output_videos" directory if it doesn't exist
    output_directory = "output_videos"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read data from the JSON file
    with open("data.json", "r") as file:
        data = json.load(file)

    # Process each entry in the JSON data and create videos accordingly
    for entry in data:
        type_text = "Girls Facts" if entry["type"] == "girl" else "Boys Facts"
        fact_text = entry["fact"]
        create_video(image_directory, music_directory, output_directory, type_text, fact_text)

        # Remove the processed entry from the data array
        data.remove(entry)
    
    # Update the JSON file with the remaining data (without the processed entries)
    with open("data.json", "w") as file:
        json.dump(data, file)
