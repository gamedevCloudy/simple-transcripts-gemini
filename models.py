from pydantic import BaseModel, Field

class Transcript(BaseModel): 
    text: str = Field(description="the trancription on audio in SRT format")
