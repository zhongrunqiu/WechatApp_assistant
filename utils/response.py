#coding:utf-8

#状态码
class ReturnCode:
    SUCCESS = 0
    FAILED = -100
    UNAUTHORIZED = -500
    BROKEN_AUTHORIZED_DATA = -501
    WRONG_PAEMAS = -101
    RESOURCES_NOT_EXISTS = 404
    
    @classmethod
    def message(cls,code):
        if code == cls.SUCCESS:
            return 'success'
        elif code == cls.FAILED:
            return 'failed'
        elif code == cls.UNAUTHORIZED:
            return 'unauthorized'
        elif code == cls.WRONG_PAEMAS:
            return 'wrong parmas'
        else:
            return ''



class CommonResponseMixin():
    @classmethod
    def wrap_json_response(cls,data=None,code=None,message=None):
        """
        Args:
            data:数据
            code:返回状态码
            message:返回消息

        Returns:
            {
                data : {data}
                result_code : 0
                message : 'message'
            }
        """
        response = {}
        if not code:
            code = ReturnCode.SUCCESS
        if not message:
            message = ReturnCode.message(code)
        if data:
            response['data'] = data
        response['result_code'] = code
        response['message'] = message
        return response

def wrap_json_response(data=None,code=None,message=None):
    response = {}
    if not code:
        code = ReturnCode.SUCCESS
    if not message:
        message = ReturnCode.message(code)
    if data:
        response['data'] = data
    response['result_code'] = code
    response['message'] = message
    return response