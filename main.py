import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse

# Load environment variables
load_dotenv()

# Initialize the Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja templates
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(now=lambda: datetime.now())


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    videos = supabase.storage.from_(SUPABASE_BUCKET).list()
    videos = (video for video in videos if video['name'].endswith('.mp4'))
    return templates.TemplateResponse('home.html', {'request': request, 'videos': videos})

@app.get('/videos/{video_name}')
async def get_video(video_name: str):
    video_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(video_name)
    if not video_url:
        return {'error': 'video not found'}
    
    async def video_stream():
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', video_url, headers={'Range': 'bytes=0-'}, timeout=60.0) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
    return StreamingResponse(video_stream(), media_type='video/mp4')
              
@app.get('/watch/{video_name}', response_class=HTMLResponse)
async def watch_video(request: Request, video_name: str):
    title = video_name.rsplit('.',1)[0].replace('_', ' ')
    return templates.TemplateResponse('watch.html', {'request': request, 'video_name': video_name, 'title': title})

@app.get('/upload', response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse('upload.html', {'request': request})

@app.post('/upload')
async def upload_video(request: Request, title: str = File(...), video_file: UploadFile = File(...)):
    contents = await video_file.read()
    
    file_extension = video_file.filename.split('.')[-1]
    file_name = f"{title.replace(' ', '_')}.{file_extension}"
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(
        file_name,
        contents,
        file_options={
            'content-type': 'video/mp4'
        }
    )
    
    if res.path:
        message = 'Video uploaded successfully.'
    else:
        message = 'Error uploading video.'
        

    return templates.TemplateResponse('upload.html', {'request': request, 'message': message})
