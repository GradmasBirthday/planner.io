# Voice Input with Whisper Setup Guide

This guide will help you set up the `voice_input_whisper.py` script for voice recording and transcription using OpenAI Whisper.

## Prerequisites

- Python 3.8 or higher
- Microphone access
- FFmpeg installed on your system
- Internet connection (for downloading Whisper models)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Additional System Requirements

#### Windows
- FFmpeg: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Add FFmpeg to your system PATH

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## Step 2: Test Your Microphone

Before running the script, ensure your microphone is working:

```bash
python -c "import sounddevice as sd; print('Available devices:'); print(sd.query_devices())"
```

## Step 3: Run the Voice Input Script

### Basic Usage
```bash
cd src/planner
python voice_input_whisper.py
```

### Advanced Usage with Options
```bash
# Record for 15 seconds with a larger model
python voice_input_whisper.py --duration 15 --model medium

# Record for 5 seconds with tiny model (faster)
python voice_input_whisper.py --duration 5 --model tiny

# Keep temporary audio files for debugging
python voice_input_whisper.py --no-cleanup

# Use different sample rate
python voice_input_whisper.py --sample-rate 16000
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--duration` | `-d` | Recording duration in seconds | 10 |
| `--model` | `-m` | Whisper model size | base |
| `--sample-rate` | `-sr` | Audio sample rate in Hz | 44100 |
| `--no-cleanup` | | Keep temporary audio files | False |
| `--no-progress` | | Hide recording progress | False |

## Whisper Models

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | 39 MB | Fastest | Good | Quick testing |
| base | 74 MB | Fast | Better | General use |
| small | 244 MB | Medium | Better | Better accuracy |
| medium | 769 MB | Slow | Best | High accuracy |
| large | 1550 MB | Slowest | Best | Maximum accuracy |

## Expected Output

```
🎤 Voice Input with Whisper Transcription
==================================================
📋 Settings:
   • Duration: 10 seconds
   • Model: base
   • Sample Rate: 44100 Hz
   • Cleanup: Yes
==================================================
🎤 Recording audio for 10 seconds...
   Speak now!
   Recording... 1/10 seconds
   Recording... 2/10 seconds
   ...
💾 Audio saved to: /tmp/voice_input_20241201_143022.wav
🔄 Loading Whisper model: base
✅ Whisper model loaded successfully
🔄 Transcribing audio with Whisper...
✅ Transcription completed
🗑️  Cleaned up temporary file: /tmp/voice_input_20241201_143022.wav

==================================================
📝 TRANSCRIPTION RESULT
==================================================
Hello, this is a test of the voice input system.
==================================================
```

## Features

### 🎤 Audio Recording
- Records audio from default microphone
- Configurable duration (1-60+ seconds)
- Progress indicator during recording
- High-quality audio capture

### 🔄 Transcription
- Uses OpenAI Whisper for accurate transcription
- Multiple model sizes for speed/accuracy trade-offs
- Automatic language detection
- Handles various accents and speech patterns

### 💾 File Management
- Saves audio as temporary WAV files
- Automatic cleanup after transcription
- Timestamped filenames for debugging
- Option to keep files for analysis

### ⚙️ Customization
- Adjustable sample rates
- Multiple Whisper model options
- Configurable recording duration
- Progress display options

## Troubleshooting

### Microphone Issues
- **No audio detected**: Check microphone permissions and default device
- **Poor quality**: Try different sample rates (16000, 22050, 44100)
- **Device not found**: Run `python -c "import sounddevice as sd; print(sd.query_devices())"`

### Whisper Issues
- **Model download fails**: Check internet connection and try again
- **Slow transcription**: Use smaller models (tiny, base) for faster results
- **Poor accuracy**: Try larger models (medium, large) for better results

### FFmpeg Issues
- **FFmpeg not found**: Install FFmpeg and add to system PATH
- **Audio format errors**: Ensure FFmpeg supports your audio format

### Performance Issues
- **High CPU usage**: Use smaller Whisper models
- **Memory issues**: Close other applications or use tiny model
- **Slow startup**: Models are downloaded on first use

## File Structure

```
Planner/
├── requirements.txt                    ← Python dependencies
└── src/
    └── planner/
        ├── voice_input_whisper.py     ← Main voice input script
        └── __init__.py                 ← Package init
```

## Integration with Other Scripts

The `VoiceInputWhisper` class can be imported and used in other scripts:

```python
from voice_input_whisper import VoiceInputWhisper

# Initialize
voice_input = VoiceInputWhisper(model_name="base")

# Record and transcribe
text = voice_input.record_and_transcribe(duration=10)

# Use the transcribed text
print(f"You said: {text}")
```

## Security Notes

- Audio files are temporarily stored and automatically cleaned up
- No audio data is sent to external services (Whisper runs locally)
- Microphone access is required for recording
- Temporary files may contain sensitive audio data

## Performance Tips

- Use `tiny` or `base` models for faster processing
- Lower sample rates (16000 Hz) for smaller file sizes
- Close other applications to free up system resources
- Use SSD storage for faster model loading 