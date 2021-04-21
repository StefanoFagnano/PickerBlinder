import hashlib
import os
import pickle
from pathlib import Path
from utils.global_const import APK_FOLDER, ALLOWED_APK, COMPILED_APK, INJECTIONS


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def create_folder(folder_name):
    APP_ROOT = get_project_root()
    target_decompiled = os.path.join(APP_ROOT, folder_name)

    if not os.path.isdir(target_decompiled):
        os.mkdir(target_decompiled)


def is_apk(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_APK


def get_injection(injection):
    injection_name = next(item for item in INJECTIONS if item['code'] == injection)
    print(injection_name['name'])
    return injection_name


def generate_name(file):
    file_name = APK_FOLDER + '/' + file.filename
    hashName = hashlib.md5(open(file_name, 'rb').read()).hexdigest()
    os.rename(file_name, APK_FOLDER + '/' + hashName + '.apk')
    name = hashName + '.apk'
    return name


def save_apk(file):
    create_folder('apk_files')

    file.save(os.path.join("apk_files", file.filename))
    return file


def filename_cutter(file):
    ext = file.filename[:file.filename.find(".")]
    return ext


def do_json(message, file, injection):
    path = COMPILED_APK + '/' + file.filename
    if os.path.exists(path):
        content = {
            'message': message,
            'filename': file.filename,
            'file_path': "{0}".format(path),
            'injection': get_injection(injection)

        }
        result = content
        return result


def string_to_list(string, delimiter):
    li = list(string.split(delimiter))
    return li


def open_file(filepath):
    opened_file = open(filepath)
    return opened_file.read()
