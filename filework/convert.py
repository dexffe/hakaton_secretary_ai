from pydub import AudioSegment


class Converter:
    def __init__(self):
        pass

    def convert_mp3_to_wav(self, source_path, target_path):
        audio = AudioSegment.from_mp3(source_path)
        audio.export(target_path, format="wav")

    def convert_mp4a_to_wav(self, source_path, target_path):
        audio = AudioSegment.from_file(source_path, format="mp4a")
        audio.export(target_path, format="wav")

    def convert_ogg_to_wav(self, source_path, target_path):
        audio = AudioSegment.from_ogg(source_path)
        audio.export(target_path, format="wav")

    def convert(self, source_path, target_path):
        file_extension = source_path.split('.')[-1].lower()

        if file_extension == 'mp3':
            self.convert_mp3_to_wav(source_path, target_path)
        elif file_extension in ['m4a', 'mp4a']:
            self.convert_mp4a_to_wav(source_path, target_path)
        elif file_extension == 'ogg':
            self.convert_ogg_to_wav(source_path, target_path)
        else:
            raise ValueError("Unsupported file format. Please use MP3, MP4A, or OGG.")
