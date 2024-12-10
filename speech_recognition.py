import whisper
import logging

logging.basicConfig(
    filename="../logs/speech_recognition.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transcribe_audio(input_file, output_file):
    model = whisper.load_model("base")
    result = model.transcribe(input_file)
    with open(output_file, "w") as f:
        f.write(result["text"])


if __name__ == "__main__":
    import os
    os.makedirs("../transcripts", exist_ok=True)

    transcribe_audio("../audio/call_audio.wav", "../transcripts/call_1_transcript.txt")
