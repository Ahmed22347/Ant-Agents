from crewai import Task
from crewai.project import task
import yaml


# Load YAML once
with open("src/basic_agents/crews/poem_crew/config/tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

@task
def founding_year_task(company: str):
    raw_task = tasks_config["founding_year_task"]
    description = raw_task["description"].format(company=company)
    expected_output = raw_task["expected_output"].format(company=company)

    return Task(
        description=description,
        expected_output=expected_output,
        agent=raw_task["agent"]
    )


@task
def find_website_task() -> Task:
    return Task(
        config=tasks_config['find_website_task'],
    )