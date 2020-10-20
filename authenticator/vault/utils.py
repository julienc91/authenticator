# -*- coding: utf-8 -*-


class SingletonMetaClass(type):
    def __init__(cls, name, bases, *args, **kwargs):
        super(SingletonMetaClass, cls).__init__(name, bases, *args, **kwargs)
        base_new = cls.__new__

        def singleton_new(cls_, *args, **kwds):
            if cls_.instance is None:
                cls_.instance = base_new(cls_, *args, **kwds)
            return cls_.instance

        cls.instance = None
        cls.__new__ = staticmethod(singleton_new)
