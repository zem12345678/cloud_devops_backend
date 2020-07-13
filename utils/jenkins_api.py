from jenkins import Jenkins
from cloud_devops_backend.settings import JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD

class JenkinsApi:
    def __init__(self):
        self.url = JENKINS_URL
        self.username = JENKINS_USERNAME
        self.password = JENKINS_PASSWORD
        self.server = self.connect()

    def connect(self):
        """
        连接jenkins（实例化jenkins）
        :return:
        """
        server = Jenkins(self.url, username=self.username, password=self.password)
        return server

    def get_next_build_number(self, name):
        """
        获取下一次构建号
        :param name: 任务名称(项目名称)
        :return: "int" number
        """
        return self.server.get_job_info(name)['nextBuildNumber']

    def build_job(self, name, parameters=None):
        """
        构建任务
        :param name: "str" 任务名称
        :param parameters: "dict" 参数
        :return: "int" queue number
        """
        return self.server.build_job(name=name, parameters=parameters)

    def get_build_console_output(self, name, number):
        """
        获取终端输出结果
        :param name: "str" 任务名称
        :param number: "str" 构建号
        :return: "str" 结果
        """
        return self.server.get_build_console_output(name, number)

