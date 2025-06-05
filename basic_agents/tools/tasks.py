from crewai import Task
from crewai.project import task

@task
def founding_year_task() -> Task:
    return Task(
        config=self.tasks_config['founding_year_task'],
    )

@task
def find_website_task() -> Task:
    return Task(
        config=self.tasks_config['find_website_task'],
    )