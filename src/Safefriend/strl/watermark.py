import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from PIL import Image,ImageChops


from stegano import lsb
# from PIL import Image,ImageChops
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

def main_page():
    st.markdown("# Watermark Basic")
    st.sidebar.markdown("# Watermark Basic")

   
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
            
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Watermark text input
            watermark_text = st.text_input("Watermark Text", "Hello")

            # Button to add watermark
            if st.button("Watermark Basic"):
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
                # Remove temporary file
                # os.unlink(temp_file.name)

def embed_watermark_with_stegano(image_path, watermark_path, output_path):
        secret = lsb.hide(image_path, watermark_path)
        secret.save(output_path)


def verify_watermark(original_image_path, extracted_watermark_path):
    original_watermark = Image.open(original_image_path)
    extracted_watermark = Image.open(extracted_watermark_path)
    
    # Kiểm tra sự khác biệt giữa hai watermark
    diff = ImageChops.difference(original_watermark, extracted_watermark)
    
    if diff.getbbox() is None:
        # print("Watermark verified: The image has not been tampered with.")
        return True
    else:
        # print("Watermark verification failed: The image has been tampered with.")
        return False

def page2():
    st.markdown("# Watermark Hidden")
    st.sidebar.markdown("# Watermark Hidden")

    # Upload image and watermark
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    watermark_file = st.file_uploader("Upload Watermark", type=["jpg", "jpeg", "png"])

    if image_file is not None and watermark_file is not None:
        content1 = image_file.read()
        content2 = watermark_file.read()

        if st.button("Embed Watermark"):
            # Create temporary files to save the uploaded files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file, \
                tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_watermark_file:
                # Save the uploaded image to a temporary file
                image_file.seek(0)
                temp_image_file.write(image_file.read())

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

                # Remove temporary files
                # os.unlink(temp_image_file.name)
                # os.unlink(temp_watermark_file.name)

    # def embed_watermark_with_stegano(image_path, watermark_path, output_path):
    #     secret = lsb.hide(image_path, watermark_path)
    #     secret.save(output_path)

    # # Upload image and watermark
    # image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    # watermark_file = st.file_uploader("Upload Watermark", type=["jpg", "jpeg", "png"])

    # if image_file is not None and watermark_file is not None:
    #     if st.button("Embed Watermark"):
    #         # Create a temporary file to save the watermarked image
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
    #             embed_watermark_with_stegano(image_file, watermark_file, temp_file.name)
    #             watermarked_image = Image.open(temp_file.name)
    #             st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

    #             # Download button for watermarked image
    #             st.download_button(
    #                 label="Download Watermarked Image",
    #                 data=temp_file.name,
    #                 file_name="watermarked_image.png",
    #                 mime="image/png",
    #             )

    #             # Remove temporary file
    #             os.unlink(temp_file.name)

def page3():
    st.markdown("# Watermark Verify")
    st.sidebar.markdown("# Watermark Verify")
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    watermark_file = st.file_uploader("Upload Watermark", type=["jpg", "jpeg", "png"])
    if image_file is not None and  watermark_file is not None: 
        check=verify_watermark(image_file,watermark_file)
        if check:
            st.write('Watermark verified: The image has not been tampered with.')
        else:
            st.write('Watermark verification failed: The image has been tampered with.')



             


page_names_to_funcs = {
    "Watermark Basic": main_page,
    "Watermark Hidden": page2,
    "Watermark Verify": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


# def add_watermark_overlay(input_image, watermark_text):
#     input_image = input_image.convert('RGBA')
#     width, height = input_image.size
#     overlay = Image.new('RGBA', input_image.size, (255, 255, 255, 0))

#     draw = ImageDraw.Draw(overlay)

#     watermark_color_pattern = (255, 255, 255, 30)

#     for i in range(0, width + height, 50):
#         draw.line([(0, height - i), (i, height)], fill=watermark_color_pattern, width=5)

#     font_size = 80
#     font = ImageFont.truetype('arial.ttf', font_size)
#     text_width = draw.textlength(watermark_text, font)
#     text_height = font_size * 1
#     x = (width - text_width) // 2
#     y = (height - text_height) // 2

#     watermark_color_text = (255, 255, 255, 80)
#     draw.text((x, y), watermark_text, fill=watermark_color_text, font=font)

#     watermarked_image = Image.alpha_composite(input_image, overlay)

#     return watermarked_image

# ..
# def embed_watermark_with_stegano(image_path, watermark_path, output_path):
#     secret = lsb.hide(image_path, watermark_path)
#     secret.save(output_path)

# # Sử dụng
# # embed_watermark_with_stegano('image/image.png', 'image/watermark_no_copy.png', 'watermarked_image.png')


# def verify_watermark(original_image_path, extracted_watermark_path):
#     original_watermark = Image.open(original_image_path)
#     extracted_watermark = Image.open(extracted_watermark_path)
    
#     # Kiểm tra sự khác biệt giữa hai watermark
#     diff = ImageChops.difference(original_watermark, extracted_watermark)
    
#     if diff.getbbox() is None:
#         print("Watermark verified: The image has not been tampered with.")
#     else:
#         print("Watermark verification failed: The image has been tampered with.")


# def extract_watermark_with_stegano(image_path, output_path):
#     img=Image.open(image_path)
#     watermark = lsb.reveal(img)
#     img_watermark=Image.open(watermark)
#     img_watermark.save(output_path)

# # # Sử dụng
# # extract_watermark_with_stegano('watermarked_image.png', 'extracted_watermark.png')
# verify_watermark('image/watermark_no_copy.png', 'extracted_watermark.png')
# ..

# Streamlit app
# st.markdown("# Image Watermarking")

#selection button

# col1, col2, col3 = st.columns(3)
# with col1:
#     button1 = st.button("Watermark Basic")
# with col2:
#     button2 = st.button("Watermark Hidden")
# with col3:
#     button3 = st.button("Watermark Verify")

# if button1:
    # Upload image
# uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
            
#             # Display uploaded image
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)

#             # Watermark text input
#             watermark_text = st.text_input("Watermark Text", "Hello")

#             # Button to add watermark
#             if st.button("Watermark Basic"):
#                 watermarked_image = add_watermark_overlay(image, watermark_text)
#                 st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

#                 # Save watermarked image to temporary file
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
#                     watermarked_image.save(temp_file.name)

#                 # Download button
#                 st.download_button(
#                     label="Download Watermarked Image",
#                     data=temp_file.name,
#                     file_name="watermarked_image.png",
#                     mime="image/png",
#                 )
#                 # Remove temporary file
#                 os.unlink(temp_file.name)