# -*- coding: utf-8 -*-
"""
    lib/error.py
    ~~~~~~~~~~~~~~

    自定义error
    :date:2013-01-28
"""

__authors__ = ['"linnchord gao" <linnchord@gmail.com>']


class ErrorCode:
    Debug = 0
    Info = 1
    Warn = 2
    Error = 3


class AppError(Exception):
    """
    统一应用错误对象，返回错误编码和消息
    """
    def __init__(self, msg="you've got a error!", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg


class ParaValidateFailError(AppError):
    """
    参数验证失败
    """
    pass


class UploadFailedError(AppError):
    """
    上传失败
    """
    pass


class UploadTypeError(AppError):
    """
    上传数据类型错误
    """
    pass


class WrongParamError(AppError):
    """
    参数错误
    """
    pass


class AuthFailedError(AppError):
    """
    授权认证失败
    """
    def __init__(self, msg=u"授权认证失败，请确认或稍后再尝试。", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg


class OAuthError(AppError):
    """
    开放认证授权错误
    """
    def __init__(self, msg=u"开放平台授权认证失败，请确认或稍后再尝试。", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg


class ExceedLimitError(AppError):
    """
    超过逻辑上限错误
    """
    pass


class DuplicatedValueError(AppError):
    """
    逻辑值重复错误
    """
    pass


class WrongOperationError(AppError):
    """
    操作错误
    """
    def __init__(self, msg=u"操作错误，请确认或稍后再尝试。", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg


class BusinessLogicError(AppError):
    """
    商务逻辑错误
    """
    pass


class UnsupportedFormatError(AppError):
    """
    格式不支持错误
    """
    pass


class SqlObjError(AppError):
    """
    sql对象错误
    """
    pass


class ResourceNotFoundError(AppError):
    """
    未找到资源错误
    """
    def __init__(self, msg=u"未找到指定资源或已经过期销毁。", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg


class ResourceExpireError(AppError):
    """
    资源已经过期
    """
    def __init__(self, msg=u"指定资源已经过期", code=ErrorCode.Warn):
        self.code = code
        self.msg = msg
