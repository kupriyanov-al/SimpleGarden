import datetime

class MsgSendTime:
    def __init__(self) -> None:
        self._mesOld = {}

    def __comparemes(self, mesnew):
        if self._mesOld != mesnew:
            self._mesOld = mesnew.copy()
            return False
        return True

    def timeStampMsg(self, mesnew):

        if self.__comparemes(mesnew) != True:

            now = datetime.datetime.now()
            mesnew["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            return mesnew
        return False


class ParamSetup:
    def __init__(self) -> None:
        self._msgParam = {
            'temp_on': "25",
            'temp_delta': "0.2",
            'timeRele': "21:00",
            'timeReleWork': "30"
        }

    @property
    def temp_on(self):
        return self._msgParam['temp_on']

    @temp_on.setter
    def temp_on(self, x):
        self._msgParam['temp_on'] = x

    @property
    def temp_delta(self):
        return self._msgParam['temp_delta']

    @temp_delta.setter
    def temp_delta(self, x):
        self._msgParam['temp_delta'] = x

    @property
    def timeRele(self):
        return self._msgParam['timeRele']

    @timeRele.setter
    def timeRele(self, x):
        self._msgParam['timeRele'] = x

    @property
    def timeReleWork(self):
        return self._msgParam['timeReleWork']

    @timeReleWork.setter
    def timeReleWork(self, x):
        self._msgParam['timeReleWork'] = x

    @property
    def msgParam(self):
        return self._msgParam

    @msgParam.setter
    def msgParam(self, x):
        self._msgParam = x



