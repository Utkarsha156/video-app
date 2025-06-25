# Video Frame Feature Search using FastAPI and Qdrant

This project is a web application built with FastAPI that allows users to upload videos, extract frames at regular intervals, compute feature vectors for each frame using ResNet, and search for visually similar frames using vector similarity with Qdrant. A simple HTML frontend is included for user interaction.

## Features

- Upload MP4 video files
- Extract frames at 1-second intervals
- Compute feature vectors using ResNet18
- Store vectors in Qdrant (in-memory vector database)
- Search for similar frames based on an image input
- Access individual frames by filename
- User interface built with HTML and CSS

## Project Structure

```
video-app/
├── main.py               # FastAPI application
├── utils.py              # Utility functions for frame extraction and vector computation
├── static/
│   └── index.html        # Frontend HTML interface
├── frames/               # Directory where extracted frames are stored
├── requirements.txt      # Python dependencies
├── Procfile              # Railway deployment entry
└── .gitignore            # Git ignore rules
```

## Technologies Used

- FastAPI
- Qdrant (in-memory mode)
- PyTorch (ResNet18 for feature extraction)
- OpenCV
- HTML, CSS (for frontend UI)


## API Endpoints

| Method | Endpoint            | Description                             |
|--------|---------------------|-----------------------------------------|
| POST   | /upload-video/      | Uploads a video and extracts frames     |
| POST   | /search-similar/    | Uploads an image and finds similar frames |
| GET    | /list-frames/       | Lists all extracted frame filenames     |
| GET    | /frame/{filename}   | Retrieves a specific frame image        |

## Screenshots

Below are screenshots of the 4 core frontend options:

### 1. Upload Video
Allows uploading a video file (e.g., `.mp4`) for processing.

![Upload Video](https://github.com/user-attachments/assets/930bb561-77fa-44de-a815-58a213fd31c0)



---

### 2. Search Using Uploaded Image
Lists all frames extracted from the uploaded video.


![List Frames](https://github.com/user-attachments/assets/f2bb635f-2d11-415f-a6df-85e3965516c2)



---

### 3. View All Extracted Frames 
Finds similar frames to a given image using vector similarity.


![Search by Image](https://github.com/user-attachments/assets/a49e1a62-b9cb-45f3-962c-e70db71cccc6)
![Search by Image](https://github.com/user-attachments/assets/c9c63fe8-b205-468e-83ba-7db2edffd446)



---

### 4. Search Using Frame Name (from list)
Search using a frame already extracted and listed.


![name](https://github.com/user-attachments/assets/e9975690-e94d-4532-bc60-47f23f1e1661)

![Search by Name](https://github.com/user-attachments/assets/e33cbbc7-a7a2-44df-bbed-baee895fcc39)





## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/video-app.git
cd video-app
```

### 2. Set up a virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # On Windows
# source venv/bin/activate  # On Linux/macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

Open your browser and navigate to: `http://127.0.0.1:8000`






