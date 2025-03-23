import grpc
import workflow_pb2, workflow_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = workflow_pb2_grpc.WorkflowExecutorStub(channel)

def execute_workflow(workflow_name):
    print(f"workflow_name type: {type(workflow_name)}, value: {workflow_name}")
    request = workflow_pb2.ExecuteRequest(workflow_name=workflow_name)
    response = stub.ExecuteWorkflow(request)
    print(f"Execution Response: {response.message}, Status: {response.status}")

def get_workflow_status(workflow_name):
    request = workflow_pb2.StatusRequest(workflow_name=workflow_name)
    response = stub.GetWorkflowStatus(request)
    print(f"Workflow Status: {response.status}")

if __name__ == "__main__":
    execute_workflow("asdasd")
    get_workflow_status("asdasdasd")
