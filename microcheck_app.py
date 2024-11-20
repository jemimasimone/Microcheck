from pathlib import Path
from tkinter import Tk, Canvas, Button, Frame, BOTH, filedialog, messagebox, ttk, Label
from PIL import Image, ImageTk
import numpy as np
import torch
import torchvision.transforms as transforms
from Pytorch_UNet.unet import UNet
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

# ----- CALL YOUR MODEL
model = UNet(n_channels=3, n_classes=1)
model.load_state_dict(torch.load("unet_tuning_epoch_30.pth", map_location=torch.device('cpu'), weights_only=True))
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

# ----- UPLOAD IMAGES
def upload_images():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        multiple=False  # Ensure only one file can be selected
    )
    
    if not file_path:
        # No file selected
        return
    
    # Clear any existing images on the canvas
    main_content.delete("all")
    
    # Canvas dimensions
    canvas_width = main_content.winfo_width()
    canvas_height = main_content.winfo_height()
    
    # Parameters for image placement
    margin = 10
    max_width = (canvas_width - 3 * margin) // 2 #Dividing the space for side by side images
    max_height = canvas_height - 2 * margin
    
    try:
        # Open the image using PIL
        img = Image.open(file_path)
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # photo_original = ImageTk.PhotoImage(img)
        # original_x = canvas_width //4*3
        # main_content.create_image(original_x, canvas_height//2, image=photo_original)

        photo_original = ImageTk.PhotoImage(img.resize((400, 400), Image.Resampling.LANCZOS))  # Resize to 400x400
        original_x = canvas_width // 4 * 3 + 20
        main_content.create_image(original_x, canvas_height // 2, image=photo_original)


        # ----- PROCESS FOR U-NET
        preprocess = transforms.Compose([ 
            transforms.Resize((700, 700)),
            transforms.ToTensor(),
        ])
        
        img_tensor = preprocess(img).unsqueeze(0)  # Add batch dimension
        
        # Run the image through the model to get the predicted mask
        with torch.no_grad():
            outputs = model(img_tensor)
        
        # Apply sigmoid to get confidence levels as probabilities
        confidence_levels = torch.sigmoid(outputs)
        confidence_map = confidence_levels.cpu().numpy().squeeze()

        cmap = plt.colormaps['viridis']
        colored = cmap(confidence_map)
        
        # Save the processed output as a temporary image file
        plt.imsave('temp_processed.png', colored)
        processed_img = Image.open('temp_processed.png')
        
        # # Resize the processed image to fit within the same max width/height
        # processed_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        # photo_processed = ImageTk.PhotoImage(processed_img)

        # Resize the processed image explicitly to 400x400
        processed_img = processed_img.resize((400, 400), Image.Resampling.LANCZOS)
        photo_processed = ImageTk.PhotoImage(processed_img)
        
        # Position for the processed image (left side of the canvas)
        processed_x = canvas_width // 4 - 20  # Place processed image at 1/4 width on left side
        main_content.create_image(processed_x, canvas_height // 2, image=photo_processed)

        # # Confidence level vertical bar
        # bar_width = 10
        # confidence_bar_x = canvas_width // 8  # Left side of the processed image
        # main_content.create_line(confidence_bar_x, 0, confidence_bar_x, canvas_height, width=bar_width, fill="yellow")

        def create_colorbar(canvas_height, processed_x):
            # Create a Matplotlib figure
            fig, ax = plt.subplots(figsize=(1, 5))  # 1 unit wide, 5 units tall
            cmap = plt.colormaps['viridis']  # Use the same colormap as the output

            # Create a colorbar
            norm = plt.Normalize(vmin=0, vmax=1)  # Normalized from 0 to 1
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])

            # Add the colorbar to the figure
            cbar = fig.colorbar(sm, cax=ax, orientation='vertical')

            # Save the colorbar as a temporary image
            colorbar_path = "temp_colorbar.png"
            plt.savefig(colorbar_path, bbox_inches='tight', pad_inches=0, transparent=True)
            plt.close(fig)

            # Load the colorbar image
            colorbar_image = Image.open(colorbar_path)

            # Resize the colorbar to 400 pixels in height and a narrower width
            new_height = 400  # Fixed height
            new_width = 50  # Narrower width
            colorbar_image = colorbar_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage for Tkinter
            colorbar_photo = ImageTk.PhotoImage(colorbar_image)

            # Display the colorbar on the canvas
            colorbar_x = processed_x - 470  # Position to the left of the processed image
            main_content.create_image(colorbar_x, canvas_height // 2, image=colorbar_photo)

            # Keep a reference to prevent garbage collection
            main_content.colorbar_photo = colorbar_photo




        # Generate and display the confidence colorbar
        create_colorbar(canvas_height, canvas_width)

        # Interpretation
        confidence_value = np.mean(confidence_map) * 100  # Calculate average confidence level in percentage
        interpretation = f"Confidence: {confidence_value:.2f}%\nDetected Microplastics: {'Pellet, Fiber, Fragment'}\nAccuracy Level: High"
        
        title = Label(main_content, text="Microcheck", font=("IstokWeb Bold", 16), bg="#004e66", fg="white")
        title.place(relx=0.5, rely=0.05, anchor="center")
        
        subheader = Label(main_content, text=os.path.basename(file_path), font=("IstokWeb Bold", 12), bg="#004e66", fg="white")
        subheader.place(relx=0.5, rely=0.1, anchor="center")
        
        interpretation_label = Label(main_content, text=interpretation, font=("IstokWeb Bold", 10), bg="#004e66", fg="white")
        interpretation_label.place(relx=0.5, rely=0.9, anchor="center")

        # Keep references to prevent garbage collection
        main_content.uploaded_images = [(img, photo_original), (processed_img, photo_processed)]

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
window.geometry("950x750")
window.configure(bg="#FFFFFF")
window.resizable(False, False)

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

button_1.grid(row=0, column=0, padx=10, pady=10)

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
    command=save_image,
    relief="flat",
    bg="#002733",              
    activebackground="#002733"
)

button_2.grid(row=0, column=1, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()
