Create an env file using python3.11 -m venv env_name (Using Python3.11)

Install requirement.txt file using pip install -r requirement.txt and setup Postgres & GRPC. (We can create a bash file to do all these and install everything required with a single file execution)

Make you current path as Civils AI and start the RestAPIs using uvicorn main:app --reload (It gets hosted on local host and 8000 port). We can add a config file to make the ports flexible to change.

Command To Create a Workflow curl -X POST "http://127.0.0.1:8000/workflows/" -H "Content-Type: application/json" -d '{"name": "New Pipelines2"}'

Command To Delete a Workflow curl -X DELETE "http://127.0.0.1:8000/workflows/New%20Pipeline"

Command To list all the Worflows curl -X GET "http://127.0.0.1:8000/workflows/"

Command To list a specific Worflow curl -X GET "http://127.0.0.1:8000/workflows/WorkflowName"

Command To Create a Task curl -X POST "http://127.0.0.1:8000/tasks/New%20Pipelines"      -H "Content-Type: application/json"      -d '{
       "name": "Data Extraction",
       "description": "Extract data from source",
       "order": 1,
       "execution_type": "sync"
     }'

Command To Delete a Task curl -X DELETE "http://127.0.0.1:8000/tasks/WorkflowName/TaskName"

Command To Update a Task curl -X PUT "http://127.0.0.1:8000/tasks/New%20Pipelines/Data%20Extraction"      -H "Content-Type: application/json"      -d '{
       "description": "Extract data from sink",
       "order": 1,
       "execution_type": "sync"
     }'


Command to generate the grpc Code python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/workflow.proto

From your current path as CivilsAI run this command to start grpc server python grpc_server.py

From your current path as CivilsAI run this command to send request from grpc client python grpc_client.py

The reason to use monolithic is the services are too small to be seperated. Creating a microservices for this would be a overkill. What we can do is create a seperate Machine to execute tasks. 

I have used singleton connector for postgres and handled the exception using rollback so that the connector does not become useless.

If the classes were sharable we could have used __slots__ to limit the user of creating any new object params.
