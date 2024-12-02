#-*- coding:utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

from src.utils.config import BaseConfig

 
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
        if not os.path.exists(BaseConfig.LOG_PATH):
            os.makedirs(BaseConfig.LOG_PATH)
            
        log_file = os.path.join(BaseConfig.LOG_PATH, BaseConfig.LOG_FILE_NAME)

        # Create a custom logger
        custom_logger = logging.getLogger(BaseConfig.LOGNAME)
        custom_logger.setLevel(logging.DEBUG)

        # Create file handler with RotatingFileHandler
        f_handler = RotatingFileHandler(log_file)
        f_handler.setLevel(logging.DEBUG)

        # Create formatter and add it to handlers
        F_formatter = logging.Formatter('%(asctime)s.%(msecs)-3d %(levelname)-8s PID: %(process)d %(name)s: %(message)s')
        f_handler.setFormatter(F_formatter)

        # Add handlers to the logger
        custom_logger.addHandler(f_handler)

        return custom_logger

    @classmethod
    def update_console_log(cls, logger):
        """日志输出到控制台
        """

        # Create console handler with StreamHandler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)

        C_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        c_handler.setFormatter(C_formatter)

        logger.addHandler(c_handler)


logger = LOGGER().logger