from zope.interface import implements

from plone.supermodel.utils import ns
from plone.supermodel.parser import IFieldMetadataHandler

from plone.autoform.interfaces import OMITTED_KEY, WIDGETS_KEY, MODES_KEY, ORDER_KEY
from plone.autoform.interfaces import SUPERMODEL_NAMESPACE, SUPERMODEL_PREFIX

class FormSchema(object):
    """Support the form: namespace in model definitions.
    """
    implements(IFieldMetadataHandler)
    
    namespace = SUPERMODEL_NAMESPACE
    prefix = SUPERMODEL_PREFIX
    
    def _add(self, schema, key, name, value):
        tagged_value = schema.queryTaggedValue(key, {})
        tagged_value[name] = value
        schema.setTaggedValue(key, tagged_value)
    
    def _add_order(self, schema, name, direction, relative_to):
        tagged_value = schema.queryTaggedValue(ORDER_KEY, [])
        tagged_value.append((name, direction, relative_to,))
        schema.setTaggedValue(ORDER_KEY, tagged_value)
    
    def read(self, field_node, schema, field):
        name = field.__name__
        
        widget  = field_node.get( ns('widget',  self.namespace) )
        mode    = field_node.get( ns('mode',    self.namespace) )
        omitted = field_node.get( ns('omitted', self.namespace) )
        before  = field_node.get( ns('before',  self.namespace) )
        after   = field_node.get( ns('after',   self.namespace) )

        if widget:
            self._add(schema, WIDGETS_KEY, name, widget)
        if mode:
            self._add(schema, MODES_KEY, name, mode)
        if omitted:
            self._add(schema, OMITTED_KEY, name, omitted)
        if before:
            self._add_order(schema, name, 'before', before)
        if after:
            self._add_order(schema, name, 'after', after)

    def write(self, field_node, schema, field):
        name = field.__name__
        
        widget  = schema.queryTaggedValue(WIDGETS_KEY, {}).get(name, None)
        mode    = schema.queryTaggedValue(MODES_KEY,   {}).get(name, None)
        omitted = schema.queryTaggedValue(OMITTED_KEY, {}).get(name, None)
        order   = [(d,v) for n,d,v in schema.queryTaggedValue(ORDER_KEY,  []) if n == name]
        
        if widget is not None:
            if not isinstance(widget, basestring):
                widget = "%s.%s" % (widget.__module__, widget.__name__)
            field_node.set(ns('widget', self.namespace), str(widget))
            
        if mode is not None:
            field_node.set(ns('mode', self.namespace), str(mode))
        
        if omitted is not None:
            field_node.set(ns('omitted', self.namespace), str(omitted))

        for direction, relative_to in order:
            if direction == 'before':
                field_node.set(ns('before',  self.namespace), relative_to)
            elif direction == 'after':
                field_node.set(ns('after',  self.namespace), relative_to)