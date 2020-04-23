import os
import sys
from pathlib import Path

import django
from django.conf import settings
from django.template import Context, Template


ROOT = Path(__file__).parent

sys.path.append(str(ROOT.parent.absolute()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.server')
django.setup()
settings.TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [ROOT],
}]


def _install_config(src, dst, filename, context=None):
    template = Template((src / filename).read_text())
    result = template.render(context=Context(context or {}))
    (dst / filename).write_text(result)


def update_conf():
    nginx_dir = Path('/etc/nginx/')
    nginx_conf_dir = nginx_dir / 'sites-enabled/'
    nginx_template_dir = ROOT / 'nginx'

    # Main nginx config
    _install_config(nginx_template_dir, nginx_dir, 'nginx.conf')

    # DH-params
    _install_config(nginx_template_dir, nginx_dir, 'ffdhe2048.dh')

    # App nginx config
    _install_config(nginx_template_dir, nginx_conf_dir, 'project.conf', context={'host': settings.HOST})

    # Supervisor
    _install_config(ROOT, Path('/etc/supervisor/conf.d/'), 'project.conf')


def main():
    update_conf()


if __name__ == '__main__':
    main()
