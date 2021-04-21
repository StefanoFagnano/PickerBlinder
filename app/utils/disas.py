import os
import subprocess

from utils.global_const import DECOMPILED_APK, COMPILED_APK
from utils.utils_func import filename_cutter, create_folder


def disassemble(file):
    create_folder(DECOMPILED_APK)
    name = filename_cutter(file)
    subprocess.call(
        ['java', '-jar', 'javalib/apktool_2.5.0.jar', 'd', 'apk_files/' + file.filename, '-o',
         DECOMPILED_APK+'/' + name + '/', '-f'])


def reassemble(file):
    create_folder(COMPILED_APK)
    name = filename_cutter(file)
    print('f')
    subprocess.call(
        ['java', '-jar', 'javalib/apktool_2.5.0.jar', 'b', 'decompiled_apk/' + name + '/', '-o',
         COMPILED_APK+'/' + name + '.apk', '-f'])


def create_keystore():
    if os.path.isfile('javalib/debug.keystore'):
        print("Key exist")
    else:
        print("Key not exist")
        os.system(
            'keytool -genkey -v  -noprompt -dname "CN=mqttserver.ibm.com, OU=ID, O=IBM, L=Hursley, S=Hants, '
            'C=GB" -keystore javalib/debug.keystore  -storepass android  -alias apksign  -keypass android  -keyalg '
            'RSA -keysize 2048 -validity 10000')


def sign(file):
    print('f')
    name = filename_cutter(file)
    create_keystore()
    os.system(
        'java -jar javalib/apksigner.jar sign --ks javalib/debug.keystore --ks-key-alias apksign --ks-pass '
        'pass:android compiled_apk/'+name+'.apk')
