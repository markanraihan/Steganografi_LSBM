import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import random
import hashlib

# Helper function: get pixel order based on password
def get_pixel_order(width, height, password):
    seed = int(hashlib.sha256(password.encode()).hexdigest(), 16) % (10 ** 8)
    coords = [(x, y) for y in range(height) for x in range(width)]
    random.seed(seed)
    random.shuffle(coords)
    return coords

# Encoding function
def embed_message(path, message, password):
    img = Image.open(path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    message_bin = ''.join(format(ord(c), '08b') for c in message)
    length_bin = format(len(message_bin), '032b')
    total_bin = length_bin + message_bin

    coords = get_pixel_order(width, height, password)
    if len(total_bin) > len(coords):
        raise ValueError("Pesan terlalu panjang untuk gambar ini.")

    for i, bit in enumerate(total_bin):
        x, y = coords[i]
        r, g, b = pixels[x, y]
        channel = random.choice([0, 1, 2])
        color = [r, g, b]

        current_lsb = color[channel] % 2
        bit = int(bit)
        if current_lsb != bit:
            color[channel] = color[channel] + 1 if color[channel] < 255 else color[channel] - 1
        pixels[x, y] = tuple(color)

    out_path = path.replace('.', '_stego.')
    img.save(out_path)
    return out_path

# Decoding function
def extract_message(path, password):
    img = Image.open(path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    coords = get_pixel_order(width, height, password)

    bits = ""
    for i in range(32):
        x, y = coords[i]
        r, g, b = pixels[x, y]
        bits += str([r, g, b][random.choice([0, 1, 2])] % 2)
    msg_len = int(bits, 2)

    bits = ""
    for i in range(32, 32 + msg_len):
        x, y = coords[i]
        r, g, b = pixels[x, y]
        bits += str([r, g, b][random.choice([0, 1, 2])] % 2)

    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

# Configure modern styles
def setup_styles():
    style = ttk.Style()
    
    # Configure button styles
    style.configure('Modern.TButton',
                   font=('Segoe UI', 10),
                   padding=(20, 10))
    
    style.configure('Primary.TButton',
                   font=('Segoe UI', 11, 'bold'),
                   padding=(25, 12))
    
    style.configure('Secondary.TButton',
                   font=('Segoe UI', 9),
                   padding=(15, 8))
    
    # Configure label styles
    style.configure('Title.TLabel',
                   font=('Segoe UI', 16, 'bold'),
                   foreground='#2c3e50')
    
    style.configure('Subtitle.TLabel',
                   font=('Segoe UI', 12, 'bold'),
                   foreground='#34495e')
    
    style.configure('Normal.TLabel',
                   font=('Segoe UI', 10),
                   foreground='#2c3e50')
    
    # Configure entry styles
    style.configure('Modern.TEntry',
                   font=('Segoe UI', 10),
                   fieldbackground='white',
                   borderwidth=2,
                   relief='solid')

# Create modern frame with gradient-like effect
def create_modern_frame(parent, bg_color='#f8f9fa'):
    frame = tk.Frame(parent, bg=bg_color, relief='flat', bd=0)
    return frame

# GUI Main Menu
def show_main_menu():
    clear_widgets()
    
    # Main container
    main_frame = create_modern_frame(root, '#ecf0f1')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, text="🔐 LSB Matching Steganography", style='Title.TLabel')
    title_label.pack(pady=(0, 10))
    
    # Subtitle
    subtitle_label = ttk.Label(main_frame, text="Pilih Mode Operasi:", style='Subtitle.TLabel')
    subtitle_label.pack(pady=(20, 30))
    
    # Button container
    button_frame = create_modern_frame(main_frame, '#ecf0f1')
    button_frame.pack(pady=20)
    
    # Encoding button
    encoding_btn = ttk.Button(button_frame, text="📝 Encoding", 
                             style='Primary.TButton', command=show_encoding_interface)
    encoding_btn.pack(pady=10, padx=20, fill='x')
    
    # Decoding button
    decoding_btn = ttk.Button(button_frame, text="🔍 Decoding", 
                             style='Primary.TButton', command=show_decoding_interface)
    decoding_btn.pack(pady=10, padx=20, fill='x')
    
    # Footer
    footer_label = ttk.Label(main_frame, text="Sembunyikan pesan rahasia dalam gambar dengan aman", 
                            style='Normal.TLabel')
    footer_label.pack(pady=(40, 0))

# GUI Encoding
def show_encoding_interface():
    clear_widgets()

    def browse_image():
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp")])
        if filepath:
            path_var.set(filepath)

    def do_embed():
        path = path_var.get()
        message = msg_entry.get()
        password = pass_entry.get()
        if not path or not message or not password:
            messagebox.showwarning("Input Missing", "Semua input harus diisi.")
            return
        try:
            result = embed_message(path, message, password)
            messagebox.showinfo("Berhasil", f"Pesan berhasil disisipkan ke: {result}")
            show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Main container
    main_frame = create_modern_frame(root, '#ecf0f1')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header_frame = create_modern_frame(main_frame, '#3498db')
    header_frame.pack(fill='x', pady=(0, 20))
    
    header_label = tk.Label(header_frame, text="📝 ENCODING MODE", 
                           font=('Segoe UI', 14, 'bold'), 
                           fg='white', bg='#3498db', pady=15)
    header_label.pack()
    
    # Content frame
    content_frame = create_modern_frame(main_frame, '#ffffff')
    content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Image selection section
    img_section = create_modern_frame(content_frame, '#ffffff')
    img_section.pack(fill='x', pady=10, padx=20)
    
    ttk.Label(img_section, text="📁 Pilih Gambar:", style='Normal.TLabel').pack(anchor='w', pady=(10, 5))
    
    path_frame = tk.Frame(img_section, bg='#ffffff')
    path_frame.pack(fill='x', pady=5)
    
    path_var = tk.StringVar()
    path_entry = ttk.Entry(path_frame, textvariable=path_var, style='Modern.TEntry', width=50)
    path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
    
    browse_btn = ttk.Button(path_frame, text="Browse", style='Secondary.TButton', command=browse_image)
    browse_btn.pack(side='right')
    
    # Message section
    msg_section = create_modern_frame(content_frame, '#ffffff')
    msg_section.pack(fill='x', pady=10, padx=20)
    
    ttk.Label(msg_section, text="💬 Pesan untuk disisipkan:", style='Normal.TLabel').pack(anchor='w', pady=(10, 5))
    msg_entry = ttk.Entry(msg_section, style='Modern.TEntry', width=50)
    msg_entry.pack(fill='x', pady=5)
    
    # Password section
    pass_section = create_modern_frame(content_frame, '#ffffff')
    pass_section.pack(fill='x', pady=10, padx=20)
    
    ttk.Label(pass_section, text="🔑 Password:", style='Normal.TLabel').pack(anchor='w', pady=(10, 5))
    pass_entry = ttk.Entry(pass_section, show='*', style='Modern.TEntry', width=50)
    pass_entry.pack(fill='x', pady=5)
    
    # Button section
    btn_section = create_modern_frame(content_frame, '#ffffff')
    btn_section.pack(fill='x', pady=20, padx=20)
    
    embed_btn = ttk.Button(btn_section, text="✅ Sisipkan Pesan", 
                          style='Primary.TButton', command=do_embed)
    embed_btn.pack(pady=10)
    
    back_btn = ttk.Button(btn_section, text="⬅️ Kembali ke Menu", 
                         style='Secondary.TButton', command=show_main_menu)
    back_btn.pack(pady=5)

# GUI Decoding
def show_decoding_interface():
    clear_widgets()

    def browse_image():
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp")])
        if filepath:
            path_var.set(filepath)

    def do_extract():
        path = path_var.get()
        password = pass_entry.get()
        if not path or not password:
            messagebox.showwarning("Input Missing", "Path dan password harus diisi.")
            return
        try:
            result = extract_message(path, password)
            messagebox.showinfo("Pesan Ditemukan", f"Pesan: {result}")
            show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Main container
    main_frame = create_modern_frame(root, '#ecf0f1')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header_frame = create_modern_frame(main_frame, '#e74c3c')
    header_frame.pack(fill='x', pady=(0, 20))
    
    header_label = tk.Label(header_frame, text="🔍 DECODING MODE", 
                           font=('Segoe UI', 14, 'bold'), 
                           fg='white', bg='#e74c3c', pady=15)
    header_label.pack()
    
    # Content frame
    content_frame = create_modern_frame(main_frame, '#ffffff')
    content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Image selection section
    img_section = create_modern_frame(content_frame, '#ffffff')
    img_section.pack(fill='x', pady=10, padx=20)
    
    ttk.Label(img_section, text="📁 Pilih Gambar:", style='Normal.TLabel').pack(anchor='w', pady=(10, 5))
    
    path_frame = tk.Frame(img_section, bg='#ffffff')
    path_frame.pack(fill='x', pady=5)
    
    path_var = tk.StringVar()
    path_entry = ttk.Entry(path_frame, textvariable=path_var, style='Modern.TEntry', width=50)
    path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
    
    browse_btn = ttk.Button(path_frame, text="Browse", style='Secondary.TButton', command=browse_image)
    browse_btn.pack(side='right')
    
    # Password section
    pass_section = create_modern_frame(content_frame, '#ffffff')
    pass_section.pack(fill='x', pady=10, padx=20)
    
    ttk.Label(pass_section, text="🔑 Password:", style='Normal.TLabel').pack(anchor='w', pady=(10, 5))
    pass_entry = ttk.Entry(pass_section, show='*', style='Modern.TEntry', width=50)
    pass_entry.pack(fill='x', pady=5)
    
    # Button section
    btn_section = create_modern_frame(content_frame, '#ffffff')
    btn_section.pack(fill='x', pady=20, padx=20)
    
    extract_btn = ttk.Button(btn_section, text="🔓 Ekstrak Pesan", 
                            style='Primary.TButton', command=do_extract)
    extract_btn.pack(pady=10)
    
    back_btn = ttk.Button(btn_section, text="⬅️ Kembali ke Menu", 
                         style='Secondary.TButton', command=show_main_menu)
    back_btn.pack(pady=5)

# Utility function to clear window
def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

# Run GUI
root = tk.Tk()
root.title("LSB Matching Steganography")
root.geometry("650x500")
root.configure(bg='#ecf0f1')
root.resizable(True, True)

# Set window icon and additional properties
try:
    root.iconbitmap('icon.ico')  # Add your icon file if available
except:
    pass

# Setup modern styles
setup_styles()

# Start the application
show_main_menu()
root.mainloop()