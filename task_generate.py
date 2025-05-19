import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
num_task_range=(20,40)
# Format the request payload using the model's native structure.

# Constants
START_DATE = datetime(2025, 6, 1)  # Overall start date
WORKING_DAYS = 60                  # Shortened timeframe

# Engineer specifications
ENGINEER_SPECS = {
    'Associate Engineer': {'count': 2, 'default_points_per_day': 0.5},
    'Professional Engineer': {'count': 2, 'default_points_per_day': 1.0},
    'Lead Engineer': {'count': 2, 'default_points_per_day': 1.5},
    'Principal Engineer': {'count': 2, 'default_points_per_day': 2.0}
}

# Task categories
TASK_CATEGORIES = ['Frontend', 'Backend', 'DevOps', 'QA', 'Design', 'Documentation']

# Task types and components for more diverse task summaries
TASK_TYPES = ['Implement', 'Design', 'Test', 'Document', 'Review', 'Refactor', 'Debug', 'Optimize', 
             'Migrate', 'Configure', 'Deploy', 'Analyze', 'Research', 'Prototype', 'Validate']
TASK_COMPONENTS = ['API', 'UI', 'Database', 'Authentication', 'Integration', 'Component', 'Module', 
                  'Service', 'Pipeline', 'Framework', 'Library', 'Security', 'Performance', 'Cache', 
                  'Monitoring', 'Logging', 'Analytics', 'Reporting', 'Search', 'Notification',
                  'Payment', 'User Management', 'Content Management', 'Workflow', 'Dashboard']

# Epic themes for more variety
EPIC_THEMES = [
    'Platform Upgrade', 'Feature Enhancement', 'Performance Optimization', 'Security Hardening', 
    'UX Redesign', 'Data Migration', 'Building Observability', 'Planning Effective support and alerts'
]

# Calculate productivity reduction by concurrent task count
def calculate_points_per_day(base_rate, concurrent_tasks):
    productivity_factor = 1 - (concurrent_tasks - 1) * 0.1
    productivity_factor = max(0.1, productivity_factor)  # Ensure minimum 10% productivity
    total_points = base_rate * productivity_factor
    return total_points / concurrent_tasks if concurrent_tasks > 0 else 0

# Function to check if a date is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

# Function to add working days to a date
def add_working_days(start_date, days):
    business_days_to_add = days
    current_date = start_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        if not is_weekend(current_date):
            business_days_to_add -= 1
    return current_date

# Generate working dates for our dataset
def generate_working_dates(start_date, num_days):
    working_dates = []
    current_date = start_date
    while len(working_dates) < num_days:
        if not is_weekend(current_date):
            working_dates.append(current_date)
        current_date += timedelta(days=1)
    return working_dates

working_dates = generate_working_dates(START_DATE, WORKING_DAYS)

# Create engineer data
engineers = []
engineer_id = 1

for title, specs in ENGINEER_SPECS.items():
    for i in range(specs['count']):
        engineers.append({
            'engineer_id': engineer_id,
            'engineer_name': f"{['John', 'Jane', 'Alex', 'Sam', 'Taylor', 'Morgan', 'Casey', 'Jordan'][engineer_id-1]}",
            'engineer_title': title,
            'default_points_per_day': specs['default_points_per_day']
        })
        engineer_id += 1

# Create 8 epics
num_epics = 3
epics = []

for i in range(1, num_epics + 1):
    epic_id = i
    epic_theme = EPIC_THEMES[i-1]
    epic_name = f"Epic {i}: {epic_theme}"
    epics.append({
        'task_id': epic_id,
        'parent_task_id': None,
        'depends_on_task_id': None,
        'engineer_id': None,
        'engineer_name': None, 
        'engineer_title': None,
        'default_points_per_day': None,
        'task_summary': epic_name,
        'is_epic': True,
        'task_category': random.choice(TASK_CATEGORIES),
        'story_points': random.randint(30, 60),  # Max 60 points per epic
        'task_status': 'Not Started',
        'start_date': None,
        'due_date': None,
        'completed_date': None,
        'actual_days': None,
        'concurrent_tasks_count': None,
        'actual_points_per_day': None,
        'forecasted_points_per_day': None
    })

# Track task assignments and concurrent tasks by engineer
engineer_task_assignments = {eng['engineer_id']: [] for eng in engineers}
task_id_counter = len(epics) + 1

# Create tasks and dependencies
tasks = []
for epic in epics:
    epic_id = epic['task_id']
    epic_category = epic['task_category']
    epic_points = epic['story_points']
    
    # Determine number of tasks in this epic (5-10 tasks per epic)
    num_tasks = random.randint(*num_task_range)
    
    # Create tasks for this epic
    epic_tasks = []
    points_remaining = epic_points
    
    for j in range(num_tasks):
        # Ensure we distribute all story points
        if j == num_tasks - 1:
            task_points = points_remaining
        else:
            # Ensure no task is more than 10 points
            max_points = min(points_remaining - (num_tasks - j - 1), 10)
            task_points = random.randint(1, max(1, max_points))
            points_remaining -= task_points
        
        # Select appropriate engineer based on task category and ensure workload balance
        suitable_engineers = [eng for eng in engineers 
                              if (epic_category in ['Frontend', 'Design'] and eng['engineer_title'] in ['Associate Engineer', 'Professional Engineer']) or 
                                 (epic_category in ['Backend', 'DevOps'] and eng['engineer_title'] in ['Professional Engineer', 'Lead Engineer', 'Principal Engineer']) or
                                 (epic_category in ['QA', 'Documentation'])]
        
        # Sort engineers by current workload
        engineer_workload = [(eng['engineer_id'], len(engineer_task_assignments[eng['engineer_id']])) 
                             for eng in suitable_engineers]
        engineer_workload.sort(key=lambda x: x[1])
        
        # Choose engineer with lowest workload, but respect max concurrent task limit
        chosen_engineer = None
        for eng_id, workload in engineer_workload:
            if workload < 4:  # Max 4 concurrent tasks
                chosen_engineer = next(eng for eng in engineers if eng['engineer_id'] == eng_id)
                break
        
        if not chosen_engineer:
            # If all suitable engineers are at capacity, pick one randomly
            chosen_engineer = random.choice(suitable_engineers)
        
        # Determine dependencies - some tasks depend on previous tasks
        depends_on = None
        if epic_tasks and random.random() < 0.7:  # 70% chance of dependency
            depends_on = random.choice(epic_tasks)['task_id']
        
        # Create a more diverse task summary
        task_type = random.choice(TASK_TYPES)
        task_component = random.choice(TASK_COMPONENTS)
        task_summary = f"Task {task_id_counter}: {task_type} {task_component} for {epic['task_summary'].split(':')[1].strip()}"
        
        task = {
            'task_id': task_id_counter,
            'parent_task_id': epic_id,
            'depends_on_task_id': depends_on,
            'engineer_id': chosen_engineer['engineer_id'],
            'engineer_name': chosen_engineer['engineer_name'],
            'engineer_title': chosen_engineer['engineer_title'],
            'default_points_per_day': chosen_engineer['default_points_per_day'],
            'task_summary': task_summary,
            'is_epic': False,
            'task_category': epic_category,
            'story_points': task_points,
            'task_status': 'Not Started',
            'start_date': None,
            'due_date': None,
            'completed_date': None,
            'actual_days': None,
            'concurrent_tasks_count': None,
            'actual_points_per_day': None,
            'forecasted_points_per_day': None
        }
        
        epic_tasks.append(task)
        tasks.append(task)
        engineer_task_assignments[chosen_engineer['engineer_id']].append(task_id_counter)
        task_id_counter += 1

# Distribute tasks across the timeline
# First, we need to stagger the epics to spread them out
epic_start_indices = list(range(0, WORKING_DAYS - 20, WORKING_DAYS // (len(epics) + 1)))
random.shuffle(epic_start_indices)

for i, epic in enumerate(epics):
    if i < len(epic_start_indices):
        epic_start_idx = epic_start_indices[i]
    else:
        epic_start_idx = random.randint(0, WORKING_DAYS // 2)
    
    epic['start_date'] = working_dates[epic_start_idx]

# Assign start dates, due dates, and completion status for tasks
for task in tasks:
    epic = next(e for e in epics if e['task_id'] == task['parent_task_id'])
    epic_start_date = epic['start_date']
    
    if task['depends_on_task_id'] is None:
        # Tasks with no dependencies can start at the epic start date
        try:
            start_idx = working_dates.index(epic_start_date)
        except ValueError:
            start_idx = 0
    else:
        # Find the dependency's completion date
        dependency = next((t for t in tasks if t['task_id'] == task['depends_on_task_id']), None)
        if dependency and dependency['completed_date']:
            # Start after the dependency is completed
            dependency_date = dependency['completed_date']
            try:
                start_idx = working_dates.index(dependency_date) + 1
            except ValueError:
                # If the exact date isn't found, find the next working day
                next_day = dependency_date + timedelta(days=1)
                while is_weekend(next_day):
                    next_day += timedelta(days=1)
                start_idx = min(len(working_dates) - 1, working_dates.index(next_day))
        else:
            # If dependency isn't completed yet, start a bit after the epic start
            try:
                start_idx = working_dates.index(epic_start_date) + random.randint(1, 5)
            except ValueError:
                start_idx = random.randint(0, 5) 
# Ensure we don't go beyond the available dates
        start_idx = min(start_idx, len(working_dates) - 1)
    
    # Assign start date
    task['start_date'] = working_dates[start_idx]
    
    # Calculate task duration based on story points and engineer's productivity
    base_points_per_day = task['default_points_per_day']
    
    # Count concurrent tasks for this engineer at this time
    concurrent_tasks = 1  # Start with this task
    for other_task in tasks:
        if (other_task['task_id'] != task['task_id'] and 
            other_task['engineer_id'] == task['engineer_id'] and
            other_task['start_date'] and task['start_date'] and
            other_task['start_date'] <= task['start_date'] and
            (not other_task['completed_date'] or 
             (other_task['completed_date'] and other_task['completed_date'] >= task['start_date']))):
            concurrent_tasks += 1
    
    concurrent_tasks = min(concurrent_tasks, 4)  # Cap at max 4 concurrent tasks
    task['concurrent_tasks_count'] = concurrent_tasks
    
    # Calculate actual productivity
    actual_points_per_day = calculate_points_per_day(base_points_per_day, concurrent_tasks)
    task['actual_points_per_day'] = actual_points_per_day
    
    # Add some variability to actual productivity (±20%)
    variability = random.uniform(0.8, 1.2)
    task['actual_points_per_day'] *= variability
    
    # Calculate forecasted productivity (what we'd predict)
    #task['forecasted_points_per_day'] = task['actual_points_per_day'] * random.uniform(0.9, 1.1)  # ±10% error
    
    # Calculate duration in days
    if task['actual_points_per_day'] > 0:
        duration_days = max(1, int(task['story_points'] / task['actual_points_per_day']))
    else:
        duration_days = max(1, int(task['story_points'] / 0.1))  # Avoid division by zero
    
    task['actual_days'] = duration_days
    
    # Calculate due date
    due_idx = min(start_idx + duration_days, len(working_dates) - 1)
    task['due_date'] = working_dates[due_idx]
    
    # Determine task status based on timeline
    current_date = working_dates[len(working_dates) // 2]  # Middle of our dataset represents "today"
    
    if task['due_date'] < current_date:
        # Task is due in the past
        task['task_status'] = np.random.choice(['Completed', 'In Progress'], p=[0.9, 0.1])
        if task['task_status'] == 'Completed':
            # Completed sometime between due date and a few days before
            completion_idx = random.randint(max(0, due_idx - 5), due_idx)
            task['completed_date'] = working_dates[completion_idx]
    elif task['start_date'] > current_date:
        # Task hasn't started yet
        task['task_status'] = 'Not Started'
        task['completed_date'] = None
    else:
        # Task is in progress
        task['task_status'] = np.random.choice(['Completed', 'In Progress', 'Not Started'], p=[0.3, 0.6, 0.1])
        if task['task_status'] == 'Completed':
            # Just completed
            completion_idx = random.randint(start_idx, min(due_idx, len(working_dates) - 1))
            task['completed_date'] = working_dates[completion_idx]

# Update epic dates based on their tasks
for epic in epics:
    epic_tasks = [t for t in tasks if t['parent_task_id'] == epic['task_id']]
    if epic_tasks:
        # Epic start date is the earliest task start date
        epic['start_date'] = min(t['start_date'] for t in epic_tasks if t['start_date'])
        
        # Epic due date is the latest task due date
        epic['due_date'] = max(t['due_date'] for t in epic_tasks if t['due_date'])
        
        # Epic status is based on tasks
        completed_tasks = [t for t in epic_tasks if t['task_status'] == 'Completed']
        if len(completed_tasks) == len(epic_tasks):
            epic['task_status'] = 'Completed'
            epic['completed_date'] = max(t['completed_date'] for t in completed_tasks if t['completed_date'])
        elif any(t['task_status'] == 'In Progress' for t in epic_tasks):
            epic['task_status'] = 'In Progress'
        else:
            epic['task_status'] = 'Not Started'

# Combine epics and tasks
all_tasks = epics + tasks

# Format dates
for task in all_tasks:
    for date_field in ['start_date', 'due_date', 'completed_date']:
        if task[date_field] is not None:
            task[date_field] = task[date_field].strftime('%Y-%m-%d')

# Create dataframe
df = pd.DataFrame(all_tasks)

# Save to CSV
df.to_csv('engineer_productivity_data.csv', index=False)
print(f"Generated {len(df)} records and saved to engineer_productivity_data.csv")
print(f"Epics: {len(df[df['is_epic'] == True])}, Tasks: {len(df[df['is_epic'] == False])}")
