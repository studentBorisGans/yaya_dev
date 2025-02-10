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

GENDER_MAP = {0: "Male", 1: "Female", 2: "Other"}
SPEND_CLASS_MAP = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

def write_to_db(query: str, *values):
    print("HereweeeS")
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            user="root",
            password="Root1234",
            host="localhost",
            database="yaya_dev"
        )
        cursor = connection.cursor()

        # return None

        cursor.execute(query, values)
        connection.commit()
        print("Data inserted successfully.")

        # if cursor.with_rows:
        #     cursor.fetchall()
        # Return the last inserted row ID
        return cursor.lastrowid
    

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        # return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
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
                return write_service_pb2.CreateEntityResponse(success=False, message="DB Error")

            # write_to_database(request.data)
            return write_service_pb2.CreateEntityResponse(success=True, message="djdjdj")
        except Exception as e:
            print(f"Error writing to DB: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=e)
    
    def CreateUser(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO user_data (
                username, first_name, last_name, email, location, language, gender, age, spend_class, music_service, pw
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            values = (
                request.data.username,
                request.data.first_name,
                request.data.last_name,
                request.data.email,
                request.data.location,
                request.data.language,
                GENDER_MAP[request.data.gender],  # Should be stored as an integer
                request.data.age,
                SPEND_CLASS_MAP.get(request.data.spend_class, None),
                int(request.data.music_service),  # Convert bool to int (1 or 0)
                request.data.pw,
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEntityResponse(success=False, message="DB Error")

            # write_to_database(request.data)
            return write_service_pb2.CreateEntityResponse(success=True, message="user created")
        except Exception as e:
            print(f"Error writing to DB: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=e)
        
    def CreateDj(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO dj (
                dj_name, first_name, last_name, bio, location, email, phone
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            """
            # query = """
            # INSERT INTO dj (
            #     dj_name, first_name, last_name, bio, location
            # ) VALUES (%s, %s, %s, %s, %s);"
            # """
            values = (
                request.data.dj_name,
                request.data.first_name,
                request.data.last_name,
                request.data.bio,
                request.data.location,
                request.data.email,
                request.data.phone                
            )
            dj_id = write_to_db(query, *values)
            if dj_id is None:
                return write_service_pb2.CreateEntityResponse(success=False, message="DB Error")
            
            # if request.data.HasField("social_data"):
            #     print("Processing social data...")
            #     social = request.data.social_data

            #     connection = mysql.connector.connect(
            #         user="root",
            #         password="Root1234",
            #         host="localhost",
            #         database="yaya_dev"
            #     )
            #     cursor = connection.cursor()
            #     cursor.execute(
            #         """
            #         INSERT INTO dj_socials (dj_id, website, soundcloud, spotify, facebook, instagram, snapchat, x) 
            #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            #         """,
            #         (dj_id,
            #         social.website or None,
            #         social.soundcloud or None,
            #         social.spotify or None,
            #         social.facebook or None,
            #         social.instagram or None,
            #         social.snapchat or None,
            #         social.x or None)
            #     )
            #     cursor.close()
            #     connection.close()

                # query2 = """
                # INSERT INTO dj_socials (dj_id, website, soundcloud, spotify, facebook, instagram, snapchat, x) 
                # VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                # """
                # values2 = (
                #     dj_id,
                #     social.website or None,
                #     social.soundcloud or None,
                #     social.spotify or None,
                #     social.facebook or None,
                #     social.instagram or None,
                #     social.snapchat or None,
                #     social.x or None
                # )
                # social_insert = write_to_db(query2, *values2)
                # if social_insert is None:
                #     return write_service_pb2.CreateEntityResponse(success=False, message="DB Error with social data")

            return write_service_pb2.CreateEntityResponse(success=True, message="dj created")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return write_service_pb2.CreateEntityResponse(success=False, message=err)

        except Exception as e:
            print(f"Error writing to DB: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=e)


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