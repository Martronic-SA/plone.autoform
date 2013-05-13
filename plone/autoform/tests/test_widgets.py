import unittest2 as unittest
from plone.testing.zca import UNIT_TESTING


class TestParameterizedWidget(unittest.TestCase):

    layer = UNIT_TESTING

    def test_widget_instantiated_with_parameters(self):
        from zope.interface import implementer
        from zope.schema import Field
        from z3c.form.interfaces import IFieldWidget
        from z3c.form.interfaces import IWidget
        from plone.autoform.widgets import ParameterizedWidget

        @implementer(IWidget)
        class DummyWidget(object):
            def __init__(self, request):
                self.request = request

        @implementer(IFieldWidget)
        def DummyFieldWidget(field, request):
            return DummyWidget(request)

        field = Field()
        request = object()
        widget = ParameterizedWidget(DummyWidget, foo='bar')(field, request)

        self.assertIsInstance(widget, DummyWidget)
        self.assertEqual('bar', widget.foo)

    def test_default_widget_instantiated(self):
        from zope.component import provideAdapter
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.schema import Field
        from z3c.form.interfaces import IFieldWidget
        from plone.autoform.widgets import ParameterizedWidget

        class DummyWidget(object):
            def __init__(self, request):
                self.request = request

        @implementer(IFieldWidget)
        def DummyFieldWidget(field, request):
            return DummyWidget(request)

        provideAdapter(DummyFieldWidget, (Interface, Interface), IFieldWidget)
        
        field = Field()
        request = object()
        widget = ParameterizedWidget(foo='bar')(field, request)

        self.assertIsInstance(widget, DummyWidget)
        self.assertEqual('bar', widget.foo)        

    def test_validates_for_field_widget(self):
        from plone.autoform.widgets import ParameterizedWidget

        class NotAWidget(object):
            pass

        with self.assertRaises(TypeError):
            x = ParameterizedWidget(NotAWidget)