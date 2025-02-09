import asyncio
import asyncpg
import grpc
import time #faking DB write
from concurrent import futures
# from . import write_service_pb2, write_service_pb2_grpc
import write_service_pb2
import write_service_pb2_grpc
from grpc_reflection.v1alpha import reflection
from google.protobuf.timestamp_pb2 import Timestamp

# db_pool = None

# async def init_db_pool():
#     """
#     Initialize the PostgreSQL async connection pool.
#     """
#     global db_pool
#     db_pool = await asyncpg.create_pool(
#         dsn="postgresql://user:password@localhost:5432/db_name",  # Adjust DSN
#         min_size=3,  # Min connections
#         max_size=5,  # Max connections
#         timeout=30  # Connection timeout
#     )
#     print("✅ Database connection pool initialized.")

class WriteService(write_service_pb2_grpc.WriteServiceServicer):
    def WriteData(self, request, context):
        """
        Handle database write request.
        """
        
        print(f"Received data: {request.data}")

        write_to_database(request.data)
        return write_service_pb2.WriteResponse(status="Write successful")
    
    def CreateEvent(self, request, context):
        print(f"Received data: {request.data}")

        write_to_database(request.data)
        return write_service_pb2.CreateEventResponse(success=True, message="djdjdj")

def write_to_database(data):
    time.sleep(2)
    print(f"Wrote data: \n{data}")
    print(data.date)
    datetime = data.date.ToDatetime()
    iso = datetime.isoformat() + "Z"
    print(iso)

# Run gRPC Server
def serve():
    # server = grpc.aio.server()
    # write_service_pb2_grpc.add_WriteServiceServicer_to_server(WriteService(), server)
    # server.add_insecure_port("[::]:50051")
    # await server.start()
    # print("gRPC server started on port 50051")
    # await server.wait_for_termination()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # 10 workers for concurrent requests
    write_service_pb2_grpc.add_WriteServiceServicer_to_server(WriteService(), server)
    SERVICE_NAMES = (
        write_service_pb2.DESCRIPTOR.services_by_name['WriteService'].full_name,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")


    # Run the server indefinitely
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()


# Theres a conflict in my setup. In order for my grpc server to work, the code in the generated pb2_grpc.py python file (from proto) needs to import the other generated python file as such: import write_service_pb2 as write__service__pb2. However, my FastAPI endpoint needs to access these files as well to create the stub and channel, as well as accessing the functions.