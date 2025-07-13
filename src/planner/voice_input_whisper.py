import sounddevice as sd
import soundfile as sf
import whisper
import tempfile
import os
import numpy as np
from datetime import datetime
import argparse

class VoiceInputWhisper:
    def __init__(self, model_name="base", sample_rate=44100, channels=1):
        """
        Initialize the voice input and transcription system.
        
        Args:
            model_name (str): Whisper model to use ('tiny', 'base', 'small', 'medium', 'large')
            sample_rate (int): Audio sample rate in Hz
            channels (int): Number of audio channels (1 for mono, 2 for stereo)
        """
        self.model_name = model_name
        self.sample_rate = sample_rate
        self.channels = channels
        self.model = None
        self.temp_file = None
        
    def load_whisper_model(self):
        """Load the Whisper model (lazy loading to avoid loading until needed)"""
        if self.model is None:
            print(f"🔄 Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            print(f"✅ Whisper model loaded successfully")
    
    def record_audio(self, duration=10, show_progress=True):
        """
        Record audio from the microphone.
        
        Args:
            duration (int): Recording duration in seconds
            show_progress (bool): Whether to show recording progress
            
        Returns:
            numpy.ndarray: Recorded audio data
        """
        print(f"🎤 Recording audio for {duration} seconds...")
        print("   Speak now!")
        
        if show_progress:
            # Record with progress indicator
            audio_data = []
            chunk_duration = 1.0  # Update progress every second
            chunks = int(duration / chunk_duration)
            
            for i in range(chunks):
                chunk = sd.rec(int(chunk_duration * self.sample_rate), 
                              samplerate=self.sample_rate, 
                              channels=self.channels, 
                              dtype='float32')
                sd.wait()
                audio_data.append(chunk)
                print(f"   Recording... {i+1}/{chunks} seconds")
            
            # Record any remaining time
            remaining = duration % chunk_duration
            if remaining > 0:
                chunk = sd.rec(int(remaining * self.sample_rate), 
                              samplerate=self.sample_rate, 
                              channels=self.channels, 
                              dtype='float32')
                sd.wait()
                audio_data.append(chunk)
            
            return np.concatenate(audio_data)
        else:
            # Record all at once
            audio_data = sd.rec(int(duration * self.sample_rate), 
                               samplerate=self.sample_rate, 
                               channels=self.channels, 
                               dtype='float32')
            sd.wait()
            return audio_data
    
    def save_audio_temp(self, audio_data):
        """
        Save audio data to a temporary file.
        
        Args:
            audio_data (numpy.ndarray): Audio data to save
            
        Returns:
            str: Path to the temporary audio file
        """
        # Create temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = tempfile.NamedTemporaryFile(
            suffix=f"_{timestamp}.wav", 
            delete=False,
            prefix="voice_input_"
        )
        
        # Save audio data
        sf.write(temp_file.name, audio_data, self.sample_rate)
        self.temp_file = temp_file.name
        
        print(f"💾 Audio saved to: {self.temp_file}")
        return self.temp_file
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        print("🔄 Transcribing audio with Whisper...")
        
        # Load model if not already loaded
        self.load_whisper_model()
        
        # Transcribe
        result = self.model.transcribe(audio_file_path)
        transcribed_text = result["text"].strip()
        
        print("✅ Transcription completed")
        return transcribed_text
    
    def cleanup_temp_file(self):
        """Clean up the temporary audio file"""
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.unlink(self.temp_file)
                print(f"🗑️  Cleaned up temporary file: {self.temp_file}")
            except Exception as e:
                print(f"⚠️  Warning: Could not delete temporary file {self.temp_file}: {e}")
    
    def record_and_transcribe(self, duration=10, cleanup=True):
        """
        Complete workflow: record audio and transcribe it.
        
        Args:
            duration (int): Recording duration in seconds
            cleanup (bool): Whether to clean up temporary files
            
        Returns:
            str: Transcribed text
        """
        try:
            # Record audio
            audio_data = self.record_audio(duration)
            
            # Save to temporary file
            audio_file = self.save_audio_temp(audio_data)
            
            # Transcribe
            transcribed_text = self.transcribe_audio(audio_file)
            
            # Clean up
            if cleanup:
                self.cleanup_temp_file()
            
            return transcribed_text
            
        except Exception as e:
            print(f"❌ Error during recording/transcription: {e}")
            if cleanup:
                self.cleanup_temp_file()
            return None

def main():
    """Main function to run the voice input script"""
    parser = argparse.ArgumentParser(description="Voice Input with Whisper Transcription")
    parser.add_argument("--duration", "-d", type=int, default=10, 
                       help="Recording duration in seconds (default: 10)")
    parser.add_argument("--model", "-m", type=str, default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model to use (default: base)")
    parser.add_argument("--sample-rate", "-sr", type=int, default=44100,
                       help="Audio sample rate in Hz (default: 44100)")
    parser.add_argument("--no-cleanup", action="store_true",
                       help="Don't clean up temporary audio files")
    parser.add_argument("--no-progress", action="store_true",
                       help="Don't show recording progress")
    
    args = parser.parse_args()
    
    print("🎤 Voice Input with Whisper Transcription")
    print("=" * 50)
    print(f"📋 Settings:")
    print(f"   • Duration: {args.duration} seconds")
    print(f"   • Model: {args.model}")
    print(f"   • Sample Rate: {args.sample_rate} Hz")
    print(f"   • Cleanup: {'No' if args.no_cleanup else 'Yes'}")
    print("=" * 50)
    
    # Initialize voice input system
    voice_input = VoiceInputWhisper(
        model_name=args.model,
        sample_rate=args.sample_rate
    )
    
    # Record and transcribe
    transcribed_text = voice_input.record_and_transcribe(
        duration=args.duration,
        cleanup=not args.no_cleanup
    )
    
    if transcribed_text:
        print("\n" + "=" * 50)
        print("📝 TRANSCRIPTION RESULT")
        print("=" * 50)
        print(transcribed_text)
        print("=" * 50)
    else:
        print("\n❌ Transcription failed")

if __name__ == "__main__":
    main() 