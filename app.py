from fastapi import FastAPI, HTTPException
from server import LectionsServicer
from concurrent import futures
import grpc
import lections_pb2_grpc
from config import GRPC_PORT
import threading
import logging

app = FastAPI()
grpc_server = None  # Теперь здесь будет храниться сам сервер

def run_grpc_server():
    global grpc_server
    try:
        with open(r"certs/server.key", "rb") as key_file:
            private_key = key_file.read()
        with open(r"certs/server.crt", "rb") as cert_file:
            certificate = cert_file.read()

        server_credentials = grpc.ssl_server_credentials(
            [(private_key, certificate)]
        )

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        lections_pb2_grpc.add_LectionsServiceServicer_to_server(LectionsServicer(), server)
        
        server.add_secure_port(f"[::]:{GRPC_PORT}", server_credentials)
        
        grpc_server = server
        server.start()
        logging.info(f"Secure gRPC Server started on port {GRPC_PORT}")
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"Failed to start secure gRPC server: {e}")
        raise

@app.post('/start_grpc_server')
def start_grpc():
    global grpc_server
    try:
        if grpc_server is not None:
            return {"Message": "Server already running"}
        
        thread = threading.Thread(target=run_grpc_server, daemon=True)
        thread.start()
        return {"Message": "gRPC server started successfully"}
    except Exception as e:
        logging.error("Failed to start gRPC server: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed: {e}")

@app.post('/stop_grpc_server')
def stop_grpc():
    global grpc_server
    try:
        if grpc_server is None:
            return {"Message": "Server not running"}
        
        grpc_server.stop(0)
        grpc_server = None
        return {"Message": "gRPC server stopped successfully"}
    except Exception as e:
        logging.error("Failed to stop gRPC server: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)