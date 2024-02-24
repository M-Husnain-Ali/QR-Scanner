import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io

custom_css = """
<style>
h1 {
    color: #ff0070;
    font-family: 'CalligraphyFont', cursive;
    text-align: center;
    margin-bottom: 2rem;
}

button {
    background-color: #ff007f;
    color: white;
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    border: none;
    margin-top: 2rem;
    cursor: pointer;
}

button:hover {
    background-color: #ff0055;
}

.warning-text {
    color: red;
    font-weight: bold;
    margin-top: 1rem;
}

</style>
"""

def generate_fancy_qr_code(data, color, background_color, background_image, gradient_colors):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=color, back_color=background_color)

    if background_image is not None:
        background = Image.open(background_image)
        qr_image = qr_image.resize(background.size)
        qr_image.putalpha(128)
        qr_image = Image.alpha_composite(background.convert("RGBA"), qr_image)

    if gradient_colors:
        qr_image = qr_image.convert("RGBA")
        gradient = Image.new("L", qr_image.size, 0)
        draw = ImageDraw.Draw(gradient)
        for i in range(qr_image.width):
            alpha = int(255 * i / qr_image.width)
            draw.line([(i, 0), (i, qr_image.height)], fill=alpha)
        qr_image.putalpha(gradient)

    img_bytes = io.BytesIO()
    qr_image.save(img_bytes, format='PNG')
    return img_bytes.getvalue()

def main():
    st.set_page_config(page_title="Fancy QR Code Generator", page_icon=":sparkles:")
    st.markdown("<h1>Fancy QR Code Generator</h1>", unsafe_allow_html=True)
    st.write("Generate a fancy QR code for your business!")

    st.markdown(custom_css, unsafe_allow_html=True)

    data = st.text_input("Enter the data for the QR code (e.g., website URL, contact info):")
    color = st.color_picker("Select the QR code color:", "#000000")
    background_color = st.color_picker("Select the QR code background color:", "#FFFFFF")

    background_options = ["Plain Color", "Image"]
    background_choice = st.selectbox("Choose Creative Background:", background_options)

    if background_choice == "Image":
        background_image = st.file_uploader("Upload background image:", type=['jpg', 'jpeg', 'png'])
        if background_image is not None:
            try:
                Image.open(background_image)
            except Exception as e:
                st.warning("Please upload a valid image file.")
                return
    else:
        background_image = None

    gradient_colors = st.checkbox("Apply Gradient Colors")

    generate_button = st.button("Generate Fancy QR Code")

    if generate_button:
        if not data:
            st.warning("Please enter the data for the QR code.")
        else:
            qr_code_bytes = generate_fancy_qr_code(data, color, background_color, background_image, gradient_colors)
            st.image(qr_code_bytes, use_column_width=True, caption="Fancy QR Code")

if __name__ == "__main__":
    main()