from PIL import Image
import tkinter as tk
from tkinter import filedialog

def openImages(face_path, ci_path):
    faceImage = Image.open(face_path)
    ciImage = Image.open(ci_path)
    return [faceImage, ciImage]

def select_folder(title):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    return folder_path
