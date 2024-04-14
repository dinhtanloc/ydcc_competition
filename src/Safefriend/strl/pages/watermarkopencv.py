import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from PIL import Image,ImageChops


from stegano import lsb

# Function to add watermark overlay to image
def add_watermark_overlay(input_image, watermark_text):
    input_image = input_image.convert('RGBA')
    width, height = input_image.size
    overlay = Image.new('RGBA', input_image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(overlay)

    watermark_color_pattern = (255, 255, 255, 30)

    for i in range(0, width + height, 50):
        draw.line([(0, height - i), (i, height)], fill=watermark_color_pattern, width=5)

    font_size = 80
    font = ImageFont.truetype('arial.ttf', font_size)
    text_width = draw.textlength(watermark_text, font)
    text_height = font_size * 1
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    watermark_color_text = (255, 255, 255, 80)
    draw.text((x, y), watermark_text, fill=watermark_color_text, font=font)

    watermarked_image = Image.alpha_composite(input_image, overlay)

    return watermarked_image

def embed_watermark_with_stegano(image_path, watermark_path, output_path):
        secret = lsb.hide(image_path, watermark_path)
        secret.save(output_path)

# Main function
def page1():
    st.title("Camera Capture with Watermark Overlay")
    st.markdown("# Watermark Basic")
    st.sidebar.markdown("# Watermark Basic")

    # Capture image from camera
    img_file_buffer = st.camera_input("Take a picture")

    # if img_file_buffer is not None:
    #     # Read image file buffer as a PIL Image
    #     img = Image.open(img_file_buffer)

    #     # Add watermark overlay to the image
    #     watermark_text = st.text_input("Enter watermark text:")
    #     watermarked_img = add_watermark_overlay(img, watermark_text)

    #     # Convert watermarked image to numpy array
    #     watermarked_img_array = np.array(watermarked_img)

    #     # Display watermarked image
    #     st.image(watermarked_img_array, channels="RGBA")

    if img_file_buffer is not None:
            
            # Display uploaded image
            image = Image.open(img_file_buffer)
            #st.image(image, caption="Uploaded Image", use_column_width=True)

            # Watermark text input
            watermark_text = st.text_input("Watermark Text", "Hello")

            # Button to add watermark
            if st.button("Watermark"):
                watermarked_image = add_watermark_overlay(image, watermark_text)
                st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

                # Save watermarked image to temporary file
                # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    # watermarked_image.save(temp_file.name)

                # Download button
                from io import BytesIO
                buf = BytesIO()
                watermarked_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Download Watermarked Image",
                    data=byte_im,
                    file_name="watermarked_image.png",
                    mime="image/png",
                )


def page2():
     
    st.title("Camera Capture with Watermark Overlay")
    st.markdown("# Watermark Hidden")
    st.sidebar.markdown("# Watermark Hidden")

    # Capture image from camera
    img_file_buffer = st.camera_input("Take a picture")
    watermark_file = st.file_uploader("Upload Watermark", type=["jpg", "jpeg", "png"])

    if img_file_buffer is not None and watermark_file is not None:
        content1 = img_file_buffer.read()
        content2 = watermark_file.read()

        if st.button("Embed Watermark"):
            # Create temporary files to save the uploaded files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file, \
                tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_watermark_file:
                # Save the uploaded image to a temporary file
                img_file_buffer.seek(0)
                temp_image_file.write(img_file_buffer.read())

                # Save the uploaded watermark to a temporary file
                watermark_file.seek(0)
                temp_watermark_file.write(watermark_file.read())

                # Embed watermark
                embed_watermark_with_stegano(temp_image_file.name, temp_watermark_file.name, "watermarked_image.png")

                # Display watermarked image
                watermarked_image = Image.open("watermarked_image.png")
                st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

                # Download button for watermarked image
                from io import BytesIO
                buf = BytesIO()
                watermarked_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                

                st.download_button(
                    label="Download Watermarked Image",
                    data=byte_im,
                    file_name="watermarked_image.png",
                    mime="image/png",
                )

     
# if __name__ == "__main__":
#     main()

page_names_to_funcs = {
    "Watermark Basic": page1,
    "Watermark Hidden": page2,

}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()