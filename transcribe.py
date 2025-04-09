from google import genai

from google.genai.types import HttpOptions, Part, GenerateContentConfig

from utils import upload_to_bucket
from models import Transcript

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def process_audio(audio_path, job_id):
    try:
        # Upload file to Gemini
        logger.info(f"Uploading audio file: {audio_path}")
        
        # Set up the client with timestamp configuration
        client = genai.Client(http_options=HttpOptions(api_version="v1"))

        # Prepare the transcription prompt
        prompt = """
        <task>
        Transcribe the audio in SRT format for short format content. 
        </task>
        <input>Audio will be provided to you </input>

        <guidelines> 
        - Only output Hinglish 
        - Use Roman script for Hindi words  
        - Capture natural language mix  
        - Differentiate speakers clearly  
        - Include all dialogue nuances  
        - Ensure timestamps are in SRT format (HH:MM:SS,MMM)  
        - Keep subtitle length between 3-5 words per segment 
        </guidelines>

        <output>
        
        <entire_transcript>
        1
        00:00:00,000 --> 00:00:05,000  
        Speaker X: Transcription text

        2
        00:00:05,000 --> 00:00:10,000  
        Speaker X: Transcription text

        ...
        </entire_transcript>
        Only output in SubRip SRT format

        Put the entire transcirpt into the Trancript class. 

        class Transcript(BaseModel): 
            text: str = Field(description="the trancription on audio in SRT format")
            duration: float = Field(description=("total duration of audio in seconds"))


        return: Transcript
        </output>

        """
       
        gcs_uri = await upload_to_bucket(local_file_path=audio_path, blob_name=f"{job_id}.mp3" )
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=[
                    prompt,
                    Part.from_uri(
                        file_uri=gcs_uri,
                        mime_type="audio/mpeg",
                    ),
                ],
                config=GenerateContentConfig(audio_timestamp=True, response_mime_type='application/json', response_schema=Transcript),
            )
            logger.info(response)


        except Exception as e:
            logger.info(f"Error during transcription: {e}")
            raise e
        
        transcript: Transcript = response.parsed

        return transcript
    
    except Exception as e:
        logger.error(f"Error in processing audio: {str(e)}")

        raise str(e)
