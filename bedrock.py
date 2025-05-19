import boto3
import json

from botocore.exceptions import ClientError

# Create an Amazon Bedrock Runtime client.
brt = boto3.client("bedrock-runtime")

# Set the model ID, e.g., Amazon Titan Text G1 - Express.
model_id = "arn:aws:bedrock:us-east-1:497773883116:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

# Define the prompt for the model.
prompt ="get code explain in the schema : Project Goal To build a SageMaker Canvas model that predicts engineer productivity (story points per day) based on historical task completion data,\n which will then be used in QuickSight to generate Gantt charts for forecasting timelines of new projects by engineering role,\n accounting for sequential and parallel task execution within epics.\n Generate a 1200 row dataset in JSON based on the following parameters.\n Test Data Requirements Schema engineer_tasks { task_id: integer (primary key) \n parent_task_id: integer (references task_id of parent epic, never null for regular tasks) depends_on_task_id: integer (nullable, references task_id of prerequisite task) engineer_id: integer engineer_name: string engineer_title: string (enum: \"Associate Engineer\", \"Professional Engineer\", \"Lead Engineer\", \"Principal Engineer\") default_points_per_day: float task_summary: string is_epic: boolean task_category: string (enum: \"Frontend\", \"Backend\", \"DevOps\", \"QA\", \"Design\", \"Documentation\") story_points: integer task_status: string (enum: \"Not Started\", \"In Progress\", \"Completed\") start_date: integer (range 1-130) due_date: integer (range 1-130) completed_date: integer (nullable, range 1-130) actual_days: integer (nullable) concurrent_tasks_count: integer actual_points_per_day: float (nullable) forecasted_points_per_day: float (target field for prediction) } \n Time Period 130 working days (representing 6 months of work days, excluding weekends) \n  All dates in the dataset represent working days only with Engineer Specifications 8 engineers total (2 of each title level) Default points per day by title: Associate Engineer: 0.5 points/day Professional Engineer: 1.0 points/day Lead Engineer: 1.5 points/day Principal Engineer: 2.0 points/day\n Task Allocation Rules No engineer can have more than 4 projects active concurrently Tasks should be distributed to keep engineers at or near capacity Start and end dates should be varied and somewhat evenly distributed Multi-project Impact Each additional concurrent task reduces an engineer's TOTAL productivity by 10% This reduced total is then distributed evenly across all active tasks, \n Example calculation for a Professional Engineer (baseline 1.0 points/day): With 1 task: 1.0 points/day on that task (100% of baseline) With 2 tasks: 0.45 points/day per task (0.9 total, 90% of baseline) With 3 tasks: 0.27 points/day per task (0.8 total, 80% of baseline) With 4 tasks: 0.18 points/day per task (0.7 total, 70% of baseline) Task Hierarchy and Dependencies All tasks are either: Epics (is_epic = true, parent_task_id is null) \n Stories that belong to an epic (is_epic = false, parent_task_id references an epic) Within epics, tasks can have dependencies: Sequential tasks: One task must finish before another can start (using depends_on_task_id) Parallel tasks: Multiple tasks can run simultaneously (depends_on_task_id is null).\n Task Categories Include a mix of task categories (Frontend, Backend, DevOps, QA, Design, Documentation) Distribution should be realistic based on engineer roles and specialties Data Volume Generate sufficient data to demonstrate patterns in engineer productivity Include completed, in-progress, and not-started tasks Ensure adequate historical data for meaningful model training Include examples of both sequential and parallel task execution patterns This dataset will be used to train a SageMaker Canvas model to predict engineer productivity, which will then inform QuickSight Gantt charts for project timeline forecasting based on engineer roles, task characteristics, and task dependencies."
 
payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "messages": [
        {
            "role": "user",
            "content": prompt + " just json data with satisfying constraints"
        }
    ],
    "max_tokens": 100000,
    "temperature": 0.7,
    "top_k": 250,
    "top_p": 1
}


# Convert the native request to JSON.
request = json.dumps(payload)

try:
    # Invoke the model with the request.
    response = brt.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())
print(model_response["content"])
# Extract and print the response text.
#response_text = model_response["text"]
#print(response_text)
