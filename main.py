import yt_dlp
import re
import os
from pysndfx import AudioEffectsChain
from pyrogram import Client, filters

# Initialize the Pyrogram Client
api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'
app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Create a yt-dlp instance
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'outtmpl': '%(id)s.%(ext)s',  # Save the file using the video ID as the filename
}

# Function to check if a message contains a valid audio URL
def is_valid_audio_url(text):
    url_pattern = re.compile(r'https?://.+')
    return bool(url_pattern.match(text))

# Function to extract video ID or audio ID from the URL
def extract_id_from_url(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('id')

# Function to get the title and duration of the music
def get_music_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 'Unknown Duration')
        return title, duration

# Convert duration from seconds to minutes:seconds format
def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"

# Apply effects to WAV
def apply_effects(input_path, output_path, speed=1.0):
    fx = (
        AudioEffectsChain()
        .speed(speed)  # Adjust the speed based on the user's command
        .reverb()
    )
    fx(input_path, output_path)

# Dictionary to store user-specific speed settings
user_speed_settings = {}

@app.on_message(filters.command('s'))
def set_speed(client, message):
    chat_id = message.chat.id
    try:
        speed = float(message.text.split(' ')[1])
        user_speed_settings[chat_id] = speed
        client.delete_messages(chat_id, message.message_id)
        client.send_message(chat_id, f"Speed set to: {speed}")
    except (IndexError, ValueError):
        client.send_message(chat_id, "Invalid speed format. Use /s followed by a number e.g., /s 0.8")

@app.on_message(filters.command('help'))
def show_supported_links(client, message):
    chat_id = message.chat.id
    client.delete_messages(chat_id, message.message_id)
    supported_links_message = (
        "- Here are supported sites\n- Commands:\n/s - to set speed e.g : /s 0.8")
    client.send_message(chat_id, supported_links_message)

@app.on_message(filters.command('start'))
def show_supported_links(client, message):
    chat_id = message.chat.id
    client.delete_messages(chat_id, message.message_id)
    supported_links_message = ("Welcome to the bot\n- Check /help for more information")
    client.send_message(chat_id, supported_links_message)

@app.on_message(filters.text & ~filters.command)
def process_audio_link(client, message):
    chat_id = message.chat.id
    audio_url = message.text

    # Delete the user's message containing the URL
    client.delete_messages(chat_id, message.message_id)

    # Send a "processing" message
    processing_message = client.send_message(chat_id, "Processing...")

    audio_id = extract_id_from_url(audio_url)
    if audio_id:
        ydl_opts['outtmpl'] = f"original/{audio_id}.%(ext)s"
        original_path = f"original/{audio_id}.wav"
        slowed_reverb_path = f"slowed_reverb/{audio_id}_slowed_reverb.wav"

        # Get the user-specific speed setting (default to 1.0 if not set)
        speed = user_speed_settings.get(chat_id, 1.0)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([audio_url])

                # Check the size of the downloaded audio
                audio_size = os.path.getsize(original_path) / (1024 * 1024)  # Convert to MB
                if audio_size > 500:
                    # Delete the "processing" message
                    client.delete_messages(chat_id, processing_message.message_id)
                    # Delete the downloaded audio files
                    os.remove(original_path)
                    os.remove(slowed_reverb_path)
                    client.send_message(chat_id, "The music size is too large (over 500MB).")
                else:
                    # Apply effects to the downloaded audio with the specified speed
                    apply_effects(original_path, slowed_reverb_path, speed)

                    # Get the title and duration of the music
                    title, duration = get_music_info(audio_url)

                    # Format the duration in minutes:seconds
                    formatted_duration = format_duration(duration)

                    # Send the processed audio back to the user as a file with the title as the filename
                    with open(slowed_reverb_path, 'rb') as audio_file:
                        client.send_audio(chat_id, audio_file, caption=f"Title : {title}\nduration: {formatted_duration}")

                    # Clean up the files
                    os.remove(original_path)
                    os.remove(slowed_reverb_path)

                    # Delete the "processing" message
                    client.delete_messages(chat_id, processing_message.message_id)
            except Exception as e:
                error_message = f"Error: {e}"
                # Delete the "processing" message and send the error message
                client.delete_messages(chat_id, processing_message.message_id)
                client.send_message(chat_id, error_message)
    else:
        # Delete the "processing" message and the unsupported link message
        client.delete_messages(chat_id, processing_message.message_id)
        # Send the unsupported link message with clickable "supported links"
        unsupported_message = (
            "Unsupported link.. please check supported links"
        )
        client.send_message(chat_id, unsupported_message)

if __name__ == "__main__":
    app.run()
    
