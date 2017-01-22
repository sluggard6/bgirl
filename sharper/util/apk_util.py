# -*- coding:utf-8 -*-
import os
from xml.dom import minidom
from luhu_sharper.lib.axmlparser import axmlprinter

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def get_local_apk_info(apk_path):
    to_dir = apk_path[:-4]
    # 解压app
    os.system('rm -rf %s' % (to_dir))
    os.system('unzip %s -d %s' % (apk_path, to_dir))

    #读取app manifest信息
    ap = axmlprinter.AXMLPrinter(open('%s/AndroidManifest.xml' % to_dir, 'rb').read())
    buff = minidom.parseString(ap.getBuff())
    ele = buff.getElementsByTagName("manifest")[0]
    dic = {}
    for k, v in ele.attributes.items():
        dic[k] = v
    ret = dict()
    #填充apk信息
    ret['size'] = os.path.getsize(apk_path)
    ret['package_name'] = dic.get('package', None)
    ret['version_code'] = dic.get('android:versionCode', None)
    ret['version_name'] = dic.get('android:versionName', None)

    os.system('rm -rf %s' % (to_dir))

    return ret

