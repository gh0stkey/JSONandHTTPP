# -*- coding:utf-8 -*-
# Auther: Vulkey_Chen
# Blog: gh0st.cn
# Team: MSTSEC

import json,re

from burp import IBurpExtender, ITab
from javax.swing import JPanel,JButton,JTextArea,JScrollPane
from java.awt import BorderLayout

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        print 'JSONP&HTTPP by [Vulkey_Chen]\nBlog: gh0st.cn\nTeam: MSTSEC'
        self._cb = callbacks
        self._hp = callbacks.getHelpers()
        self._cb.setExtensionName('JSONP&HTTPP')
        self.mainPanel = JPanel()
        self.mainPanel.setLayout(BorderLayout())

        self.jsonTextArea = JTextArea(20,0)
        self.jsonTextArea.setLineWrap(True)

        self.dictTextArea = JTextArea()
        self.dictTextArea.setLineWrap(True)

        self.jsonTextWrapper = JPanel()
        self.jsonTextWrapper.setLayout(BorderLayout())
        self.dictTextWrapper = JPanel()
        self.dictTextWrapper.setLayout(BorderLayout())

        self.jsonScrollPane = JScrollPane(self.jsonTextArea)
        self.dictScrollPane = JScrollPane(self.dictTextArea)

        self.jsonTextWrapper.add(self.jsonScrollPane, BorderLayout.CENTER)
        self.dictTextWrapper.add(self.dictScrollPane, BorderLayout.CENTER)

        self.mainPanel.add(self.jsonTextWrapper, BorderLayout.NORTH)
        self.mainPanel.add(self.dictTextWrapper, BorderLayout.CENTER)

        self.beautifyButton_1 = JButton("JSON2HTTPP", actionPerformed=self.onClick1)
        self.beautifyButton_2 = JButton("HTTPP2JSON", actionPerformed=self.onClick2)

        self.buttons = JPanel();
        self.buttons.add(self.beautifyButton_1, BorderLayout.CENTER)
        self.buttons.add(self.beautifyButton_2, BorderLayout.CENTER)

        self.mainPanel.add(self.buttons, BorderLayout.SOUTH)

        self._cb.customizeUiComponent(self.mainPanel)
        self._cb.addSuiteTab(self)

    def onClick1(self, event):
        _jsontext = self.jsonTextArea.getText()
        try:
            _jsontext = json.loads(re.search(r'\({.*?}\)',_jsontext).group().replace('(','').replace(')',''))
        except:
            _jsontext = json.loads(_jsontext)
        self._result = []
        self.dictTextArea.setText('&'.join(self.json2dict(_jsontext)))
        # self.dictTextArea.setText('\n'.join(self.json2dict(_jsontext)))

    def onClick2(self, event):
        _jsontext = self.jsonTextArea.getText()
        _res = []
        for i in _jsontext.split('&'):
            for x in i.split('='):
                _res.append(x)
        self.dictTextArea.setText(json.dumps(dict(zip(_res[0::2],_res[1::2]))))

    def json2dict(self,_jsontext):
        keyValue = ""
        if isinstance(_jsontext, dict):
            for key in _jsontext.keys():
                keyValue = _jsontext.get(key)
                if isinstance(keyValue, dict):
                    self.json2dict(keyValue)
                elif isinstance(keyValue, list):
                    for json_array in keyValue:
                        self.json2dict(json_array)
                else:
                    if type(keyValue) is int or type(keyValue) == long or type(keyValue) == str:
                        self._result.append(str(key) + "=" + str(keyValue))
                    elif type(keyValue) is bool:
                        self._result.append(str(key) + "=" + str(int(keyValue)))
                    elif type(keyValue) == type(None):
                        self._result.append(str(key) + "=" + "")
                    else:
                        self._result.append(str(key) + "=" + keyValue)
        elif isinstance(_jsontext, list):
            for _jsontext_array in _jsontext:
                self.json2dict(_jsontext_array)
        return self._result

    def getTabCaption(self):
        return 'JSONP&HTTPP'

    def getUiComponent(self):
        return self.mainPanel
