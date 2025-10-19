from django.shortcuts import render, redirect, get_object_or_404
from googleapiclient.discovery import build # type: ignore
from .forms import ProfileForm, SignUpForm, VideoUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User, Video
from django.core.files.storage import FileSystemStorage
from .dubbing_utils import dub_video_with_translation
import os, logging
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from pytube import YouTube  # type: ignore # Import YouTube video downloader

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set desired logging level
handler = logging.StreamHandler()  # Use FileHandler to log to a file if needed
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

YOUTUBE_API_KEY = 'AIzaSyD_IGZIrNLyo1iagBAQqs7a-maAkWsoz3k' #'apikey.json'

def get_youtube_service():
    """ Initialize and return the YouTube API service """
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_recommended_videos():
    """ Fetch the most popular videos from the YouTube API with caching """
    cache_key = 'recommended_videos'
    videos = cache.get(cache_key)
    
    if not videos:
        youtube = get_youtube_service()
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            maxResults=10,
            regionCode="US"
        )
        response = request.execute()
        videos = []
        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'video_id': item['id'],
                'source': 'YouTube'
            }
            videos.append(video)
        cache.set(cache_key, videos, timeout=60 * 15)  # Cache for 15 minutes
    
    return videos
    #else:
            #return render(request,'404.html')


def home(request):
    """ Render the home page with local and recommended videos """
    local_videos = Video.objects.all()
    recommended_videos = get_recommended_videos()
    return render(request, 'home.html', {
        'local_videos': local_videos,
        'recommended_videos': recommended_videos
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', reverse('home'))
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile_update.html', {'form': form})

def logout_view(request):
    """ Handle user logout """
    logout(request)
    return redirect('home')

def search_videos(request):
    query = request.GET.get('q', '')
    search_results = []
    if query:
        try:
            youtube = get_youtube_service()
            search_response = youtube.search().list(
                q=query,
                part="id,snippet",
                maxResults=10
            ).execute()
            
            for item in search_response.get('items', []):
                if item['id']['kind'] == 'youtube#video':
                    video_data = {
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url'],
                        'video_id': item['id']['videoId'],
                        'source': 'YouTube'
                    }
                    search_results.append(video_data)
            
          #  logger.debug(f"Search results fetched: {search_results}")
        
        except Exception as e:
           # logger.error(f"Error fetching search results: {str(e)}")
            messages.error(request, "Error retrieving search results.")
    
    paginator = Paginator(search_results, 5)  # Show 5 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'search_results.html', {
        'query': query,
        'search_results': search_results,
    })


@login_required
def user_profile(request, username):
    """ Display user profile """
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})

@login_required
def watch_video(request, video_id):
    video_details = None
    try:
        # Fetch video from local database
        video = Video.objects.get(video_id=video_id)
        video_details = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'thumbnail': video.thumbnail,
            'video_file': video.video_file.url,
            'view_count': video.view_count,
            'source': 'Local',
            'video_id': video.video_id,  # Ensure video_id is included
        }
    except Video.DoesNotExist:
        logger.warning(f"Video with ID {video_id} not found in local database.")
        try:
            # Fetch video from YouTube if not found locally
            youtube = get_youtube_service()
            youtube_request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
            response = youtube_request.execute()
            if response['items']:
                item = response['items'][0]
                video_details = {
                    'id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'video_id': video_id,
                    'source': 'YouTube',
                    'video_file': f'https://www.youtube.com/watch?v={video_id}'
                }
            else:
                logger.error(f"Video with ID {video_id} not found on YouTube.")
                messages.error(request, "Video not found on YouTube.")
                raise Http404("Video not found on YouTube.")
        except Exception as e:
            logger.error(f"Error fetching video from YouTube: {str(e)}")
            messages.error(request, "Error retrieving video from YouTube.")
            raise Http404("Error retrieving video from YouTube.")

    return render(request, 'watch.html', {'video': video_details})


@login_required
def upload_video(request):
    """ Handle video upload by users """
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = request.user
            video.source = Video.LOCAL  # Ensure it's marked as a local upload
            video.video_file = request.FILES['video_file']  # Explicitly set the uploaded file
            video.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an issue with the upload. Please try again.")
    else:
        form = VideoUploadForm()
    
    return render(request, 'upload_video.html', {'form': form})


from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage

@login_required
def dub_video(request, video_id):
    try:
        video = Video.objects.get(video_id=video_id)
        video_source = 'Local'
        video_file_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
    except Video.DoesNotExist:
        youtube = get_youtube_service()
        youtube_request = youtube.videos().list(part="snippet", id=video_id)
        response = youtube_request.execute()
        if not response.get('items'):
            messages.error(request, "Video not found on YouTube.")
            raise Http404("Video not found on YouTube.")
        item = response['items'][0]
        video_source = 'YouTube'
        youtube_video_url = f'https://www.youtube.com/watch?v={video_id}'
        temp_video_path = os.path.join(settings.MEDIA_ROOT, f'{video_id}.mp4')
        try:
            yt = YouTube(youtube_video_url)
            stream = yt.streams.get_highest_resolution()
            stream.download(filename=temp_video_path)
            video_file_path = temp_video_path
        except Exception as e:
            messages.error(request, "Error downloading YouTube video for dubbing.")
            return redirect('watch', video_id=video_id)

    target_language = request.POST.get('language')
    if not target_language:
        messages.error(request, "Please select a target language.")
        return redirect('watch', video_id=video_id)

    if not os.path.exists(video_file_path):
        messages.error(request, "Original video file not found.")
        return redirect('watch', video_id=video_id)

    try:
        # Call the dubbing function
        dubbed_video_path = dub_video_with_translation(video_file_path, target_language)
        if not os.path.exists(dubbed_video_path):
            messages.error(request, "Dubbed video not created. Try again.")
            return redirect('watch', video_id=video_id)

        # Save the dubbed video file in the 'dub_videos' directory
        fs = FileSystemStorage(location=settings.DUB_VIDEOS_DIR)
        dubbed_video_name = f'dubbed_{video_id}_{target_language}.mp4'
        with open(dubbed_video_path, 'rb') as dubbed_video_file:
            saved_file = fs.save(dubbed_video_name, dubbed_video_file)

        # If the video was from YouTube, remove the temporary download
        if video_source == 'YouTube':
            os.remove(video_file_path)

        # Remove the temporary dubbed video file
        os.remove(dubbed_video_path)

        messages.success(request, f"Video dubbed successfully in {target_language}!")

        # Provide the relative URL to the dubbed video
        dubbed_video_url = os.path.join(settings.MEDIA_URL, 'dub_videos', dubbed_video_name)

        return render(request, 'watch.html', {
            'video': video,
            'dubbed_video': dubbed_video_url,
            'dubbed_language': target_language
        })
    except Exception as e:
        messages.error(request, "Error in dubbing process.")
        return redirect('watch', video_id=video_id)


def test_video_view(request):
    """ Test view to check video display """
    return render(request, 'test_video.html')
