# ORIEN AI – Streaming Web App

A modern web-based streaming platform built with **Django**, allowing users to **upload**, **watch**, and **comment** on videos. Supports both **local uploads** and **YouTube imports**, with advanced features like **AI-powered dubbing**, **subtitles**, **user profiles**, and **view tracking**.

![Demo Screenshot](https://via.placeholder.com/800x400?text=App+Screenshot)  
*(Replace with actual screenshots in your repo)*

---

## Features

- **Video Uploads**  
  Upload local videos or import directly from YouTube.
- **Video Dubbing**  
  Generate dubbed versions of videos using AI (optional).
- **Comments System**  
  Users can post and view comments on videos.
- **User Profiles**  
  Customize profile picture and bio.
- **View Tracking**  
  Automatic view count for each video.
- **User Authentication**  
  Secure login, registration, and session management.
- **AI-powered Translation & Dubbing** *(Optional)*  
  Integrated audio extraction and translation modules.

---

## Tech Stack

- **Backend**: Django (Python 3.11.4)
- **Frontend**: HTML5 + Tailwind CSS
- **Database**: SQLite (for development)
- **AI Modules**: Audio extraction, translation, and text-to-speech (TTS) integration

---

## Installation & Setup

### Prerequisites
- Python 3.11+
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/streaming_web_app-dj.git
   cd streaming_web_app-dj
   ```

2. **Create and activate a virtual environment**

   **Unix/macOS:**
   ```bash
   python -m venv env
   source env/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **(Optional) Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to:  
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Screenshots

<img width="1693" height="1055" alt="image" src="https://github.com/user-attachments/assets/720083b9-e36b-4a4d-96e7-6ac2650e779b" />
<img width="1693" height="3185" alt="image" src="https://github.com/user-attachments/assets/27f8a072-0052-48d1-abdf-cb94d630d2ce" />
<img width="1814" height="948" alt="image" src="https://github.com/user-attachments/assets/e8266cbb-5bab-49ba-8ebc-4dabef74613e" />
<img width="1831" height="751" alt="image" src="https://github.com/user-attachments/assets/9bfde2a9-41c5-441c-b2c3-92fc6b3a965b" />

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch:  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:  
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a **Pull Request**

> For major changes, please open an **issue** first to discuss your idea.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Author

**Ariharan K.C.**  
ariharankc@gmail.com  
[LinkedIn Profile](https://linkedin.com/in/your-profile)  
[Portfolio](https://yourportfolio.com)

---