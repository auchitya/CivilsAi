Create an env file using python3.11 -m venv env_name (Using Python3.11)
Install requirement.txt file using pip install -r requirement.txt and setup Postgres & GRPC. (We can create a bash file to do all these and install everything required with a single file execution)
Make you current path as Civils AI and start the RestAPIs using uvicorn main:app --reload (It gets hosted on local host and 8000 port). We can add a config file to make the ports flexible to change.
Command To Delete a Workflow curl -X DELETE "http://127.0.0.1:8000/workflows/New%20Pipeline"
Command To list all the Worflows curl -X GET "http://127.0.0.1:8000/workflows/"
Command To list a specific Worflow curl -X GET "http://127.0.0.1:8000/workflows/WorkflowName"

The reason to use monolithic is the services are too small to be seperated. Creating a microservices for this would be a overkill. What we can do is create a seperate Machine to execute tasks. 
I have used singleton connector for postgres and handled the exception using rollback so that the connector does not become useless.
