# -*- coding: utf-8 -*-
"""The Python implementation of the gRPC client."""
from __future__ import print_function
from google.protobuf import json_format
import grpc
import logging
import obj_pb2     ## or import grpchello_pb2
import obj_pb2_grpc
import random  # 生成随机数
## No grpcDemo!  from grpcDemo import grpchello_pb2, grpchello_pb2_grpc #error!


def run():

# message PubobjRequestData {
  # //设备 ID，全局唯一
  # string deviceNo = 1;
  # //上报时间戳(ms)，1970 纪元后经过 的毫秒数
  # sint64 timestamp = 2;
  # //感知目标列表
  # repeated Object objectList = 3;
# }  
    with grpc.insecure_channel('localhost:50051') as channel:
    
        client = obj_pb2_grpc.StreamServiceStub(channel)
    
    
        # 序列化
        # objectextrainfo = obj_pb2.ObjectExtraInfo()   
        # objectextrainfo.length = 1.0
        # objectextrainfo.width = 1.0
        # objectextrainfo.height = 1.0
        # objectextrainfo.color = 1
        # objectextrainfo.licensePlate = 'name'
        # objectextrainfo.vehicleBrand = 1
        # objectextrainfo.status.append(1)
        
        # object1 = obj_pb2.Object()
        # object1.id = 1;
        # object1.source = 1
        # object1.type = 1
        # object1.lat = 1.0
        # object1.lng = 1.0
        # object1.ele = 1.0
        # object1.roadId = 'name'
        # object1.speed = 1.0
        # object1.heading = 1.0
        # object1.lanes.append(1)
        # object1.extraInfo.length = 1.0
        # object1.extraInfo.width = 1.0
        # object1.extraInfo.height = 1.0
        # object1.extraInfo.color = 1
        # object1.extraInfo.licensePlate = 'name'
        # object1.extraInfo.vehicleBrand = 1
        # object1.extraInfo.status.append(1)
        
        # pubobjrequestdata = obj_pb2.PubobjRequestData()
        # pubobjrequestdata.deviceNo = 'name'
        # pubobjrequestdata.timestamp = 1
        # pubobjrequestdata.objectList.append(object1)
        
        # #print(pubobjrequestdata)
        # #print(pubobjrequestdata.SerializeToString())

        # temp = obj_pb2.PubobjRequestData()
        # temp.ParseFromString(pubobjrequestdata.SerializeToString())
        #print(json_format.MessageToDict(pubobjrequestdata, True))
        
        Coun = 10
        while Coun > 0:
            pubobjrequestdata = obj_pb2.PubobjRequestData()
            # 设备ID，全局唯一
            pubobjrequestdata.deviceNo = 'name'
            # 上报时间戳(ms)，1970 纪元后经过 的毫秒数
            pubobjrequestdata.timestamp = random.randint(1,1000)
            # 感知目标列表     
            object1 = obj_pb2.Object()    
            # 感知目标 ID
            object1.id = random.randint(1,1000)
            # 感知数据来源
            # 0：未知
            # 1：摄像头
            # 2：浮动车上报
            # 3：毫米波雷达
            # 4：激光雷达
            # 5: 毫米波雷达与摄像头融合感知
            # 6: 激光雷达与摄像头融合感知
            object1.source = random.randint(0, 6)
            # 目标类型
            # 0: 不明物体
            # 1: 小汽车
            # 2: 行人
            # 3: 动物
            # 4.:卡车
            # 5: 警车
            # 6: 落石
            # 7: 救护车
            # 8: 道路运维车辆
            # 9: 事故目标
            # 10: 道路施工
            # 11: 抛撒物
            # 12: 自行车
            # 13: 摩托车
            # 14: 公共汽车
            # 15: 交通锥
            # 16: 小雨
            # 17: 大雨
            # 18: 团雾
            object1.type = random.randint(0, 18)
            # 纬度（WGS84坐标）
            object1.lat = random.uniform(1.1, 5.4)
            # 经度（WGS84坐标）
            object1.lng = random.uniform(1.1, 5.4)
            # 海拔（米）
            object1.ele = random.uniform(1.1, 5.4)
            # 道路ID，限定7个字符长度
            object1.roadId = 'name'
            # 行驶速度（km/h）
            object1.speed = random.uniform(0.0, 100.0)
            # 方向角：范围为 0-360 度，正北为 0度，顺时针旋转
            object1.heading = random.uniform(0.00,360.00)
            # 车道编号列表，指物体所处的车道
            # 列表，取值大小的选择
            count = random.randint(1, 5)
            while count > 0:
                object1.lanes.append(random.randint(0, 6))
                count -= 1
            # 目标物体长度   
            object1.extraInfo.length = random.uniform(1.0, 5.0)
            # 目标物体宽度
            object1.extraInfo.width = random.uniform(1.0, 3.0)
            # 目标物体高度
            object1.extraInfo.height = random.uniform(1.0, 3.0)
            # 目标物体颜色，RGB格式
            object1.extraInfo.color = random.randint(0, 7)
            # 车牌号
            object1.extraInfo.licensePlate = 'name'
            # 车辆品牌
            # 0:其他(以下没有则其他) 1:丰田 2:本 田 3:日产 4:别克 5: 雪佛兰 6: 凯迪
            # 拉克 7:克莱斯勒 8:道奇 9:福特 10:林 肯 11:阿斯顿马丁 12:路虎 13:莲花
            # 14:名爵 15:劳斯莱斯 16:五十铃 17:雷克萨斯 18:马自达 19:三菱 20:斯巴鲁
            # 21:铃木 22:雅马哈 23:奥迪 24:宝马25:奔驰 26:迈巴赫 27:欧宝 28:大众
            # 29:阿尔法罗密欧 30:法拉利 31:菲亚特32:依维柯 33:兰博基尼 34:玛莎拉蒂
            # 35:布加迪 36:雪特龙 37:标致 38:雷诺39:斯堪尼亚 40:奇瑞 41:东风 42:吉利
            # 43:长城 44:一汽 45:金杯 46:红旗 47:比亚迪 48:蔚来 49:理想 50:小鹏 51:
            # 恒大 52:捷豹 53:MINI 54:哈弗 55:长 安 56:五菱 57:荣威 58:现代 59:宝骏
            # 60:广汽传祺 61:起亚 62：北汽 63:领 克 64:斯科达 65:捷达 66:英菲尼迪
            # 67:启辰 68:WEY 69:江淮 69:奔腾 70:
            # 斯威 71:JEEP 72:威马 73:观致 74:北京 75:星途 76:讴歌 77:东南 78:福田
            # 79:中华 80:海马 81:江铃 82:大运 83:特斯拉
            object1.extraInfo.vehicleBrand = random.randint(0, 83)
            # 道路目标状态
            # 0: 紧急制动
            # 1: 车辆失控
            # 2: 逆道行驶
            object1.extraInfo.status.append(1)            
            pubobjrequestdata.objectList.append(object1)          
            
            response = client.Pubobj(pubobjrequestdata)
            print("hello client received: ")
            print(response.code)
            Coun -= 1


## 
if __name__ == "__main__":
    logging.basicConfig()
    run()
