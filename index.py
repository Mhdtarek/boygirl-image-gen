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

def create_video(image_dir, music_dir, output_path, type_text, first_part_text, second_part_text, max_duration=30):
    image_file = get_random_image(image_dir)
    image = cv2.imread(image_file)
    image = cv2.resize(image, (1080, 1920))
    height, width, _ = image.shape

    # Set text based on the input parameters
    text_size = 1.5  # Decrease the font size
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Calculate text size and position for proper centering
    first_part_lines = wrap_text(first_part_text, 20).split('\n')
    second_part_lines = wrap_text(second_part_text, 20).split('\n')
    total_first_part_height = sum([cv2.getTextSize(line, font, text_size, 2)[0][1] for line in first_part_lines])
    total_second_part_height = sum([cv2.getTextSize(line, font, text_size, 2)[0][1] for line in second_part_lines])
    total_text_height = total_first_part_height + total_second_part_height
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

    # Draw black box behind the first part text
    first_part_x = (width - max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in first_part_lines])) // 2
    first_part_y = y
    first_part_box_x1 = first_part_x - 10
    first_part_box_y1 = first_part_y - 45
    first_part_box_x2 = first_part_x + max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in first_part_lines]) + 10
    first_part_box_y2 = first_part_y + total_first_part_height + 25
    cv2.rectangle(image, (first_part_box_x1, first_part_box_y1), (first_part_box_x2, first_part_box_y2), (0, 0, 0), -1)

    # Draw the first part text on the image
    for line in first_part_lines:
        text_width, text_height = cv2.getTextSize(line, font, text_size, 2)[0]
        x = (width - text_width) // 2
        cv2.putText(image, line, (x, y), font, text_size, (255, 255, 255), 2, cv2.LINE_AA)
        y += text_height + 10  # Adjust the multiplier to control line spacing

    cv2.imwrite("temp_image_part1.jpg", image)

    # Create a subclip of the audio to match the first part video duration (15 seconds)
    audio_path = get_random_music(music_dir)
    audio = mp.AudioFileClip(audio_path)
    max_duration = min(max_duration, 30)  # Limit video duration to 30 seconds
    audio_part1 = audio.subclip(0, max_duration // 2)

    clip_part1 = mp.VideoFileClip("temp_image_part1.jpg").set_duration(15)  # Limit first part duration to 15 seconds
    clip_part1 = clip_part1.set_audio(audio_part1)
    clip_part1 = clip_part1.crossfadein(0.5)  # Add a crossfade at the beginning of the first part

    # Draw black box behind the second part text
    second_part_x = (width - max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in second_part_lines])) // 2
    second_part_y = y
    second_part_box_x1 = second_part_x - 10
    second_part_box_y1 = second_part_y - 40
    second_part_box_x2 = second_part_x + max([cv2.getTextSize(line, font, text_size, 2)[0][0] for line in second_part_lines]) + 10
    second_part_box_y2 = second_part_y + total_second_part_height + 25
    cv2.rectangle(image, (second_part_box_x1, second_part_box_y1), (second_part_box_x2, second_part_box_y2), (0, 0, 0), -1)

    # Draw the second part text on the image
    for line in second_part_lines:
        text_width, text_height = cv2.getTextSize(line, font, text_size, 2)[0]
        x = (width - text_width) // 2
        cv2.putText(image, line, (x, y), font, text_size, (255, 255, 255), 2, cv2.LINE_AA)
        y += text_height + 10  # Adjust the multiplier to control line spacing

    cv2.imwrite("temp_image_part2.jpg", image)

    # Create a subclip of the audio to match the second part video duration (15 seconds)
    audio_part2 = audio.subclip(max_duration // 2, max_duration)

    clip_part2 = mp.VideoFileClip("temp_image_part2.jpg").set_duration(max_duration - 15)  # Remaining duration after the first part
    clip_part2 = clip_part2.set_audio(audio_part2)
    clip_part2 = clip_part2.crossfadein(0.5)  # Add a crossfade at the beginning of the second part


    final_clip = mp.concatenate_videoclips([clip_part1, clip_part2])

    output_filename = f"{first_part_text.replace('.', '')} #shorts #phycology #facts.mp4"
    output_path = os.path.join("output_videos", output_filename)
    final_clip.write_videofile(output_path, codec='libx264', fps=15, audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

    # Remove temporary files
    os.remove("temp_image_part1.jpg")
    os.remove("temp_image_part2.jpg")
    if os.path.exists("temp_audio.m4a"):
        os.remove("temp_audio.m4a")

if __name__ == "__main__":
    image_directory = "./images"  # Assuming "images" is in the same directory as the script.
    music_directory = "./music"  # Assuming "music" is in the same directory as the script.

    output_directory = "output_videos"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open("data.json", "r") as file:
        data = json.load(file)

    # Initialize the video counter
    video_counter = 1

    for entry in data:
        type_text = entry["type"].capitalize() + " Facts"
        first_part_text = entry["firstpart"]
        second_part_text = entry["secondpart"]

        create_video(image_directory, music_directory, output_directory, type_text, first_part_text, second_part_text)

        # Print the video number
        print(f"Video {video_counter} created.")
        video_counter += 1

    with open("data.json", "w") as file:
        json.dump(data, file)
