import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import os
import warnings
warnings.filterwarnings("ignore")


def record_audio(duration=5, filename="input.wav", fs=44100):
    print(f"🎙️ Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    print(f"✅ Saved recording to {filename}")

def transcribe_with_whisper(audio_path):
    model = whisper.load_model("base")
    print("🧠 Transcribing...")
    result = model.transcribe(audio_path)
    print(f"📝 Transcription: {result['text']}")
    return result["text"]

if __name__ == "__main__":
    record_audio()
    transcribe_with_whisper("input.wav")
