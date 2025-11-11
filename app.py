from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, SquareGradiantColorMask, RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import io
import base64
import os
import json

app = Flask(__name__)

# Store QR history in memory (in production, use a database)
qr_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        qr_type = data.get('type', 'url')
        content = get_qr_content(data, qr_type)
        
        if not content:
            return jsonify({'error': 'Please provide data'}), 400
        
        # QR Code settings
        error_correction = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'H': qrcode.constants.ERROR_CORRECT_H
        }.get(data.get('errorCorrection', 'M'), qrcode.constants.ERROR_CORRECT_M)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=int(data.get('boxSize', 10)),
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        # Style and color settings
        style = data.get('style', 'square')
        fg_color = data.get('fgColor', '#000000')
        bg_color = data.get('bgColor', '#FFFFFF')
        gradient_type = data.get('gradientType', 'none')
        
        # Generate base QR image - simplified approach
        try:
            if gradient_type != 'none' and style != 'square':
                # Try gradient with style
                module_drawer = None
                if style == 'rounded':
                    module_drawer = RoundedModuleDrawer()
                elif style == 'circle':
                    module_drawer = CircleModuleDrawer()
                elif style == 'gapped':
                    module_drawer = GappedSquareModuleDrawer()
                
                color_mask = None
                if gradient_type == 'linear':
                    color_mask = SquareGradiantColorMask(
                        back_color=bg_color,
                        center_color=fg_color,
                        edge_color=data.get('gradientColor', '#6366f1')
                    )
                elif gradient_type == 'radial':
                    color_mask = RadialGradiantColorMask(
                        back_color=bg_color,
                        center_color=fg_color,
                        edge_color=data.get('gradientColor', '#6366f1')
                    )
                else:
                    color_mask = SolidFillColorMask(back_color=bg_color, front_color=fg_color)
                
                if module_drawer and color_mask:
                    img = qr.make_image(
                        image_factory=StyledPilImage,
                        module_drawer=module_drawer,
                        color_mask=color_mask
                    )
                else:
                    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
            elif style != 'square':
                # Style without gradient
                module_drawer = None
                if style == 'rounded':
                    module_drawer = RoundedModuleDrawer()
                elif style == 'circle':
                    module_drawer = CircleModuleDrawer()
                elif style == 'gapped':
                    module_drawer = GappedSquareModuleDrawer()
                
                if module_drawer:
                    img = qr.make_image(
                        image_factory=StyledPilImage,
                        module_drawer=module_drawer,
                        color_mask=SolidFillColorMask(back_color=bg_color, front_color=fg_color)
                    )
                else:
                    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
            else:
                # Simple square QR code
                img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        except Exception as style_error:
            print(f"Style error, falling back to simple: {str(style_error)}")
            img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        
        # Convert to RGB for additional effects
        img = img.convert('RGB')
        
        # Apply frame if selected
        try:
            frame_style = data.get('frameStyle', 'none')
            if frame_style and frame_style != 'none':
                img = add_frame(img, frame_style, fg_color)
        except Exception as frame_error:
            print(f"Frame error, skipping: {str(frame_error)}")
        
        # Add label if provided
        try:
            label_text = data.get('labelText', '').strip()
            if label_text:
                img = add_label(img, label_text, fg_color)
        except Exception as label_error:
            print(f"Label error, skipping: {str(label_error)}")
        
        # Convert to base64
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=95)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        # Save to history (limit to last 10)
        try:
            qr_history.insert(0, {
                'type': qr_type,
                'content': content[:50] + '...' if len(content) > 50 else content,
                'image': f'data:image/png;base64,{img_base64}'
            })
            if len(qr_history) > 10:
                qr_history.pop()
        except Exception as history_error:
            print(f"History error: {str(history_error)}")
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error generating QR code: {str(e)}")
        print(error_trace)
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def add_frame(img, frame_style, color):
    """Add decorative frame around QR code"""
    try:
        # Convert hex color to RGB tuple
        if isinstance(color, str):
            color = hex_to_rgb(color)
        
        width, height = img.size
        padding = 40
        new_size = (width + padding * 2, height + padding * 2)
        
        framed = Image.new('RGB', new_size, 'white')
        framed.paste(img, (padding, padding))
        
        draw = ImageDraw.Draw(framed)
        
        if frame_style == 'rounded':
            # Draw rounded corners
            corner_radius = 20
            try:
                draw.rounded_rectangle(
                    [(10, 10), (new_size[0] - 10, new_size[1] - 10)],
                    radius=corner_radius,
                    outline=color,
                    width=4
                )
            except AttributeError:
                # Fallback for older Pillow versions
                draw.rectangle(
                    [(10, 10), (new_size[0] - 10, new_size[1] - 10)],
                    outline=color,
                    width=4
                )
        elif frame_style == 'shadow':
            # Add shadow effect
            shadow = Image.new('RGB', new_size, 'white')
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rectangle(
                [(padding + 5, padding + 5), (width + padding + 5, height + padding + 5)],
                fill=(204, 204, 204)
            )
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
            shadow.paste(framed, (0, 0))
            return shadow
        
        return framed
    except Exception as e:
        print(f"Frame error: {str(e)}")
        return img

def add_label(img, text, color):
    """Add text label below QR code"""
    try:
        # Convert hex color to RGB tuple
        if isinstance(color, str):
            color = hex_to_rgb(color)
        
        width, height = img.size
        label_height = 60
        new_size = (width, height + label_height)
        
        labeled = Image.new('RGB', new_size, 'white')
        labeled.paste(img, (0, 0))
        
        draw = ImageDraw.Draw(labeled)
        
        # Try to use a nice font, fallback to default
        font = None
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 24)
                break
            except:
                continue
        
        if not font:
            font = ImageFont.load_default()
        
        # Center the text
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            # Fallback for older Pillow versions
            text_width = len(text) * 12
        
        text_x = max(0, (width - text_width) // 2)
        text_y = height + 20
        
        draw.text((text_x, text_y), text, fill=color, font=font)
        
        return labeled
    except Exception as e:
        print(f"Label error: {str(e)}")
        return img

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({'history': qr_history})

def get_qr_content(data, qr_type):
    if qr_type == 'url':
        return data.get('url', '')
    elif qr_type == 'text':
        return data.get('text', '')
    elif qr_type == 'email':
        email = data.get('email', '')
        subject = data.get('subject', '')
        message = data.get('message', '')
        return f"mailto:{email}?subject={subject}&body={message}"
    elif qr_type == 'phone':
        return f"tel:{data.get('phone', '')}"
    elif qr_type == 'location':
        lat = data.get('lat', '')
        lng = data.get('lng', '')
        location_type = data.get('locationType', 'geo')
        
        if location_type == 'google':
            return f"https://www.google.com/maps?q={lat},{lng}"
        elif location_type == 'apple':
            return f"http://maps.apple.com/?ll={lat},{lng}"
        elif location_type == 'waze':
            return f"https://waze.com/ul?ll={lat},{lng}"
        else:  # geo (default)
            return f"geo:{lat},{lng}"
    elif qr_type == 'wifi':
        ssid = data.get('ssid', '')
        password = data.get('password', '')
        security = data.get('security', 'WPA')
        return f"WIFI:T:{security};S:{ssid};P:{password};;"
    return ''

if __name__ == '__main__':
    app.run(debug=True, port=5001)
