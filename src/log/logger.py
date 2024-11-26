#-*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
LOGNAME='kyclassifier'

 
class LOGGER():
        
    def __new__(cls, *args, **kwargs):
        """实现单例模式确保多次实例化参数不会被清空
        """
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            #  不存在时初始化日志对象
            logger = cls._instance.configure_logger()
            setattr(cls,'logger',logger)
        return cls._instance
    
    def configure_logger(self):
        """
        Function to setup a logger with both file and console handlers.
        """
        log_file = '/opt/kyclassifier/output/kyclassifier.log'

        # Create a custom logger
        logger_1 = logging.getLogger(LOGNAME)
        logger_1.setLevel(logging.DEBUG)

        # Create file handler with RotatingFileHandler
        f_handler = RotatingFileHandler(log_file)
        f_handler.setLevel(logging.DEBUG)

        # Create console handler with StreamHandler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)

        # Create formatter and add it to handlers
        F_formatter = logging.Formatter('%(asctime)s.%(msecs)-3d %(levelname)-8s PID: %(process)d %(name)s: %(message)s')
        C_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        f_handler.setFormatter(F_formatter)
        c_handler.setFormatter(C_formatter)

        # Add handlers to the logger
        logger_1.addHandler(f_handler)
        logger_1.addHandler(c_handler) 

        return logger_1


logger = LOGGER().logger