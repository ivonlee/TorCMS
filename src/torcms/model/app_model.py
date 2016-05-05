# -*- coding:utf-8 -*-

import time
from datetime import datetime

import config
from torcms.core import tools
from torcms.model.ext_tab import *


class MAppBase(object):
    def __init__(self):
        self.tab_app = TabApp
        self.tab_app2catalog = TabApp2Catalog
        try:
            TabApp.create_table()
        except:
            pass

    def get_all(self):
        return (self.tab_app.select().order_by(self.tab_app.view_count))

    def update_jsonb(self, uid, indic):
        entry = self.tab_app.update(
            extinfo = indic,
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)
    def delete(self, del_id):
        try:
            self.tab_app.delete().where(self.tab_app.uuid == del_id)
            return (True)
        except:
            return (False)

    def modify_meta(self, app_id,  data_dic):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        pass

    def modify_init(self, uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        entry = self.tab_app.update(
            update_time=int(time.time()),
            html_path=data_dic['html_path'],
            date=datetime.now(),
            type=data_dic['type'],
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)

    def get_view_count(self, sig):
        try:
            return self.tab_app.get(uid=sig).view_count
        except:
            return False

    def view_count_increase(self, uid):
        equation_info = self.get_by_uid(uid)
        entry = self.tab_app.update(
            view_count=equation_info.view_count + 1,
            run_time=time.time(),
            title=equation_info.title
        ).where(self.tab_app.uid == uid)
        entry.execute()

    def get_run_count(self, sig):
        try:
            return self.tab_app.get(uid=sig).run_count
        except:
            return False

    def run_count_increase(self, uid):

        entry = self.tab_app.update(
            run_count=self.get_run_count(uid) + 1,
        ).where(self.tab_app.uid == uid)
        entry.execute()

    def query_random(self, num=8):
        fn = peewee.fn

        if config.dbtype == 1 or config.dbtype == 3:
            return self.tab_app.select().order_by(fn.Random()).limit(num)

        elif config.dbtype == 2:

            return self.tab_app.select().order_by(fn.Rand()).limit(num)

    def query_most(self, num=8):
        return self.tab_app.select().order_by(self.tab_app.view_count.desc()).limit(num)

    def query_most_by_cat(self, num=8, cat_str=1):
        return self.tab_app.select().join(self.tab_app2catalog).where(self.tab_app2catalog.catalog == cat_str).order_by(
            self.tab_app.view_count.desc()).limit(num)

    def query_least_by_cat(self, num=8, cat_str=1):
        return self.tab_app.select().join(self.tab_app2catalog).where(self.tab_app2catalog.catalog == cat_str).order_by(
            self.tab_app.view_count).limit(num)

    def get_by_keyword(self, par2):
        return self.tab_app.select().where(self.tab_app.title.contains(par2)).order_by(
            self.tab_app.view_count.desc()).limit(20)

    def query_recent(self, num=8):
        return self.tab_app.select().order_by(self.tab_app.run_time.desc()).limit(num)

    def get_by_uid(self, sig):
        try:
            return self.tab_app.get(uid=sig)
        except:
            return False


class MApp(MAppBase):
    def __init__(self):
        self.tab_app = TabApp
        self.tab_app2catalog = TabApp2Catalog
        try:
            TabApp.create_table()
        except:
            pass

    def modify_meta(self, uid, data_dic, extinfo={}):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        cur_info = self.get_by_uid(uid)
        if cur_info:
            entry = self.tab_app.update(
                title=data_dic['title'][0],
                keywords= ','.join([x.strip() for x in data_dic['keywords'][0].split(',')]),
                desc=data_dic['desc'][0],
                update_time=int(time.time()),
                date=datetime.now(),
                cnt_md=data_dic['cnt_md'][0],
                cnt_html=tools.markdown2html(data_dic['cnt_md'][0]),
                # lat=data_dic['lat'][0],
                # lon=data_dic['lon'][0],
                # zoom_max=data_dic['zoom_max'][0],
                # zoom_min=data_dic['zoom_min'][0],
                # zoom_current=data_dic['zoom_current'][0],
                extinfo=extinfo

            ).where(self.tab_app.uid == uid)
            entry.execute()
        else:

            entry = self.add_meta(uid, data_dic, extinfo)
            return entry
        return (uid)

    def query_by_tagname(self, tag_name):

        # condition = {'keywords': {'$elemMatch': {'$eq': tag_name}}}
        condition = {'keywords': [tag_name]}

        return self.tab_app.select().where(self.tab_app.extinfo.contains(condition))

    def get_label_fenye(self, tag_slug, page_num):
        all_list = self.query_by_tagname(tag_slug)

        # 当前分页的记录
        # current_list = all_list[(page_num - 1) * c.info_list_per_page: (page_num) * c.info_list_per_page]
        return (all_list)

    def add_meta(self, uid,  data_dic, extinfo = {}):

            entry = self.tab_app.create(
                uid=uid,
                title=data_dic['title'][0],
                keywords= ','.join([x.strip() for x in data_dic['keywords'][0].split(',')]),
                desc=data_dic['desc'][0],
                update_time=int(time.time()),
                date=datetime.now(),
                cnt_md=data_dic['cnt_md'][0],
                cnt_html=tools.markdown2html(data_dic['cnt_md'][0]),
                extinfo=extinfo,

                # lat=data_dic['lat'][0],
                #lon=data_dic['lon'][0],
                #zoom_max=data_dic['zoom_max'][0],
                #zoom_min=data_dic['zoom_min'][0],
                # zoom_current=data_dic['zoom_current'][0],
            )

    def get_list(self, condition):

        db_data = self.tab_app.select().where(self.tab_app.extinfo.contains(condition))

        return (db_data)


    def get_num_condition(self, con):

        return self.get_list(con).count()

    def modify_init(self, uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        entry = self.tab_app.update(
            update_time=int(time.time()),
            # html_path=data_dic['html_path'],
            date=datetime.now(),
            type=data_dic['type'],
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)

    def addata_init(self, data_dic):
        if self.get_by_uid(data_dic['sig']):
            uu = self.get_by_uid(data_dic['sig'])
            if data_dic['title'] == uu.title and data_dic['desc'] == uu.desc and data_dic['type'] == uu.type:
                pass
            else:
                self.modify_init(data_dic['sig'], data_dic)
        else:
            time_stamp = int(time.time())
            entry = self.tab_app.create(
                uid=data_dic['sig'],
                title=data_dic['title'],
                desc=data_dic['desc'],
                type=data_dic['type'],
                create_time=time_stamp,
                update_time=time_stamp,
                # html_path=data_dic['html_path'],
                cnt_md=data_dic['cnt_md'],
                cnt_html=data_dic['cnt_html'],
                date=datetime.now(),
                memo='',
                lat=43,
                lon=105,
                zoom_max=13,
                zoom_min=8,
                zoom_current=8,
            )


    def get_list_fenye(self, tag_slug, page_num):
        # 所有的记录
        all_list = self.get_list(tag_slug)
        # 当前分页的记录
        # current_list = all_list[(page_num - 1) * c.info_list_per_page: (page_num) * c.info_list_per_page]
        return (all_list)


    def get_cat_recs_count(self, catid):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': [catid]}
    
        db_data = self.tab_app.select().where(self.tab_app.extinfo.contains(condition))
        return db_data.count()