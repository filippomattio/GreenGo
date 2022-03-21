class Flag():
    flag=False

    def getFlag(self):
        return self.flag

    def SetFlag(self, bool):
        if bool == True:
            self.flag=True
        else:
            self.flag = False
