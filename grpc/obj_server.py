# -*- coding: utf-8 -*-
import grpc
import time
import logging
from concurrent import futures 
import obj_pb2, obj_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class gRPCServicerImpl(obj_pb2_grpc.StreamServiceServicer):

    def Pubobj(self, request, context):
        print ("called with " + request.deviceNo)
        
# message PubobjRequestData {
  # //设备 ID，全局唯一
  # string deviceNo = 1;
  # //上报时间戳(ms)，1970 纪元后经过 的毫秒数
  # sint64 timestamp = 2;
  # //感知目标列表
  # repeated Object objectList = 3;
# }        

        return obj_pb2.ResponseData(code = request.timestamp)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  obj_pb2_grpc.add_StreamServiceServicer_to_server(gRPCServicerImpl(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
    serve()