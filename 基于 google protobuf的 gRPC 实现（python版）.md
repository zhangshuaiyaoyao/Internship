# **基于 google protobuf的 gRPC 实现（python版）** #

## 1. python下protobuf的安装  ##

使用 pip 安装 grpcio 依赖包

    pip install grpcio

## 2. 编译obj.proto文件

### 2.1创建.protobuf文件(以3.道路目标信息接口为例)：

    syntax = "proto3";
    package grpcstream;
    service StreamService {
      rpc Pubobj(PubobjRequestData) returns (ResponseData) {}
    }
    
    message ObjectExtraInfo {
      float length = 1;
      float width = 2;
      float height = 3;
      int32 color = 4;
      string licensePlate = 5;
      int32 vehicleBrand = 6;
      repeated int32 status = 7;
    }
    
    message Object {
      int32 id = 1;
      int32 source = 2;
      int32 type = 3;
      double lat = 4;
      double lng = 5;
      double ele = 6;
      string roadId = 7;
      float speed = 8;
      float heading = 9;
      repeated int32 lanes = 10;
      ObjectExtraInfo extraInfo = 11;
    }
    
    message PubobjRequestData {
      string deviceNo = 1;
      sint64 timestamp = 2;
      repeated Object objectList = 3;
    }
      
    message ResponseData {
      int32 code = 1;
      string msg = 2;
    }

### 2.2对.protobuf文件进行编译

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./obj.proto

得到*obj_pb2.py*和*obj_pb2_grpc.py*文件

### 2.3 创建Server 

	# -*- coding: utf-8 -*-

    import grpc
    import time
    import logging
    from concurrent import futures 
    import obj_pb2, obj_pb2_grpc
    
    
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    

    class gRPCServicerImpl(obj_pb2_grpc.StreamServiceServicer):
    
		# 这里实现我们定义的接口
    	def Pubobj(self, request, context):
    		print ("called with " + request.deviceNo)
    
    # message PubobjRequestData {
      # string deviceNo = 1;
      # sint64 timestamp = 2;
      # repeated Object objectList = 3;
    # }
    
			# 在这里返回 ResponseData，如何返回，返回怎样的数值在这里定义
    		return obj_pb2.ResponseData(code = request.timestamp)
    
    
    def serve():

	  # 这里通过 thread pool 来并发处理server的任务
      server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
      # 将对应的任务处理函数添加到rpc server中
      obj_pb2_grpc.add_StreamServiceServicer_to_server(gRPCServicerImpl(), server)
      # 这里使用的非安全接口，世界gRPC支持TLS/SSL安全连接，以及各种鉴权机制
      # 接口在这里更改
      server.add_insecure_port('[::]:50051')  
      server.start()
      
      try:
    	while True:
      		time.sleep(_ONE_DAY_IN_SECONDS)
      except KeyboardInterrupt:
    	server.stop(0)
    
    if __name__ == '__main__':
    	serve()

### 2.4 创建Client

	# -*- coding: utf-8 -*-
	"""The Python implementation of the gRPC client."""
	from __future__ import print_function
	from google.protobuf import json_format
	import grpc
	import logging
	import obj_pb2     ## or import grpchello_pb2
	import obj_pb2_grpc
	## No grpcDemo!  from grpcDemo import grpchello_pb2, grpchello_pb2_grpc #error!
	
	
	def run():
	
	# message PubobjRequestData {
	  # string deviceNo = 1;
	  # sint64 timestamp = 2;
	  # repeated Object objectList = 3;
	# }  

		# 该处的接口需要与 Server 对应
	    with grpc.insecure_channel('localhost:50051') as channel:
	    
	        client = obj_pb2_grpc.StreamServiceStub(channel)    
	    
	        # 自建输入例子
            # RequestData信息中一共有三种类型
            # 1. message类： class1 = obj_pb2.Class()
            # 2. message中repeated信息： class1.data.append()
            # 3. message嵌套： class1.class2.name = 'name' 暂时不能直接赋值
            # 下面是一个输入测试：
        
	        object1 = obj_pb2.Object()
	        object1.id = 1;
	        object1.source = 1
	        object1.type = 1
	        object1.lat = 1.0
	        object1.lng = 1.0
	        object1.ele = 1.0
	        object1.roadId = 'name'
	        object1.speed = 1.0
	        object1.heading = 1.0
	        object1.lanes.append(1)
	        object1.extraInfo.length = 1.0
	        object1.extraInfo.width = 1.0
	        object1.extraInfo.height = 1.0
	        object1.extraInfo.color = 1
	        object1.extraInfo.licensePlate = 'name'
	        object1.extraInfo.vehicleBrand = 1
	        object1.extraInfo.status.append(1)
	        
	        pubobjrequestdata = obj_pb2.PubobjRequestData()
	        pubobjrequestdata.deviceNo = 'name'
	        pubobjrequestdata.timestamp = 1
	        pubobjrequestdata.objectList.append(object1)
	        
			# 测试输入
	        #print(pubobjrequestdata)
            # 测试输入的序列化
	        #print(pubobjrequestdata.SerializeToString())
			
			# 测试输入的反序列化
	        #temp = obj_pb2.PubobjRequestData()
	        #temp.ParseFromString(pubobjrequestdata.SerializeToString())
	        #print(json_format.MessageToDict(pubobjrequestdata, True))
	     
	
	     	# 通过 Server 中 Pubobj 函数返回 ResponseData
	        response = client.Pubobj(pubobjrequestdata)
		
		# 输出验证
	    print("hello client received: ")
	    print(response.code)
	
	## 
	if __name__ == "__main__":
	    logging.basicConfig()
	    run()


    

## 3. 测试验证
1. 首先执行 obj_server.py 文件

	`python obj_server.py`
1. 接着执行 obj_client.py 文件

    `python obj_server.py`
1. 得到输出
服务端输出为：called with name
客户端输出为：hello client received: 1
与程序内编写一致

## 4. 编写 RequestData 生成程序
	
	import random  # 生成随机数

    # 该程序主要包括两类
    # 1. object1 = obj_pb2.Object()
    # 2. pubobjrequestdata = obj_pb2.PubobjRequestData()
    
    
    # 产生一个 1 到 10 的随机整数:
    # random.randint(1,10)
    # 产生一个 0 到 1 的随机浮点数:
    # random.random()
    # 产生一个 1.1 到 5.4 之间的随机浮点数:
    # random.uniform(1.1, 5.4) 
    # 从序列中随机选取一个元素:
    # random.choice(' ')
    # 生成从 1 到 100 间隔为 2 的随机整数:
    # random.randrange(1,100,2)
    
    
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
    while count > 0
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
    
    
    pubobjrequestdata = obj_pb2.PubobjRequestData()
    # 设备ID，全局唯一
    pubobjrequestdata.deviceNo = 'name'
    # 上报时间戳(ms)，1970 纪元后经过 的毫秒数
    pubobjrequestdata.timestamp = 1
    # 感知目标列表
    pubobjrequestdata.objectList.append(object1)

测试：
在 Client 文件中采用该程序，尝试生成10条输入数据，Client端执行结果为：

	hello client received:
	933
	hello client received:
	791
	hello client received:
	750
	hello client received:
	36
	hello client received:
	910
	hello client received:
	657
	hello client received:
	668
	hello client received:
	728
	hello client received:
	683
	hello client received:
	107

###本文参考博客：
1.[https://blog.csdn.net/maylcc/article/details/103558367?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control](https://blog.csdn.net/maylcc/article/details/103558367?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control "linux 环境下python3 对google 的 protobuf 安装和使用 详解")
2.[https://blog.csdn.net/XiaoYi_Eric/article/details/81674092](https://blog.csdn.net/XiaoYi_Eric/article/details/81674092 "基于google protobuf的gRPC实现(python版)")
3.[https://blog.csdn.net/a464057216/article/details/54932719/?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0.pc_relevant_baidujshouduan&spm=1001.2101.3001.4242](https://blog.csdn.net/a464057216/article/details/54932719/?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0.pc_relevant_baidujshouduan&spm=1001.2101.3001.4242 "69.Protobuf进阶——使用Python操作Protobuf")