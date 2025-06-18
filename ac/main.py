import os
from pydub import AudioSegment
import configparser

def read_settings():
    config = configparser.ConfigParser()
    ini_path = os.path.join(os.path.dirname(__file__), 'settings.ini')
    config.read(ini_path)

    try:
        source = config.get('Paths', 'source')
        destination = config.get('Paths', 'destination')
        return source, destination
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"❌ Error in settings.ini: {e}")
        exit(1)

def check_destination_folder(destination_folder):
    if not os.path.exists(destination_folder):
        print(f"⚠️ Destination folder '{destination_folder}' does not exist. Creating ...")
        os.makedirs(destination_folder)
    else:
        print(f"✅ Destination folder '{destination_folder}' is valid.")

def convert_flac_to_mp3(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".flac"):
            flac_path = os.path.join(source_folder, filename)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_path = os.path.join(destination_folder, mp3_filename)

            print(f"Converting: {flac_path} -> {mp3_path}")
            try:
                audio = AudioSegment.from_file(flac_path, format="flac")
                audio.export(mp3_path, format="mp3", bitrate="320k")
                print("✅ Conversion successful.")
            except Exception as e:
                print(f"❌ Error converting {filename}: {e}")

if __name__ == "__main__":
    source, destination = read_settings()

    check_destination_folder(destination)

    convert_flac_to_mp3(source, destination)
