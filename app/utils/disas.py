import  subprocess


def disas(file_name):
    subprocess.call(
        ['java', '-jar', 'javalib/apktool_2.5.0.jar', 'd', 'upload_dir/test.apk', '-o', 'upload_dir/tmp', '-f'])


def reassemble(file_name):
    print('f')
    subprocess.call(
        ['java', '-jar', 'javalib/apktool_2.5.0.jar', 'b', 'upload_dir/tmp', '-o', 'upload_dir/test-hacked.apk', '-f'])


def sign(file_name):
    print('f')
    subprocess.call(['java', '-jar', 'javalib/apksigner.jar', 'sign', '--ks', 'javalib/debug.keystore', '--ks-key-alias', 'androiddebugkey', '--ks-pass',  'pass:android', 'upload_dir/test-hacked.apk'], shell=True)
