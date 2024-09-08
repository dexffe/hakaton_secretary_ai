import vosk
import sys
import soundfile as sf
def Get_Transcription(audio_path,model_path="..\models\vosk-model-ru-0.10"):
    wf = sf.SoundFile(audio_path)
    samplerate = wf.samplerate
    audio = wf.read(dtype='int16')
    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, samplerate)
    rec.AcceptWaveform(audio.tobytes())
    return rec.Result()['text']