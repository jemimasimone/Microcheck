from pathlib import Path
from tkinter import Tk, Canvas, Button, Frame, BOTH, filedialog, messagebox
from PIL import Image, ImageTk
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def resize_images(new_width):
    aspect_ratio_1 = original_button_image_1.height / original_button_image_1.width
    aspect_ratio_2 = original_button_image_2.height / original_button_image_2.width
    new_height_1 = int(new_width * aspect_ratio_1)
    new_height_2 = int(new_width * aspect_ratio_2)
    
    # Resize images
    resized_image_1 = original_button_image_1.resize((new_width, new_height_1), Image.Resampling.LANCZOS)
    resized_image_2 = original_button_image_2.resize((new_width, new_height_2), Image.Resampling.LANCZOS)
    
    return ImageTk.PhotoImage(resized_image_1), ImageTk.PhotoImage(resized_image_2)

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
            if not main_content.uploaded_images:
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
            
            # Resize the image if necessary
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

def upload_images():
    # Open file dialog to select a single image
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
    num_images = 1
    max_width = (canvas_width - (num_images + 1) * margin) // num_images
    max_height = canvas_height - 2 * margin
    
    try:
        # Open the image using PIL
        img = Image.open(file_path)
        
        # Resize the image while maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Convert the image to PhotoImage
        photo = ImageTk.PhotoImage(img)
        
        # Calculate position (centered)
        x_position = canvas_width // 2
        y_position = canvas_height // 2
        
        # Add the image to the canvas
        main_content.create_image(x_position, y_position, image=photo)
        
        # Keep a reference to prevent garbage collection
        main_content.uploaded_images = [(img, photo)]
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image:\n{os.path.basename(file_path)}\n\n{e}")

def save_image():
    try:
        if not main_content.uploaded_images:
            messagebox.showwarning("No Image", "No image to save. Please upload an image first.")
            return
        
        # Assuming only one image is uploaded
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
        
        # Save the image
        img.save(save_path)
        messagebox.showinfo("Image Saved", f"Image successfully saved to:\n{save_path}")
    
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save image:\n{e}")

# Initialize main window
window = Tk()
window.title("Microcheck")
window.geometry("700x550")
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
    text="Upload",
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

# Bind the window resize event
window.bind("<Configure>", on_resize)

window.mainloop()
