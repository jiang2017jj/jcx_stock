# -*- coding = utf-8 -*-


import datetime
import os
import sys
import time
import pytz
from crontab import CronTab
import logging
import logging.config

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# PathProject = os.path.split(rootPath)[0]
# sys.path.append(rootPath)
# sys.path.append(PathProject)


class AutoRunnerHandler():
    def __init__(self):
        self.year = datetime.datetime.now().year
        self.day = datetime.datetime.now().day
        self.minute = datetime.datetime.now().minute
        self.runtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def task_start_timing(self):
        # CronTab类
        my_user_cron = CronTab(user=True)
        my_user_cron.remove_all(comment=sys.argv[8])

        job = my_user_cron.new(command='/usr/local/python3/bin/python3 /var/lib/jenkins/workspace/'
                                       'api_automation_test_master-JU72M6SAEYKDY6SN3LUUPLXPTX3F35MVFZ5'
                                       '7J4JE3I5TJCTRFXHQ/api_test/common/auto_test.py %s %s  >> /var/lib/task/%s.log'
                                       % (sys.argv[3], sys.argv[8], sys.argv[8]))
        job.set_comment(sys.argv[8])
        if sys.argv[2] == 'm':
            _time = '*/%s * * * *' % sys.argv[1]
        elif sys.argv[2] == 'h':
            _time = '%s */%s * * *' % (self.minute, sys.argv[1])
        elif sys.argv[2] == 'd':
            _time = '%s %s */%s * *' % (self.minute, self.hour, sys.argv[1])
        else:
            _time = '%s %s * * */%s' % (self.minute, self.hour, sys.argv[1])

        job.setall(_time)

        my_user_cron.write()

        LogHandler().save_debug_log_to_file_by_logging("task_start_timing添加测试结束时间")

        end_task = CronTab(user=True)

        jobs = end_task.new(command='/usr/local/python3/bin/python3 /var/lib/jenkins/workspace/'
                                    'api_automation_test_master-JU72M6SAEYKDY6SN3LUUPLXPTX3F35MVFZ5'
                                    '7J4JE3I5TJCTRFXHQ/api_test/common/end_task.py %s >> /var/lib/task/%s.log'
                                    % (sys.argv[8], sys.argv[8]))

        jobs.set_comment(sys.argv[8]+"_结束")

        _time = '%s %s %s %s *' % (
            sys.argv[4],
            sys.argv[5],
            sys.argv[6],
            sys.argv[7],
        )
        jobs.setall(_time)

        end_task.write()


    def task_end_timing(self):
        my_user_cron = CronTab(user=True)
        my_user_cron.remove_all(comment=sys.argv[1])
        my_user_cron.remove_all(comment=sys.argv[1]+"_开始")
        my_user_cron.remove_all(comment=sys.argv[1]+"_结束")
        my_user_cron.write()



class TaskHander():

    def __init__(self):
        pass

    def create_task(name, task, task_args, crontab_time, desc):
        pass


    def change_task_status(name, mode):
        pass


    def delete_task(name):
        pass




if __name__ == '__main__':
    # 需要根据具体业务进行完善
    arh = AutoRunnerHandler()
    pass