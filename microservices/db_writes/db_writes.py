import asyncio
import mysql.connector

import grpc
import time #faking DB write
from concurrent import futures
# from . import write_service_pb2, write_service_pb2_grpc
import write_service_pb2
import write_service_pb2_grpc
from grpc_reflection.v1alpha import reflection
from google.protobuf.timestamp_pb2 import Timestamp

def write_to_db(query: str, *values):
    try:
        connection = mysql.connector.connect(
            user="root",
            password="Root1234",
            host="localhost",
            database="yaya_dev"
        )
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print("Data inserted successfully.")

        # Return the last inserted row ID
        return cursor.lastrowid

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()
        print("\nConnection closed")

class WriteService(write_service_pb2_grpc.WriteServiceServicer):
    def WriteData(self, request, context):
        print(f"Received data: {request.data}")

        write_to_database(request.data)
        return write_service_pb2.WriteResponse(status="Write successful")
    
    def CreateEvent(self, request, context):
        print(f"Received data: {request.data}")
        try:
            datetime = request.data.date.ToDatetime()
            iso = datetime.isoformat() + "Z"
            mysql_datetime = datetime.fromisoformat(iso.replace('T', ' ').replace('Z', '')).strftime('%Y-%m-%d %H:%M:%S')
            query = """
                INSERT INTO event_data (organizer_id, venue_id, published, tagged, event_name, date, budget, pre_event_poster, pre_bio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (
                request.data.org_id,
                request.data.venue_id,
                request.data.published,
                request.data.tagged_bool,
                request.data.name,
                mysql_datetime,
                request.data.budget,
                request.data.pre_event_poster,
                request.data.pre_bio
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEventResponse(success=False, message="DB Error")

            # write_to_database(request.data)
            return write_service_pb2.CreateEventResponse(success=True, message="djdjdj")
        except Exception as e:
            print(f"Error writing to DB: {e}")
            return write_service_pb2.CreateEventResponse(success=False, message=e)


def write_to_database(data):
    time.sleep(2)
    print(f"Wrote data: \n{data}")
    print(data.date)
    datetime = data.date.ToDatetime()
    iso = datetime.isoformat() + "Z"
    print(iso)

# Run gRPC Server
def serve():
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
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()


# Theres a conflict in my setup. In order for my grpc server to work, the code in the generated pb2_grpc.py python file (from proto) needs to import the other generated python file as such: import write_service_pb2 as write__service__pb2. However, my FastAPI endpoint needs to access these files as well to create the stub and channel, as well as accessing the functions.