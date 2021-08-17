from django import template


register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def filter_class(field, cls_prefix):
    """Удаляет из словаря с атрибутами для тега все классы, кроме начинающихся
    с префикса cls_prefix.
    """
    attrs = field.get("attrs")
    if attrs:
        _class = attrs.get("class")
        if _class:
            classes = " ".join(c.replace(cls_prefix, "")
                               for c in _class.split()
                               if c.startswith(cls_prefix))
            field["attrs"]["class"] = classes
    return field
