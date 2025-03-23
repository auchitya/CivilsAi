import grpc
from concurrent.futures import ThreadPoolExecutor
from workflow_executor import WorkflowExecutorServicer
import workflow_pb2_grpc

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    workflow_pb2_grpc.add_WorkflowExecutorServicer_to_server(WorkflowExecutorServicer(), server)

    print("Starting gRPC Server on port 50051...")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
