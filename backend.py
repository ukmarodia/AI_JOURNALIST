from fastapi import FastAPI, HTTPException, File, Response
from dotenv import load_dotenv
from models import NewsRequest

app = FastAPI();
load_dotenv()

@app.post("/generate-news")
async def generate_news_audio(request: NewsRequest):
    try:
        results = {}
        if request.source_type in ["news", "both"]:
            results["news"] = {"news_scraped": " this is from google news"}

        if request.source_type in ["reddit", "both"]:
            results ["reddit"] = {"reddit_scraped": "This is from reddit"}

        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})

        #setup llm summarizer

        news_summary = my_summary_function(news_data, reddit_data)

        #convert summary to audio 
        audio_path = convert_text_to_audio(news_summary)

        if audio_path:
            return response, headers, etc
        
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))    