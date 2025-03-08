"""This module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations

from apify import Actor
from crewai import Agent, Crew, Task

from src.tools import LinkedInScraperTool


async def main() -> None:
    """Main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with the Apify platform, and it also enhances performance in
    the field of web scraping significantly.

    Raises:
        ValueError: If the input is missing required attributes.
    """
    async with Actor:
        # Charge for Actor start
        await Actor.charge('actor-start')

        # Handle input
        actor_input = await Actor.get_input()

        profile_urls = actor_input.get('profileUrls', [])
        Actor.log.info(f"Processing {len(profile_urls)} profile URLs")
        outreach_purpose = actor_input.get('outreachPurpose')
        custom_message = actor_input.get('customMessage')
        model_name = actor_input.get('modelName', 'gpt-4o-mini')

        if not profile_urls:
            msg = 'Missing "profileUrls" attribute in input!'
            raise ValueError(msg)
        if not outreach_purpose:
            msg = 'Missing "outreachPurpose" attribute in input!'
            raise ValueError(msg)

        # Create a toolkit for the agent
        tools = [LinkedInScraperTool()]

        # Create an agent
        agent = Agent(
            role='Professional Outreach Specialist',
            goal='Generate personalized outreach emails for multiple LinkedIn profiles',
            backstory='I am an AI assistant specialized in professional networking and communication',
            tools=tools,
            llm_model=model_name,
        )

        results = []
        for profile_url in profile_urls:
            # Create a task for each profile
            task = Task(
                description=f'Generate personalized outreach email for the LinkedIn profile at {profile_url}. Purpose: {outreach_purpose}. Additional context: {custom_message}',
                agent=agent,
                expected_output="A personalized outreach email corresponding to the provided LinkedIn profile",
                context=[{
                    'profile_url': profile_url,
                    'description': f'LinkedIn profile at {profile_url} needs a personalized outreach email',
                    'expected_output': 'A detailed personalized email based on the profile information'
                }]
            )

            # Create a crew for each task
            crew = Crew(
                agents=[agent],
                tasks=[task],
            )
            # Execute the task
            result = crew.kickoff()

            # Ensure result is a string
            if not isinstance(result, str):
                result = str(result)

            # Store the result
            await Actor.push_data({
                'profileUrl': profile_url,
                'outreachEmail': result,
            })
            await Actor.charge('task-completed')
            # await Actor.push_data(result)
        Actor.log.info('Pusheded all data into the dataset!')