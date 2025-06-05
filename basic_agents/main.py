#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from basic_agents.crews.poem_crew.poem_crew import PoemCrew
from basic_agents.crews.poem_crew.founding_year_crew import founding_year_Crew
from basic_agents.crews.poem_crew.config.tasks import founding_year_task


class AgentState(BaseModel):
    sentence_count: int = 1
    website: str = ""
    year: str = ""
    valuation: str = ""
    headquaters: str = ""
    employee_count: str = ""
    topic: str = "Databricks"



class AgentFlow(Flow[AgentState]):

    @start()
    def start_flow(self):
        print("Start")


    @listen(start_flow)
    def find_website(self):
        print("finding Website")
        result = (
            founding_year_Crew()
            .crew(task_description="website", topic=self.state.topic)
            .kickoff(inputs={"company": self.state.topic})
        )

        print("Year", result.raw)
        self.state.website = result.raw

    @listen(find_website)
    def find_headquarters(self):
        result = (
            founding_year_Crew()
            .crew(task_description="Headquaters", topic=self.state.topic)
            .kickoff(inputs={"company": self.state.topic})
        )
      
        self.state.headquaters = result.raw
        print(self.state.headquaters)


    @listen(find_headquarters)
    def find_year(self):
        result = (
            founding_year_Crew()
            .crew(task_description="Year", topic=self.state.topic)
            .kickoff(inputs={"company": self.state.topic})
        )
      
        self.state.year = result.raw


    @listen(find_year)
    def find_employee_count(self):
        result = (
            founding_year_Crew()
            .crew(task_description="Employees", topic=self.state.topic)
            .kickoff(inputs={"company": self.state.topic})
        )
      
        self.state.employee_count = result.raw

    @listen(find_employee_count)
    def find_value(self):
        result = (
            founding_year_Crew()
            .crew(task_description="value", topic=self.state.topic)
            .kickoff(inputs={"company": self.state.topic})
        )
      
        self.state.valuation = result.raw
    
    @listen(find_value)
    def process_output(self):
        print(f"Report")
        print(f"Company: {self.state.topic}")
        print(f"Founding Year: {self.state.year}")   
        print(f"Headquarters: {self.state.headquaters}")
        print(f"Employee Count: {self.state.employee_count}")        
        print(f"Valuation: {self.state.valuation}")
        print(f"Website: {self.state.website}")


def kickoff():
    poem_flow = AgentFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = AgentFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
