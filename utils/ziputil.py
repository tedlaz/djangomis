import zipfile
from io import BytesIO


def create_zip(txt_data, zip_filename, filename='JL10', encoding='CP1253'):
    with zipfile.ZipFile(zip_filename, 'w') as file:
        file.writestr(filename, txt_data.encode(encoding))


def create_zip_stream(txt_data, filename='JL10', encoding='CP1253'):
    stream = BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as fil:
        fil.writestr(filename, txt_data.encode(encoding))
    return stream
