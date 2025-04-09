import asyncio
import uuid

from transcribe import process_audio


async def main():
    job_id = uuid.uuid4()
    transcript = await process_audio(audio_path="noname.mp3", job_id=job_id)
    
    print(transcript.text)  # Optional: do something with it

if __name__ == "__main__":
    asyncio.run(main())
