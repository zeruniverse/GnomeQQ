#GnomeQQ
**SmartQQ所有GET/POST请求均需要携带 Referer = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'**
##登陆
###二维码方式（手机QQ/安全中心扫描）：  
直接使用https://github.com/xqin/SmartQQ-for-Raspberry-Pi代码
###用户名密码登陆：  
直接使用https://github.com/xqin/PiWebQQ代码  
##消息获取
+ 定时拉取心跳包  
```
html = http.Post('http://d.web2.qq.com/channel/poll2', (
      ('r', '{{"clientid":"{0}","psessionid":"{1}","key":0,"ids":[]}}'.format(ClientID, PSessionID)),
      ('clientid', ClientID),
      ('psessionid', PSessionID)
    ), Referer)
```   
心跳包状态102，116和0为正常状态，其余状态码为错误码。  
状态102代表暂无消息，不需要任何动作。    
状态116需要更新PTWebQQ值。  
状态0代表有新消息，根据后面的具体参数做相应操作。  
```
if ret['retcode'] == 102:#无消息
      continue
    if ret['retcode'] == 116:#更新PTWebQQ值
      PTWebQQ = ret['p']
      continue
    if ret['retcode'] == 0:
      for msg in ret['result']:
        msgType = msg['poll_type']
        if msgType == 'message':#QQ消息
          txt = msg['value']['content'][1]
          logging.debug("QQ Message:" + txt)
          if txt[0] == '#':
              thread.start_new_thread(runCommand, (txt[1:].strip(), msg['value']['from_uin']))
          if txt[0:4] == 'exit':
              http.Get('http://d.web2.qq.com/channel/logout2?ids=&clientid={0}&psessionid={1}'.format(ClientID, PSessionID), Referer)
              exit()
        elif msgType == 'sess_message':#QQ临时会话的消息
          logging.debug(msg['value']['content'][1])
        elif msgType == 'group_message':#群消息
          txt = msg['value']['content'][1]
          logging.debug("Group Message:" + txt)
        elif msgType == 'discu_message':#讨论组的消息
          txt = msg['value']['content'][1]
          logging.debug("Discu Message:" + txt)
        elif msgType == 'kick_message':
          logging.error(msg['value']['reason'])
          exit()
        elif msgType != 'input_notify':
          logging.debug(msg)
```  
##消息回复  
**返回retcode=0代表发送成功**
###好友消息  
```
reqURL = "http://d.web2.qq.com/channel/send_buddy_msg2"
        data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":"{1}", "msg_id":{2}, "psessionid":"{3}"}}'.format(tuin, ClientID, msgId, PSessionID, str(content))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, Referer)
        rspp = json.loads(rsp)
```
**clientID和psessionID从登陆时获得**
###临时对话（来自群或讨论组）
```
 reqURL = "http://d.web2.qq.com/channel/send_sess_msg2"
 data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":"{1}", "msg_id":{2}, "psessionid":"{3}", "group_sig":"{5}", "service_type":{6}}}'.format(tuin, ClientID, msgId, PSessionID, str(content), group_sig, service_type)),
            ('clientid', ClientID),
            ('psessionid', PSessionID),
            ('group_sig', group_sig),
            ('service_type',service_type)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, Referer)
        rspp = json.loads(rsp)
```
这里的service_type指定来自讨论组或群（0表示群，1表示讨论组）  
group_sig需要获取：   
```
info = json.loads(HttpClient_Ist.Get('http://d.web2.qq.com/channel/get_c2cmsg_sig2?id={0}&to_uin={1}&clientid={2}&psessionid={3}&service_type={4}&t={5}'.format(myid, tuin, ClientID, PSessionID, service_type, ts), Referer))
```
代码中的ts为当前时间的**13位**时间戳  
###群消息  
```
reqURL = "http://d.web2.qq.com/channel/send_qun_msg2"
        data = (
            ('r', '{{"group_uin":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":"{1}","msg_id":{2},"psessionid":"{3}"}}'.format(self.guin, ClientID, msgId, PSessionID, content.replace("\\", "\\\\\\\\"))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, Referer)
```
其中group_uin为群id  
###讨论组消息
```
reqURL = "http://d.web2.qq.com/channel/send_discu_msg2"
data = (
            ('r', '{{"did":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":"{1}","msg_id":{2},"psessionid":"{3}"}}'.format(self.guin, ClientID, msgId, PSessionID, content.replace("\\", "\\\\\\\\"))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
rsp = HttpClient_Ist.Post(reqURL, data, Referer)
```
其中did为讨论组id  
