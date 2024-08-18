# coding=utf-8
import web
import sys, os
import json
import traceback


from Tools import tools

sys.path.append(os.path.abspath('../../src'))
from PyDesktopWebUI import WebApp



reload(sys)
sys.setdefaultencoding('utf-8')

'''
2024年6月29日 py web 后台 by lixin
@version 1.0.0
'''
class index:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        path = tools.commonStatic.pages_path + '/index.html'
        with open(path) as fp:
            return fp.read()


class FileHandler:
    def GET(self, filename):
        path = os.path.join(os.getcwd(), "static", "file", filename)
        tools.log.info("下载文件:%s" %( str(path) ) )
        if os.path.isfile(path):
            with open(path) as fp:
                return fp.read()


class HtmlHandler:
    def GET(self, filename):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        path = tools.commonStatic.pages_path + '/' + filename + '.html'
        tools.log.info("HtmlHandler:%s" %( str(path) ) )
        fpt = ""
        try:
            if os.path.isfile(path):
                with open(path, 'r') as fp:
                    fpt = web.template.Template(fp.read())(filename)
                    return tools.render.layout(fpt)
        except Exception as e:
            tools.log.error(traceback.format_exc())
            return "500 err"
        return "not found"


class ApiHandler:

    def GET(self, fn):
        self.req_type = "GET"
        return self._run_api(fn)

    def POST(self, fn):
        self.req_type = "POST"
        return self._run_api(fn)

    def _run_api(self, fn_name):
        try:
            web.header('content-type', 'text/json;charset=UTF-8')
            fn_name = "_api_" + str(fn_name).strip()
            tools.log.info("req_type=" + self.req_type + " |fn_name=" + fn_name)
            if hasattr(self, fn_name):
                data = web.data()
                tools.log.info("data=" + str(data))
                return getattr(self, fn_name)()
        except Exception as e:
            tools.log.error(traceback.format_exc())
            return tools.returnData.err(msg="错误:{}".format(e))

    def _api_test(self):
        return tools.returnData.ok(msg="调用python方法返回"+os.getcwd() )


    # 读取本地文件
    def _api_read_file(self):
        data = web.data()
        json_data = json.loads(data)
        path = json_data.get("path")
        data =""
        code = 1
        msg = ""
        try:
            with open(path, 'r') as fp:
                data = fp.read()
        except Exception as e:
            tools.log.error(traceback.format_exc())
            msg = str(e)
        return tools.returnData.unknown(code=code, msg=msg, data=data)

    # 选择本地文件 获取文件名和路径
    def _api_select_file(self):
        file_path = tools.tk.openfile()
        data = {}
        code = 1
        msg = ""
        if len(file_path) > 0:
            code = 0
            data = {"file_path": file_path, "base_path": file_path.replace(os.path.basename(file_path), ""), "file_name": os.path.basename(file_path)}
        else:
            msg = "未获取文件"
        return tools.returnData.unknown(code=code, msg=msg, data=data)

    # 保存文件
    def _api_save_file(self):
        data = web.data()
        json_data = json.loads(data)
        path = json_data.get("path")
        data =""
        code = 1
        msg = ""
        try:
            with open(path, 'r') as fp:
                data = fp.read()
        except Exception as e:
            tools.log.error(traceback.format_exc())
            msg = str(e)
        return tools.returnData.unknown(code=code, msg=msg, data=data)


if __name__ == "__main__":
    tools.init_log_file("./log/web.log")
    urls = ('/', 'index',
            '/page/(.*)\.html', 'HtmlHandler',
            '/file/(.*)', 'FileHandler',
            '/api/(.*)', 'ApiHandler')
    WebApp(urls=urls,log=tools.log , fvars = globals()).run(port=8888)

