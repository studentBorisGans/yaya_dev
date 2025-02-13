# import asyncio
import psycopg2

import grpc
import time #faking DB write
from concurrent import futures
import write_service_pb2
import write_service_pb2_grpc
from grpc_reflection.v1alpha import reflection
from google.protobuf.timestamp_pb2 import Timestamp

GENDER_MAP = {0: "Male", 1: "Female", 2: "Other"}
SPEND_CLASS_MAP = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

err_msg = ""

def write_to_db(query: str, *values):
    global err_msg
    err_msg = ""
    print("HereweeeS")
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(database = "postgres", 
                                        user = "user", 
                                        host= 'localhost',
                                        password = "password",
                                        port = 5432)

        cursor = connection.cursor()

        return None

        cursor.execute(query, values)
        connection.commit()
        print("Data inserted successfully.")

        # if cursor.with_rows:
        #     cursor.fetchall()
        return cursor.lastrowid
    
    except psycopg2.errors.DatabaseError as dbError:
        print(f"Database Error: \n{dbError}")
        err_msg = dbError
        return None
    except psycopg2.errors.OperationalError as opError:
        print(f"Operational Error: \n{opError}")
        err_msg = opError
        return None
    except Exception as genError:
        print(f"Unexpected Exception: \n{genError}")
        err_msg = genError
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("\nConnection closed")

class WriteService(write_service_pb2_grpc.WriteServiceServicer):    
    def CreateEvent(self, request, context):
        print(f"Received data: {request.data}")
        try:
            datetime = request.data.date.ToDatetime()
            iso = datetime.isoformat() + "Z"
            mysql_datetime = datetime.fromisoformat(iso.replace('T', ' ').replace('Z', '')).strftime('%Y-%m-%d %H:%M:%S')
            query = """
                INSERT INTO event_data (organizer_id, venue_id, event_name, date, budget, pre_event_poster, pre_bio)
                VALUES (%s, %s, %s, %s, %s, %s, %s);

            """
            values = (
                request.data.org_id,
                request.data.venue_id,
                request.data.name,
                mysql_datetime,
                request.data.budget,
                request.data.pre_event_poster,
                request.data.pre_bio
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {err_msg}")

            return write_service_pb2.CreateEntityResponse(success=True, message="Event created!")
        except Exception as e:
            print(f"Exception during writing: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=f"Exception during writing: {e}")
    
    def CreateUser(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO user_data (
                username, first_name, last_name, email, location, language, gender, age, spend_class, pw
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            values = (
                request.data.username,
                request.data.first_name,
                request.data.last_name,
                request.data.email,
                request.data.location,
                request.data.language,
                # GENDER_MAP[request.data.gender],
                request.data.gender,
                request.data.age,
                # SPEND_CLASS_MAP.get(request.data.spend_class, None),
                'NA',
                # int(request.data.music_service),
                request.data.pw,
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {err_msg}")

            return write_service_pb2.CreateEntityResponse(success=True, message="User created!")
        except Exception as e:
            print(f"Exception during writing: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=f"Exception during writing: {e}")
    # string email = 100;
#   string phone = 101;
    def CreateDj(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO dj (
                alias, first_name, last_name, bio, location, email, phone
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
                return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {err_msg}")
            
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

            return write_service_pb2.CreateEntityResponse(success=True, message="DJ created!")
        # except mysql.connector.Error as err:
        #     print(f"Exception during writing: {err}")
        #     return write_service_pb2.CreateEntityResponse(success=False, message=err)

        except Exception as e:
            print(f"Exception during writing: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=f"Exception during writing: {e}")

    def CreateVenue(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO venues (
                name, capacity, address, city, state, zip, country, table_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            values = (
                request.data.venue_name,
                request.data.venue_capacity,
                request.data.venue_address,
                request.data.venue_city,
                request.data.venue_state,
                request.data.venue_zip,
                request.data.venue_country,
                request.data.table_count
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {err_msg}")

            return write_service_pb2.CreateEntityResponse(success=True, message="Venue created!")
        except Exception as e:
            print(f"Exception during writing: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=f"Exception during writing: {e}")
    
    def CreateOrganizer(self, request, context):
        print(f"Received data: {request.data}")
        try:
            query = """
            INSERT INTO organizer (
                name, first_name, last_name, email, phone, country, website
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """

            values = (
                request.data.org_name,
                request.data.first_name,
                request.data.last_name,
                request.data.email,
                request.data.phone,
                request.data.country,
                request.data.website
            )
            if write_to_db(query, *values) is None:
                return write_service_pb2.CreateEntityResponse(success=False, message=f"DB Error: {err_msg}")

            return write_service_pb2.CreateEntityResponse(success=True, message="Organizer created!")
        except Exception as e:
            print(f"Exception during writing: {e}")
            return write_service_pb2.CreateEntityResponse(success=False, message=f"Exception during writing: {e}")


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