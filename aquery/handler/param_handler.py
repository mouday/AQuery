# -*- coding: utf-8 -*-
from aquery.handler.abs_handler import ParamHandlerAbstract


class ParamHandler(ParamHandlerAbstract):
    @classmethod
    def handle_args_data(cls, data, outer_kwargs, *args, **kwargs):

        real_data = None

        args_len = len(args)

        # 获取类数据
        if args_len > 0:
            # 第一个参数可能是类类型
            if isinstance(args[0], type):
                outer_kwargs.setdefault('class_object', args[0])

                if args_len > 1:
                    real_data = args[1]
            else:
                real_data = args[0]

        return data if data else real_data

    @classmethod
    def handle(cls, data, outer_kwargs, *args, **kwargs):
        """
        获取参数 优先级
        data > args[0] > kwargs
        """
        data = cls.handle_args_data(data, outer_kwargs, *args, **kwargs)
        return data if data else kwargs



