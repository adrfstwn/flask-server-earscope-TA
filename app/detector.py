from earscope_model.model import EarScopeModel

# Inisialisasi model
model = EarScopeModel()

def process_frame_with_model(image_data):
    """
    Fungsi untuk memproses frame menggunakan model.
    :param image_data: Gambar dalam format Base64.
    :return: Gambar hasil proses dalam format Base64.
    """
    print("Processing frame...")
    return model.process_image(image_data)