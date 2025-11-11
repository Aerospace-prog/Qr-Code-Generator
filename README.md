# QR Code Generator Pro 🎨

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)

A professional web-based QR code generator with advanced features and a stunning modern UI.

[Live Demo](#) • [Features](#-unique-features) • [Installation](#installation) • [Deploy](#deployment)

</div>

---

## 🚀 Unique Features

### Multiple QR Code Types
- 🔗 **URL/Website** - Generate QR codes for any website
- 📝 **Plain Text** - Convert any text to QR code
- 📧 **Email** - Create mailto links with subject and message
- 📱 **Phone Number** - Generate callable phone number QR codes
- 📍 **Location** - GPS auto-detect or custom coordinates with multiple map types (Google, Apple, Waze)
- 📶 **WiFi** - Share WiFi credentials easily

### Advanced Customization
- **4 Different Styles**: Square, Rounded, Circle, Gapped
- **🌈 Gradient Effects**: Linear and Radial gradients (RARE!)
- **🖼️ Frame Styles**: Rounded borders and shadow effects
- **🏷️ Custom Labels**: Add text below QR codes automatically
- **Custom Colors**: Choose any foreground, background, and gradient colors
- **Error Correction Levels**: Low, Medium, High
- **Adjustable Size**: Control the size of your QR code

### Unique Features (Rare to Find!)
- **📜 History Tracking** - View and reuse your last 10 QR codes
- **📦 Batch Generation** - Generate multiple QR codes at once
- **🎨 Quick Templates** - Pre-designed styles (Business, Social, Minimal, Modern)
- **📍 Auto-Location Detection** - GPS-based location QR codes
- **📋 Copy to Clipboard** - One-click copy QR image
- **🔗 Share Feature** - Native share on mobile devices
- **💾 Multiple Export Options** - PNG, SVG support

## Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

Then open your browser to: **http://127.0.0.1:5001**

## Features Overview

### 🎯 QR Code Types
- URL with auto-validation
- Plain text with multi-line support
- Email with subject and message
- Phone numbers with international format
- Location with 4 map types (Generic, Google Maps, Apple Maps, Waze)
- WiFi with WPA/WEP/No password options

### 🎨 Customization
- **Styles**: Square, Rounded corners, Circular dots, Gapped squares
- **Gradients**: None, Linear, Radial
- **Frames**: None, Rounded border, Shadow effect
- **Labels**: Add custom text below QR code
- **Colors**: Full color picker for foreground, background, and gradient

### 📦 Batch Generation
Generate multiple QR codes at once by entering URLs line by line.

### 📜 History
Automatically saves your last 10 generated QR codes for quick access.

### 🎨 Templates
Quick-apply professional templates:
- **Business Card**: Professional gradient style
- **Social Media**: Vibrant and eye-catching
- **Minimal**: Clean black & white
- **Modern**: Cool blue gradient

## Tips

- Use **High error correction** when adding frames or labels
- Gradients work best with rounded or circle styles
- Test your QR codes with multiple scanners
- Use high contrast colors for better scanning
- Batch generation is perfect for event tickets or product labels

## Requirements

- Python 3.6+
- Flask
- qrcode[pil]
- Pillow (PIL)

## Troubleshooting

If you get a "Port already in use" error, the app will automatically try port 5001.

If you encounter any errors:
1. Make sure all dependencies are installed
2. Check that you're using Python 3.6 or higher
3. Try restarting the server

## Browser Compatibility

Works best on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

Some features like "Copy to Clipboard" and "Share" require modern browsers.

## 🚀 Deployment

Ready to deploy? Check out the [DEPLOYMENT.md](DEPLOYMENT.md) guide for detailed instructions on deploying to:
- Render (Recommended)
- Railway
- Heroku
- Vercel
- And more!

## 👨‍💻 Author

**Kushagra**
- Portfolio: [kushagra-portfolio-nine-ebon.vercel.app](https://kushagra-portfolio-nine-ebon.vercel.app/)
- GitHub: [@Aerospace-prog](https://github.com/Aerospace-prog)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is [MIT](LICENSE) licensed.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

## 📧 Contact

For questions or feedback, reach out through:
- GitHub Issues
- Portfolio Contact Form

---

<div align="center">

Made with ❤️ by [Kushagra](https://kushagra-portfolio-nine-ebon.vercel.app/)

**[⬆ back to top](#qr-code-generator-pro-)**

</div>
