# -*- coding:utf-8 -*-

import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from torcms.model.muser import MUser
import config


class TemplateRendring(object):
    """
    A simple class to hold methods for rendering templates.
    """

    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(self.settings['template_path'])
        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, TemplateRendring):
    def init(self):
        self.tmpl_name = 'tmpl_torlite'
        self.muser = MUser()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def parse_url(self, url_str):
        url_str = url_str.strip()
        url_arr = [] if len(url_str) == 0 else url_str.split('/')
        return url_arr

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def is_admin(self):
        if self.userinfo and self.userinfo.privilege[4] == '1':
            return True
        return False

    def editable(self):
        # Deprecated.
        if self.get_current_user():
            return 1
        else:
            return 0

    def render_jinja2(self, template_name, **kwargs):
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'current_user': self.current_user,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)
