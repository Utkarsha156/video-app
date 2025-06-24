import os
import uuid
import cv2
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models

# Load ResNet18 model and remove final classification layer
resnet = models.resnet18(pretrained=True)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1])
resnet.eval()

# Preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    ),
])

@torch.no_grad()
def compute_resnet_vector(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    features = resnet(tensor).squeeze().numpy()
    return features.tolist()

def extract_frames(video_path, output_dir, interval_sec=1):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    frame_interval = int(fps * interval_sec)

    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0
    saved_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            saved_frames.append(filepath)
        frame_count += 1

    cap.release()
    return saved_frames
