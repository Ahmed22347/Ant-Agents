from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai_tools import SerpApiGoogleSearchTool, SerplyWebSearchTool
#from .tools.Segmented_search import CustomSearchTool
from ...tools.segmented_tool_wrapper import SegmentedToolWrapper
from ...tools.Fetch_tool import FetchTool
from crewai import LLM
#from crewai_tools import SeleniumScrapingTool

# Initialize the tool
# Create an LLM with streaming enabled




# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class founding_year_Crew():
    """ Headquaters Founding_Year No_Employees Valuation Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    topic = ""

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def business_researcher(self) -> Agent:
        search_tool_wrapper = SegmentedToolWrapper(SerplyWebSearchTool(), self.agents_config['business_researcher']['role'].format(company=self.topic))
        
        fetch_tool = FetchTool()

        llm = LLM(model="groq/llama-3.1-8b-instant",stream=False)
        return Agent(
            config=self.agents_config['business_researcher'],
            tools=[search_tool_wrapper, fetch_tool],
            max_rpm = 10,
            max_tpm =5000,
            llm=llm,
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        search_tool_wrapper = SegmentedToolWrapper(SerplyWebSearchTool(), self.agents_config['researcher']['role'].format(company=self.topic))
        
        fetch_tool = FetchTool()

        llm = LLM(model="groq/llama-3.1-8b-instant",stream=False)
        return Agent(
            config=self.agents_config['researcher'],
            tools=[search_tool_wrapper, fetch_tool],
            max_rpm = 10,
            max_tpm =5000,
            llm=llm,
            verbose=True
        )

    @agent
    def business_researcher_manager(self) -> Agent:
        llm = LLM(model="groq/llama-3.1-8b-instant",stream=False)
        return Agent(
            config=self.agents_config['business_researcher_manager'],
            max_rpm = 10,
            max_tpm =5000,
            llm=llm,
            verbose=True
        )

    @agent
    def researcher_manager(self) -> Agent:
        llm = LLM(model="groq/llama-3.1-8b-instant",stream=False)
        return Agent(
            config=self.agents_config['researcher_manager'],
            max_rpm = 10,
            max_tpm =5000,
            llm=llm,
            verbose=True
        )
       
    @task
    def founding_year_task(self) -> Task:
        return Task(
            config=self.tasks_config['founding_year_task'],
        )

    @task
    def find_website_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_website_task'],
        )    
    @task
    def find_headquarters_task(self) -> Task:
        return Task(
            config=self.tasks_config['headquarters_task'],
        ) 
    
    @task
    def find_employee_count_task(self) -> Task:
        return Task(
            config=self.tasks_config['employee_count_task'],
        ) 
    
    @task
    def find_valuation_task(self) -> Task:
        return Task(
            config=self.tasks_config['valuation_task'],
        )     

    @crew
    def crew(self, task_description, topic) -> Crew:
        """Creates the KybAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        self.topic =topic
        new_agent = self.business_researcher()
        manager = self.business_researcher_manager()
        new_task=None
        if task_description == "website":
            new_task= self.find_website_task()
            new_agent = self.researcher()
            manager = self.researcher_manager()
        elif task_description == "Headquaters":
            new_task = self.find_headquarters_task()
        elif task_description == "Year":
            new_task = self.founding_year_task()
        elif task_description == "Employees":
            new_task=self.find_employee_count_task()
        else:
            new_task=self.find_valuation_task()

        return Crew(
            agents=[new_agent], # Automatically created by the @agent decorator
            tasks=[new_task],
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
