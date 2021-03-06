# -*- coding:utf-8 -*-


import datetime

import tornado.escape

from torcms.core import tools
from torcms.model.core_tab import CabReply, CabVoter2Reply


class MReply():
    def __init__(self):
        try:
            CabReply.create_table()
        except:
            pass

    def add_one(self):
        pass

    def update_vote(self, reply_id, count):

        entry = CabReply.update(
            vote=count
        ).where(CabReply.uid == reply_id)

        entry.execute()

    def update(self, uid, post_data, update_time=False):

        if 'id_spec' in post_data:
            id_spec = post_data['id_spec'][0]
        else:
            id_spec = 0

        if 'src_type' in post_data and post_data['src_type'][0] == '1':
            cnt_html = tools.rst2html(post_data['cnt_md'][0])
        else:
            cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        if update_time:
            entry = CabReply.update(
                title=post_data['title'][0],
                date=datetime.datetime.now(),
                cnt_html=cnt_html,
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                time_update=tools.timestamp(),
                id_spec=id_spec,
                logo=post_data['logo'][0],
                keywords=post_data['keywords'][0],
                src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
            ).where(CabReply.uid == uid)
        else:
            entry = CabReply.update(
                title=post_data['title'][0],
                cnt_html=cnt_html,
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                id_spec=id_spec,
                logo=post_data['logo'][0],
                keywords=post_data['keywords'][0],
                src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
            ).where(CabReply.uid == uid)
        entry.execute()

    def insert_data(self, post_data):

        uid = tools.get_uuid()
        try:
            CabReply.create(
                uid=uid,
                user_name=post_data['user_name'],
                create_user_id=post_data['user_id'],
                timestamp=tools.timestamp(),
                date=datetime.datetime.now(),
                cnt_md=post_data['cnt_md'][0],
                cnt_html=tools.markdown2html(post_data['cnt_md'][0]),
                vote=0,
            )
            return (uid)
        except:
            return False

    def get_reply_by_uid(self, reply_id):
        rec = CabReply.get(CabReply.uid == reply_id)
        return rec

    def get_by_zan(self, reply_id):
        return CabVoter2Reply.select().where(CabVoter2Reply.reply_id == reply_id).count()
