# -*- coding:utf-8 -*-

import tornado
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.mappcatalog import MAppCatalog as  MCatalog


class InfoPublishHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.template_dir_name = 'tmpl_claslite'
        self.mcat = MCatalog()

    def to_login(self):
        self.redirect('/member/login')
        return (True)

    def get(self, input=''):
        url_arr = input.split('/')
        if input == '':
            self.view_class1()
        elif len(input) == 4:
            self.view_class2(input)
        elif len(input) == 5:
            self.echo_class2(input)
        elif len(url_arr) == 2 and url_arr[1] == 'vip':
            self.view_class2(url_arr[0], 1)

    @tornado.web.authenticated
    def echo_class2(self, input=''):
        '''
        弹出的二级发布菜单
        '''
        fatherid = input[1:]
        self.write(self.format_class2(fatherid))

    @tornado.web.authenticated
    def format_class2(self, fatherid):
        dbdata = self.mcat.get_range2_without_parent(fatherid)
        outstr = '<ul class="list-group">'
        for rec in dbdata:
            outstr += '''
            <a href="/meta/cat_add/{0}" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.uid, rec.name)
        outstr += '</ul>'

        print(outstr)
        return (outstr)

    @tornado.web.authenticated
    def view_class1(self, fatherid=''):
        if self.is_admin():
            pass
        else:
            return False
        dbdata = self.mcat.get_parent_list()
        class1str = ''
        for rec in dbdata:
            class1str += '''
             <a onclick="select('/publish/2{0}');" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.uid, rec.name)

        kwd = {
            'class1str': class1str,
            # 'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('tmpl_claslite/publish/publish.html',
                    kwd=kwd)

    @tornado.web.authenticated
    def view_class2(self, fatherid=''):
        '''
        从第二级分类发布
        :param fatherid:
        :return:
        '''
        if self.is_admin():
            pass
        else:
            return False
        fatherid = fatherid[:2] + '00'
        kwd = {
            'class1str': self.format_class2(fatherid),
            'parentid': '0',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('tmpl_claslite/publish/publish2.html',
                    kwd=kwd)