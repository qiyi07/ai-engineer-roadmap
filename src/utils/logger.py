import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 确保 logs 目录存在
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(
    name: str = "app",
    level: str = "INFO",
    log_to_file: bool = True,
) -> logging.Logger:
    """配置并返回一个带文件轮转和终端输出的 Logger"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # 避免重复添加 Handler（当多次调用时）
    if logger.handlers:
        return logger

    # 1. 终端输出（带颜色风格，便于调试）
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 2. 文件输出（按大小轮转，单文件最大 10MB，保留 3 个备份）
    if log_to_file:
        file_handler = RotatingFileHandler(
            LOG_DIR / "app.log",
            maxBytes=10_485_760,  # 10MB
            backupCount=3,
            encoding="utf-8",
        )
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


# 预置一个全局 logger 实例（供其他模块导入使用）
logger = setup_logger()
