from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_profiles
from fastapi.responses import FileResponse
import pandas as pd
import tempfile
import os

app = FastAPI()
class ScrapeRequest(BaseModel):
    li_at: str
    search_link: str
    max_results: int

@app.post("/scrape/")
async def scrape(request: ScrapeRequest):
    try:
        data = scrape_profiles(request.li_at, request.search_link, request.max_results)

        # Convert to DataFrame and save to temp CSV
        df = pd.DataFrame(data)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(tmp.name, index=False)

        return FileResponse(path=tmp.name, filename="linkedin_profiles.csv", media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
