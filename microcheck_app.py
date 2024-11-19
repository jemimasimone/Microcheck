from pathlib import Path
from tkinter import Tk, Canvas, Button, Frame, BOTH, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import torch
import torchvision.transforms as transforms
from Pytorch_UNet.unet import UNet
import sys
import os
import datetime
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

# ----- PATH FILES FOR ASSETS
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ----- PATH FILES FOR MODEL
if getattr(sys, 'frozen', False):
    model_path = Path(sys._MEIPASS) / 'unet_tuning_epoch_30.pth'
else:
    model_path = Path(__file__).parent / 'unet_tuning_epoch_30.pth'

# ----- CALL YOUR MODEL
model = UNet(n_channels=3, n_classes=1)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# ----- RESPONSIVE IMAGES DEPENDING ON CANVAS
def resize_images(new_width):
    aspect_ratio_1 = original_button_image_1.height / original_button_image_1.width
    aspect_ratio_2 = original_button_image_2.height / original_button_image_2.width
    new_height_1 = int(new_width * aspect_ratio_1)
    new_height_2 = int(new_width * aspect_ratio_2)
    
    # Resize images
    resized_image_1 = original_button_image_1.resize((new_width, new_height_1), Image.Resampling.LANCZOS)
    resized_image_2 = original_button_image_2.resize((new_width, new_height_2), Image.Resampling.LANCZOS)
    
    return ImageTk.PhotoImage(resized_image_1), ImageTk.PhotoImage(resized_image_2)

# ----- RESIZE IMAGES UPOAN UPLOAD
def on_resize(event):
    if event.widget == window:
        # Button images
        new_width = max(100, window.winfo_width() // 8)
        resized_image_1, resized_image_2 = resize_images(new_width)
        
        button_1.configure(image=resized_image_1)
        button_1.image = resized_image_1
        button_2.configure(image=resized_image_2)
        button_2.image = resized_image_2
        
        # Redraw uploaded image
        try:
            if not any(main_content.uploaded_images):
                return  # No image to redraw
            
            # Get the uploaded image
            img, photo = main_content.uploaded_images[0]
            
            # Clear existing images on the canvas
            main_content.delete("all")
            
            # Canvas dimensions
            canvas_width = main_content.winfo_width()
            canvas_height = main_content.winfo_height()
            
            # Parameters for image placement
            margin = 10
            max_width = canvas_width - 2 * margin
            max_height = canvas_height - 2 * margin
            
            # Resize the image
            img_resized = img.copy()
            img_resized.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Update the PhotoImage
            photo_resized = ImageTk.PhotoImage(img_resized)
            
            # Calculate position (centered)
            x_position = canvas_width // 2
            y_position = canvas_height // 2
            
            # Place the image on the canvas
            main_content.create_image(x_position, y_position, image=photo_resized)
            
            # Update the reference to prevent garbage collection
            main_content.uploaded_images[0] = (img_resized, photo_resized)
        
        except AttributeError:
            # No images uploaded yet
            pass

# ----- UPLOAD IMAGES FUNCTION
def upload_images():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        multiple=False
    )
    
    if not file_path:
        return
    
    # Clear any existing images on the canvas
    main_content.delete("all")
    
    # Canvas dimensions
    canvas_width = main_content.winfo_width()
    canvas_height = main_content.winfo_height()
    
    # Parameters for image placement
    margin = 10
    num_images = 1
    max_width = (canvas_width - (num_images + 1) * margin) // num_images
    max_height = canvas_height - 2 * margin
    
    try:

        # Centered image
        x_position = canvas_width // 2
        y_position = canvas_height // 2

        # Open the image using PIL
        img = Image.open(file_path)
        image_filename = os.path.splitext(os.path.basename(file_path))[0]
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)


        # ----- PROCESS FOR U-NET
        preprocess = transforms.Compose([
            transforms.Resize((700, 700)), #Image size
            transforms.ToTensor(),
            # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # If your model was trained with this normalization
        ])
        
        img_tensor = preprocess(img).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(img_tensor) #Get predicted mask
        
        #Get confidence levels as probabilities
        confidence_levels = torch.sigmoid(outputs)

        #Color map -> image
        confidence_map = confidence_levels.cpu().numpy().squeeze()
        cmap = cm.get_cmap('viridis')
        colored = cmap(confidence_map)

        #Mean conf formula
        mean_confidence_levels = confidence_levels.mean(dim=[1, 2, 3]).cpu().numpy()

        for i, mean_confidence in enumerate(mean_confidence_levels):
            percentage_confidence = mean_confidence * 100 #Convert to percentage
            # ----- INTERPRETATION
            annotation_text = f'The highlighted image shows microplastic with confidence of {percentage_confidence:.2f}%'

        #Figure & axis
        fig, ax = plt.subplots()

        # colorbar
        im = ax.imshow(colored)
        cbar = ax.figure.colorbar(im, ax=ax)

        #Title
        ax.set_title(f'Confidence Map of Image {image_filename}\n{annotation_text}') #Annotation text - interpretation

        # ----- RESULTING IMAGE
        # Convert the Matplotlib figure to a PIL Image
        plt.savefig('temp.png')
        conf_pil = Image.open('temp.png')
        plt.close()

        # Convert the PIL Image to a Tkinter PhotoImage
        conf_tk = ImageTk.PhotoImage(conf_pil)


        # ----- DISPLAY IMAGE
        main_content.create_image(x_position, y_position, image=conf_tk)
        main_content.uploaded_images = [(conf_pil, conf_tk)]


    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image:\n{os.path.basename(file_path)}\n\n{e}")


# ----- SAVE IMAGE OUTPUT
def save_image():
    try:
        if not main_content.uploaded_images:
            messagebox.showwarning("No Image", "No image to save. Please upload an image first.")
            return
        
        # Get the PIL Image object (first item in the tuple)
        img = main_content.uploaded_images[0][0]
        
        # Open a save dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*"),
            ],
            title="Save Image As"
        )
        
        if not save_path:
            # User cancelled the save dialog
            return
        
        # Save the PIL Image object to the specified path
        img.save(save_path)
        messagebox.showinfo("Image Saved", f"Image successfully saved to:\n{save_path}")
    
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save image:\n{e}")

# ----- TKINTER
# Initialize main window
window = Tk()
window.title("MicroCheck")
window.geometry("750x750")
window.configure(bg="#FFFFFF")
window.resizable(True, True)

# Create a main frame
main_frame = Frame(window, bg="#FFFFFF")
main_frame.pack(fill=BOTH, expand=True)

# Configure grid weights for main_frame
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)  # Main content
main_frame.rowconfigure(1, weight=0)  # Footer

# Create the main content canvas (optional)
main_content = Canvas(
    main_frame,
    bg="#004e66",
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

main_content.grid(row=0, column=0, sticky="nsew")
main_content.uploaded_image = None

# Create a footer frame
footer_frame = Frame(main_frame, bg="#002733")
footer_frame.grid(row=1, column=0, sticky="ew")
footer_frame.columnconfigure(0, weight=1)
footer_frame.columnconfigure(1, weight=1)
footer_frame.rowconfigure(0, weight=1)

# Load original images using PIL
original_button_image_1 = Image.open(relative_to_assets("button_1.png"))
original_button_image_2 = Image.open(relative_to_assets("button_2.png"))

# Initial resize
initial_button_width = 120
button_image_1_resized, button_image_2_resized = resize_images(initial_button_width)

# Create "Upload" Button
button_1 = Button(
    footer_frame,
    image=button_image_1_resized,
    text="Scan Photo",
    compound="center",
    fg="#000000",
    font=("IstokWeb Bold", 12),
    borderwidth=0,
    highlightthickness=0,
    command=upload_images, #Action once clicked
    relief="flat",
    bg="#002733",              
    activebackground="#002733"
)

button_1.image = button_image_1_resized
button_1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# Create "Save" Button
button_2 = Button(
    footer_frame,
    image=button_image_2_resized,
    text="Save",
    compound="center",
    fg="#000000",      
    font=("IstokWeb Bold", 12), 
    borderwidth=0,
    highlightthickness=0,
    command=save_image,  #Action once clicked
    relief="flat",
    bg="#002733",             
    activebackground="#002733" 
)

button_2.image = button_image_2_resized  
button_2.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

canvas_width = main_content.winfo_width()
canvas_height = main_content.winfo_height()

# Bind the window resize event
window.bind("<Configure>", on_resize)

window.mainloop()
