from django import template
from django.template.defaultfilters import stringfilter

import markdown
import re

register = template.Library()


@register.filter
def convert_markdown(value):
    return markdown.markdown(value)


@register.filter
def replace(string, args):
    search = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub(search, replace, string)
