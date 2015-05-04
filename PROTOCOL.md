#GnomeQQ
**SmartQQ所有GET/POST请求均需要携带 Referer = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'及COOKIE**
##登陆
###二维码方式（手机QQ/安全中心扫描）：  
直接使用[这个](https://github.com/xqin/SmartQQ-for-Raspberry-Pi)代码
###用户名密码登陆：  
直接使用[这个](https://github.com/xqin/PiWebQQ)代码  
##消息获取
+ 定时拉取心跳包  
```
html = http.Post('http://d.web2.qq.com/channel/poll2', (
      ('r', '{{"clientid":"{0}","psessionid":"{1}","key":0,"ids":[]}}'.format(ClientID, PSessionID)),
      ('clientid', ClientID),
      ('psessionid', PSessionID)
    ), Referer)
```   
+ 心跳包状态102，116和0为正常状态，其余状态码为错误码。  
+ 状态102代表暂无消息，不需要任何动作。    
+ 状态116需要更新PTWebQQ值。  
+ 状态0代表有新消息，根据后面的具体参数做相应操作。  
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
##ID及昵称获取
###获取个人信息
GET http://s.web2.qq.com/api/get_self_info2?t=（13位时间戳） 
返回值先检查retcode,retcode=0则读取消息，消息示例：  
{"retcode":0,"result":{"birthday":{"month":2,"year":1994,"day":7},"face":567,"phone":"","occupation":"","allow":3,"college":"","uin":2993078122,"blood":0,"constel":1,"lnick":"小黄鸡","vfwebqq":"588dac747352a8546cffc1cef12cac84d335c063392822fab7022fd5c2660f49917b737eff11764b","homepage":"","vip_info":0,"city":"温哥华","country":"加拿大","personal":"","shengxiao":10,"nick":"小黄鸡","email":"","province":"","account":2993078122,"gender":"male","mobile":""}}  
这里的vfwebqq没有任何作用  
~~###获取vfwebqq码    
GET http://s.web2.qq.com/api/getvfwebqq?ptwebqq=(登陆时获取)&clientid=XXX&psessionid=XXX&t=(13位时间戳)  
返回示例：  
{"retcode":0,"result":{"vfwebqq":"5cf2b148005e4a818b9daba310f90bbde6b0549c8b2e246dd318f0bc5dd159a4f67ff385b95b7096"}}    
（好像登陆的时候已经获取了vfwebqq?)~~  
###获取好友，群，讨论组信息  
0. 使用WEBQQ的函数计算hash值（下面是JS代码，需要翻译为PYTHON）：
```
u = function (x, K) {
                x += "";
                for (var N = [], T = 0; T < K.length; T++) N[T % 4] ^= K.charCodeAt(T);
                var U = ["EC", "OK"],
                    V = [];
                V[0] = x >> 24 & 255 ^ U[0].charCodeAt(0);
                V[1] = x >> 16 & 255 ^ U[0].charCodeAt(1);
                V[2] = x >> 8 & 255 ^ U[1].charCodeAt(0);
                V[3] = x & 255 ^ U[1].charCodeAt(1);
                U = [];
                for (T = 0; T < 8; T++) U[T] = T % 2 == 0 ? N[T >> 1] : V[T >> 1];
                N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
                V = "";
                for (T = 0; T < U.length; T++) {
                    V += N[U[T] >> 4 & 15];
                    V += N[U[T] & 15]
                }
                return V
            }
```
以下各步需要post计算出的hash值:  
hash = u(selfuin,ptwebqq)  
selfuin在上一步的个人信息里  
ptwebqq在cookie里  
另外需要vfwebqq,可用上面删除线的方法获取，也可以在登陆时获取  
  
1. 好友信息：    
POST http://s.web2.qq.com/api/get_user_friends2  
PARAM： r:{"vfwebqq":"XXX","hash":"XXX"}  
RESPONSE EXAMPLE： {"retcode":0,"result":{"friends":[{"flag":0,"uin":1574737440,"categories":0}],"marknames":[],"categories":[],"vipinfo":[{"vip_level":0,"u":1574737440,"is_vip":0}],"info":[{"face":252,"flag":17334848,"nick":"ZerUniverse","uin":1574737440}]}}   
  
2. 群信息：  
POST http://s.web2.qq.com/api/get_group_name_list_mask2  
PARAM： r:{"vfwebqq":"XXX","hash":"XXX"}  
RESPONSE EXAMPLE: {"retcode":0,"result":{"gmasklist":[],"gnamelist":[],"gmarklist":[]}}  
  
3. 讨论组信息：  
GET http://s.web2.qq.com/api/get_discus_list  
PARAM：   
clientid=XXX    
psessionid=XXX  
vfwebqq=XXX  
t=13位时间戳  
RESPONSE:  
{"retcode":0,"result":{"dnamelist":[{"name":"ZZYTEST、QQ提醒、ZerUniver","did":1664044173}]}}  
    
4. 群成员：  
GET http://s.web2.qq.com/api/get_group_info_ext2  
PARAM:  
gcode={G_UIN}  
vfwebqq=XXX  
t=13位时间戳  
RESPONSE：  
检查retcode=0?  
从result->minfo里面拉取uin和昵称  
  
5. 讨论组成员：   
GET http://d.web2.qq.com/channel/get_discu_info  
PARAM:  
did={discussion group id}  
vfwebqq=XXX  
clientid=XXX  
psessionid=XXX  
t=13位时间戳  
  
6. 通过UIN获取QQ号（webqq中用uin来指定对象）：  
GET http://s.web2.qq.com/api/get_friend_uin2?tuin={0}&type=1&vfwebqq={1}  
参数0填对方uin,参数1填vfwebqq  
返回： retcode=0, 真实QQ号在result->account里面
