# -*- coding:utf-8 -*-
import math

import redis

import config
# from torcms.claslite.model.catalog_model import MCatalog
# from torcms.claslite.model.infor_model import MInfor

from torcms.model.mappcatalog import MAppCatalog as  MCatalog
from torcms.model.app_model import MApp as  MInfor
from torcms.core.base_handler import BaseHandler

redisvr = redis.Redis(host='localhost', port=6379, db=0, password=None, socket_timeout=None, connection_pool=None,
                      charset='utf-8', errors='strict', unix_socket_path=None)

'''
关键词过滤，涉及到不同分类，使用  session 来处理。
分类下面的过滤，则使用GET的url的参数。
'''


class InfoListHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.template_dir_name = 'tmpl_claslite'
        self.minfo = MInfor()
        self.mcat = MCatalog()

    def get(self, input=''):
        print(input)

        if len(input) == 4:
            self.list(input)
        elif len(input) > 4:
            self.echo_html(input)
        else:
            self.render('html/404.html', kwd = {})

    def gen_redis_kw(self):
        condition = {}
        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []

        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        if redis_kw:
            condition['keywords'] = kw_condition_arr
        return condition

    def echo_html(self, input):

        condition = self.gen_redis_kw()


        url_arr = input.split('/')
        sig = url_arr[0]

        num = (len(url_arr) - 2) // 2

        if sig.endswith('00'):
            condition['def_cat_pid'] = sig
        else:
            condition['def_cat_uid'] = sig

        fenye_num = 1
        for ii in range(num):
            ckey = url_arr[ii * 2 + 2]

            tval = url_arr[ii * 2 + 3]
            if tval == '0':
                continue
            if ckey == 'fenye':
                # 分页参数。单独处理。
                fenye_num = int(tval)
                continue
            if ckey == 'fabiaoshijian':
                if tval == '1':
                    cval = 1
                elif tval == '2':
                    cval = 2
            else:
                cval = tval
            ckey = 'tag_' + ckey
            condition[ckey] = cval

        print(condition)
        if url_arr[1] == 'con':
            infos = self.minfo.get_list_fenye(condition, fenye_num)
            self.echo_html_list_str(sig, infos)
        elif url_arr[1] == 'num':
            allinfos = self.minfo.get_list(condition)
            self.echo_html_fenye_str(allinfos.count(), fenye_num)

    def echo_html_list_str(self, list_type, infos):
        '''
        生成 list 后的 HTML 格式的字符串
        '''
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguang': tuiguang_str,
        }
        self.render('autogen/infolist/infolist_{1}.html'.format(self.template_dir_name, list_type),
                    kwd=kwd,
                    post_infos=infos,
                    widget_info=kwd)

    def echo_html_fenye_str(self, rec_num, fenye_num):
        '''
        生成分页的导航
        '''
        pagination_num = int(math.ceil(rec_num * 1.0 / 10))

        if pagination_num == 1 or pagination_num == 0:
            fenye_str = ''
        elif pagination_num > 1:
            fenye_str = '<ul class="pagination">'
            for num in range(1, pagination_num + 1):
                if num == fenye_num:
                    checkstr = 'active'
                else:
                    checkstr = ''
                tmp_str_df = '''
                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>{1}</a></li>'''.format(checkstr, num)
                fenye_str += tmp_str_df
            fenye_str += '</ul>'

        else:
            pass
        self.write(fenye_str)

    def list(self, input):
        '''
        页面打开后的渲染方法，不包含 list 的查询结果与分页导航
        '''
        condition = self.gen_redis_kw()

        sig = input

        bread_crumb_nav_str = '当前位置：<a href="/">数据中心</a>'
        bread_crumb_nav_str += ' > '
        if input.endswith('00'):
            parent_id = input
            parent_catname = self.mcat.get_by_id(parent_id).name
            condition['parentid'] = [parent_id]
            catname = self.mcat.get_by_id(sig).name
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(sig, catname)

        else:
            condition['catid'] = [sig]
            parent_id = sig[:2] + '00'
            parent_catname = self.mcat.get_by_id(parent_id).name
            catname = self.mcat.get_by_id(sig).name
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(parent_id, parent_catname)
            bread_crumb_nav_str += ' > '
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(sig, catname)

        num = self.minfo.get_num_condition(condition)


        kwd = {
            'catid': input,
            'daohangstr': bread_crumb_nav_str,
            'parentid': parent_id,
            'parentlist': self.mcat.get_parent_list(),
            'condition': condition,
            'catname': catname,
            'rec_num': num,
        }

        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []
        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        self.render('autogen/list/list_{1}.html'.format(self.template_dir_name, input),
                    kwd=kwd, widget_info=kwd,
                    condition_arr=kw_condition_arr)