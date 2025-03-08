"""This module defines the tools used by the agent.

Feel free to modify or add new tools to suit your specific needs.

To learn how to create a new tool, see:
- https://docs.crewai.com/concepts/tools
"""

from __future__ import annotations

import os

from apify import Actor
from apify_client import ApifyClient
from crewai.tools import BaseTool
from crewai.utilities.converter import ValidationError
from pydantic import BaseModel, Field

from src.models import InstagramPost, InstagramPosts
from src.models import LinkedInProfile, LinkedInProfiles


class InstagramScraperInput(BaseModel):
    """Input schema for InstagramScraper tool."""

    handle: str = Field(..., description="Instagram handle of the profile to scrape (without the '@' symbol).")
    max_posts: int = Field(default=30, description='Maximum number of posts to scrape.')


class InstagramScraperTool(BaseTool):
    """Tool for scraping Instagram profile posts."""

    name: str = 'Instagram Profile Posts Scraper'
    description: str = 'Tool to scrape Instagram profile posts.'
    args_schema: type[BaseModel] = InstagramScraperInput

    def _run(self, handle: str, max_posts: int = 30) -> list[InstagramPost]:
        run_input = {
            'directUrls': [f'https://www.instagram.com/{handle}/'],
            'resultsLimit': max_posts,
            'resultsType': 'posts',
            'searchLimit': 1,
        }
        if not (token := os.getenv('APIFY_TOKEN')):
            raise ValueError('APIFY_TOKEN environment variable is missing!')

        apify_client = ApifyClient(token=token)
        if not (run := apify_client.actor('apify/instagram-scraper').call(run_input=run_input)):
            msg = 'Failed to start the Actor apify/instagram-scraper'
            raise RuntimeError(msg)

        dataset_id = run['defaultDatasetId']
        dataset_items: list[dict] = (apify_client.dataset(dataset_id).list_items()).items

        try:
            posts: InstagramPosts = InstagramPosts.model_validate(dataset_items)
        except ValidationError as e:
            Actor.log.warning('Received invalid dataset items: %s. Error: %s', dataset_items, e)
            raise RuntimeError('Received invalid dataset items.') from e
        else:
            return posts.root


class LinkedInScraperInput(BaseModel):
    """Input schema for LinkedInScraper tool."""

    profile_url: str = Field(..., description="LinkedIn profile URL to scrape.")

class LinkedInScraperTool(BaseTool):
    """Tool for scraping LinkedIn profiles."""

    name: str = 'LinkedIn Profile Scraper'
    description: str = 'Tool to scrape LinkedIn profiles and gather professional information.'
    args_schema: type[BaseModel] = LinkedInScraperInput

    def _run(self, profile_url: str) -> LinkedInProfile:
        if not (token := os.getenv('APIFY_TOKEN')):
            raise ValueError('APIFY_TOKEN environment variable is missing!')

        apify_client = ApifyClient(token=token)
        run_input = {
            'profileUrls': [profile_url],
        }

        Actor.log.info(f'Starting LinkedIn profile scrape for: {profile_url}')
        if not (run := apify_client.actor('dev_fusion/linkedin-profile-scraper').call(run_input=run_input)):
            Actor.log.warning(f'Failed to scrape profile: {profile_url}')
            raise RuntimeError(f'Failed to scrape profile: {profile_url}')

        dataset_id = run['defaultDatasetId']
        dataset_items: list[dict] = (apify_client.dataset(dataset_id).list_items()).items
        Actor.log.info(f'Received raw dataset items: {dataset_items}')

        try:
            # Add URL field to the dataset items before validation
            for item in dataset_items:
                item['url'] = profile_url

            profiles: LinkedInProfiles = LinkedInProfiles.model_validate(dataset_items)
            if not profiles.root:
                Actor.log.warning('No profile data found in the response')
                return None
            
            profile = profiles.root[0]
            Actor.log.info(f'Successfully scraped profile data: {profile}')
            return profile
        except ValidationError as e:
            Actor.log.warning(f'Received invalid data for profile {profile_url}: {e}')
            raise RuntimeError(f'Received invalid data for profile {profile_url}') from e
        return all_profiles