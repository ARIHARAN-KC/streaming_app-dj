# ORIEN AI - Streaming Web App

A modern web-based streaming platform built with **Django**, allowing users to upload, watch, and comment on videos.  
Supports both **local uploads** and **YouTube imports**, with features like dubbing, subtitles, and user profiles.

---

## 🚀 Features

- 🎥 **Video Uploads** — Upload local videos or stream directly from YouTube.
- 🧩 **Video Dubbing** — Generate dubbed versions of uploaded videos.
- 💬 **Comments System** — Users can comment on videos.
- 👤 **User Profiles** — Profile picture and bio customization.
- 📊 **View Tracking** — Automatic view count for each video.
- 🔐 **User Authentication** — Login, registration, and secure session management.
- 🧠 **AI-powered Translation/Dubbing (optional)** — Integrated with audio extraction and translation modules.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django 5.1 |
| Database | SQLite (default) |
| Frontend | Django Templates + Bootstrap/Tailwind |
| Media Handling | Django FileField, ffmpeg |
| Language | Python 3.11 |
| Authentication | Django Auth System |

---

## Installation & Setup

### Clone the repository
```bash
git clone https://github.com/<your-username>/streaming_web_app-dj.git
cd streaming_web_app-dj
Create and activate a virtual environment
bash
python -m venv env
env\Scripts\activate
Install dependencies
bash
pip install -r requirements.txt
Apply migrations
bash
python manage.py makemigrations
python manage.py migrate
Run the development server
bash
python manage.py runserver
Then open:
http://127.0.0.1:8000/
Screenshots
<img width="1693" height="1055" alt="image" src="https://github.com/user-attachments/assets/720083b9-e36b-4a4d-96e7-6ac2650e779b" />
<img width="1693" height="3185" alt="image" src="https://github.com/user-attachments/assets/27f8a072-0052-48d1-abdf-cb94d630d2ce" />
<img width="1814" height="948" alt="image" src="https://github.com/user-attachments/assets/e8266cbb-5bab-49ba-8ebc-4dabef74613e" />
<img width="1831" height="751" alt="image" src="https://github.com/user-attachments/assets/9bfde2a9-41c5-441c-b2c3-92fc6b3a965b" />	
Contributing
Pull requests are welcome!
Please fork this repository and open a PR with clear commit messages.
License
This project is licensed under the MIT License — see the LICENSE file for details.
Author
Ariharan K.C.
ariharankc@gmail.com
[LinkedIn Profile](https://www.linkedin.com/in/ariharankc07/)
https://ariharan-portfolifo.vercel.app/
