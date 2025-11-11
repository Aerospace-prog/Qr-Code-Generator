import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, SquareGradiantColorMask
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import os


class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator Pro")
        self.root.geometry("800x900")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.qr_type = tk.StringVar(value="url")
        self.error_correction = tk.StringVar(value="M")
        self.box_size = tk.IntVar(value=10)
        self.border = tk.IntVar(value=4)
        self.fg_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.style_var = tk.StringVar(value="square")
        self.logo_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎨 QR Code Generator Pro",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # QR Type Selection
        type_frame = tk.LabelFrame(main_frame, text="Select QR Code Type", font=("Helvetica", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        types = [
            ("🔗 URL/Website", "url"),
            ("📝 Plain Text", "text"),
            ("📧 Email", "email"),
            ("📱 Phone Number", "phone"),
            ("📍 Location", "location"),
            ("📇 vCard", "vcard"),
            ("📶 WiFi", "wifi")
        ]
        
        for i, (text, value) in enumerate(types):
            rb = tk.Radiobutton(
                type_frame,
                text=text,
                variable=self.qr_type,
                value=value,
                font=("Helvetica", 10),
                bg="#f0f0f0",
                command=self.update_input_fields
            )
            rb.grid(row=i//4, column=i%4, sticky="w", padx=10, pady=5)
        
        # Input Frame
        self.input_frame = tk.LabelFrame(main_frame, text="Enter Data", font=("Helvetica", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.input_widgets = {}
        self.update_input_fields()
        
        # Customization Frame
        custom_frame = tk.LabelFrame(main_frame, text="Customize QR Code", font=("Helvetica", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        custom_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Style selection
        style_row = tk.Frame(custom_frame, bg="#f0f0f0")
        style_row.pack(fill=tk.X, pady=5)
        tk.Label(style_row, text="Style:", font=("Helvetica", 10), bg="#f0f0f0", width=15, anchor="w").pack(side=tk.LEFT)
        styles = [("Square", "square"), ("Rounded", "rounded"), ("Circle", "circle"), ("Gapped", "gapped")]
        for text, value in styles:
            tk.Radiobutton(style_row, text=text, variable=self.style_var, value=value, bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        # Colors
        color_row = tk.Frame(custom_frame, bg="#f0f0f0")
        color_row.pack(fill=tk.X, pady=5)
        tk.Label(color_row, text="Colors:", font=("Helvetica", 10), bg="#f0f0f0", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Button(color_row, text="Foreground Color", command=self.choose_fg_color, bg="#3498db", fg="white", font=("Helvetica", 9)).pack(side=tk.LEFT, padx=5)
        tk.Button(color_row, text="Background Color", command=self.choose_bg_color, bg="#3498db", fg="white", font=("Helvetica", 9)).pack(side=tk.LEFT, padx=5)
        
        # Logo
        logo_row = tk.Frame(custom_frame, bg="#f0f0f0")
        logo_row.pack(fill=tk.X, pady=5)
        tk.Label(logo_row, text="Logo (optional):", font=("Helvetica", 10), bg="#f0f0f0", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Button(logo_row, text="Choose Logo Image", command=self.choose_logo, bg="#3498db", fg="white", font=("Helvetica", 9)).pack(side=tk.LEFT, padx=5)
        self.logo_label = tk.Label(logo_row, text="No logo selected", font=("Helvetica", 9), bg="#f0f0f0", fg="#7f8c8d")
        self.logo_label.pack(side=tk.LEFT, padx=5)
        
        # Error correction
        ec_row = tk.Frame(custom_frame, bg="#f0f0f0")
        ec_row.pack(fill=tk.X, pady=5)
        tk.Label(ec_row, text="Error Correction:", font=("Helvetica", 10), bg="#f0f0f0", width=15, anchor="w").pack(side=tk.LEFT)
        for text, value in [("Low", "L"), ("Medium", "M"), ("High", "H")]:
            tk.Radiobutton(ec_row, text=text, variable=self.error_correction, value=value, bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        # Size
        size_row = tk.Frame(custom_frame, bg="#f0f0f0")
        size_row.pack(fill=tk.X, pady=5)
        tk.Label(size_row, text="Size:", font=("Helvetica", 10), bg="#f0f0f0", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Scale(size_row, from_=5, to=20, orient=tk.HORIZONTAL, variable=self.box_size, bg="#f0f0f0").pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Generate Button
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=10)
        
        generate_btn = tk.Button(
            btn_frame,
            text="🎯 Generate QR Code",
            command=self.generate_qr,
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            height=2,
            cursor="hand2"
        )
        generate_btn.pack(fill=tk.X)
    
    def update_input_fields(self):
        # Clear existing widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.input_widgets.clear()
        
        qr_type = self.qr_type.get()
        
        if qr_type == "url":
            self.create_input("URL:", "url", "https://example.com")
        elif qr_type == "text":
            self.create_text_input("Text:", "text", "Enter your text here...")
        elif qr_type == "email":
            self.create_input("Email:", "email", "example@email.com")
            self.create_input("Subject:", "subject", "")
            self.create_text_input("Message:", "message", "")
        elif qr_type == "phone":
            self.create_input("Phone Number:", "phone", "+1234567890")
        elif qr_type == "location":
            self.create_input("Latitude:", "lat", "40.7128")
            self.create_input("Longitude:", "lng", "-74.0060")
        elif qr_type == "vcard":
            self.create_input("Name:", "name", "John Doe")
            self.create_input("Phone:", "phone", "+1234567890")
            self.create_input("Email:", "email", "john@example.com")
            self.create_input("Organization:", "org", "")
        elif qr_type == "wifi":
            self.create_input("Network Name (SSID):", "ssid", "MyWiFi")
            self.create_input("Password:", "password", "")
            tk.Label(self.input_frame, text="Security:", font=("Helvetica", 10), bg="#f0f0f0").pack(anchor="w", pady=(5, 0))
            security_var = tk.StringVar(value="WPA")
            self.input_widgets["security"] = security_var
            security_frame = tk.Frame(self.input_frame, bg="#f0f0f0")
            security_frame.pack(anchor="w", pady=5)
            for sec in ["WPA", "WEP", "nopass"]:
                tk.Radiobutton(security_frame, text=sec, variable=security_var, value=sec, bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
    
    def create_input(self, label, key, placeholder=""):
        tk.Label(self.input_frame, text=label, font=("Helvetica", 10), bg="#f0f0f0").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(self.input_frame, font=("Helvetica", 10), width=60)
        entry.insert(0, placeholder)
        entry.pack(fill=tk.X, pady=(0, 5))
        self.input_widgets[key] = entry
    
    def create_text_input(self, label, key, placeholder=""):
        tk.Label(self.input_frame, text=label, font=("Helvetica", 10), bg="#f0f0f0").pack(anchor="w", pady=(5, 0))
        text = tk.Text(self.input_frame, font=("Helvetica", 10), height=4, width=60)
        text.insert("1.0", placeholder)
        text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.input_widgets[key] = text
    
    def choose_fg_color(self):
        color = colorchooser.askcolor(title="Choose Foreground Color", initialcolor=self.fg_color)
        if color[1]:
            self.fg_color = color[1]
    
    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.bg_color)
        if color[1]:
            self.bg_color = color[1]
    
    def choose_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.logo_path = file_path
            self.logo_label.config(text=os.path.basename(file_path), fg="#27ae60")
    
    def get_data(self):
        qr_type = self.qr_type.get()
        
        if qr_type == "url":
            return self.input_widgets["url"].get().strip()
        elif qr_type == "text":
            return self.input_widgets["text"].get("1.0", tk.END).strip()
        elif qr_type == "email":
            email = self.input_widgets["email"].get().strip()
            subject = self.input_widgets["subject"].get().strip()
            message = self.input_widgets["message"].get("1.0", tk.END).strip()
            return f"mailto:{email}?subject={subject}&body={message}"
        elif qr_type == "phone":
            return f"tel:{self.input_widgets['phone'].get().strip()}"
        elif qr_type == "location":
            lat = self.input_widgets["lat"].get().strip()
            lng = self.input_widgets["lng"].get().strip()
            return f"geo:{lat},{lng}"
        elif qr_type == "vcard":
            name = self.input_widgets["name"].get().strip()
            phone = self.input_widgets["phone"].get().strip()
            email = self.input_widgets["email"].get().strip()
            org = self.input_widgets["org"].get().strip()
            return f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nORG:{org}\nEND:VCARD"
        elif qr_type == "wifi":
            ssid = self.input_widgets["ssid"].get().strip()
            password = self.input_widgets["password"].get().strip()
            security = self.input_widgets["security"].get()
            return f"WIFI:T:{security};S:{ssid};P:{password};;"
        
        return ""
    
    def generate_qr(self):
        data = self.get_data()
        
        if not data:
            messagebox.showerror("Error", "Please enter data for the QR code!")
            return
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{self.error_correction.get()}"),
                box_size=self.box_size.get(),
                border=self.border.get(),
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Apply style
            style = self.style_var.get()
            module_drawer = None
            if style == "rounded":
                module_drawer = RoundedModuleDrawer()
            elif style == "circle":
                module_drawer = CircleModuleDrawer()
            elif style == "gapped":
                module_drawer = GappedSquareModuleDrawer()
            
            # Generate image
            if module_drawer:
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=module_drawer,
                    color_mask=SolidFillColorMask(back_color=self.bg_color, front_color=self.fg_color)
                )
            else:
                img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color)
            
            # Add logo if selected
            if self.logo_path:
                img = img.convert('RGB')
                logo = Image.open(self.logo_path)
                
                # Calculate logo size (10% of QR code)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.15)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Add white background to logo
                logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
                logo_bg.paste(logo, (10, 10))
                
                # Paste logo in center
                logo_pos = ((qr_width - logo_size - 20) // 2, (qr_height - logo_size - 20) // 2)
                img.paste(logo_bg, logo_pos)
            
            # Save file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                initialfile="qrcode.png"
            )
            
            if file_path:
                img.save(file_path)
                messagebox.showinfo("Success", f"QR Code generated successfully!\nSaved to: {file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
