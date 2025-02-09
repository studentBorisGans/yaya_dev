import asyncio
import grpc
from fastapi import FastAPI, BackgroundTasks
from concurrent import futures
# from . import write_service_pb2, write_service_pb2_grpc
import write_service_pb2
import write_service_pb2_grpc


app = FastAPI()

# Async Queue for Background Writes
write_queue = asyncio.Queue()

async def process_writes():
    while True:
        write_task = await write_queue.get()
        await write_task()  # Execute the async write function
        write_queue.task_done()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_writes())  # Start background processing

# FastAPI Endpoint
@app.post("/write/")
async def write_data(data: dict, background_tasks: BackgroundTasks):
    async def db_write():
        await asyncio.sleep(2)  # Simulate DB write
        print(f"Written: {data}")

    if data.get("priority"):
        await db_write()
        return {"status": "completed"}
    else:
        await write_queue.put(db_write)
        return {"status": "queued"}

# gRPC Server Implementation
class WriteService(write_service_pb2_grpc.WriteServiceServicer):
    async def WriteData(self, request, context):
        async def db_write():
            await asyncio.sleep(2)  # Simulate DB write
            print(f"Written via gRPC: {request.data}")

        if request.priority:
            await db_write()
            return write_service_pb2.WriteResponse(status="completed")
        else:
            await write_queue.put(db_write)
            return write_service_pb2.WriteResponse(status="queued")

# Run gRPC Server
async def serve():
    server = grpc.aio.server()
    write_service_pb2_grpc.add_WriteServiceServicer_to_server(WriteService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC server started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(serve())
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
