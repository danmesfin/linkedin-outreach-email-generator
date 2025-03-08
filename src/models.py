"""This module defines Pydantic models for this project.

These models are used mainly for the structured tool and LLM outputs.
Resources:
- https://docs.pydantic.dev/latest/concepts/models/
"""

from __future__ import annotations

from pydantic import BaseModel, Field, RootModel


class InstagramPost(BaseModel):
    """Instagram Post Pydantic model."""

    url: str = Field(..., description='The URL of the post')
    likes_count: int = Field(..., description='The number of likes on the post', alias='likesCount')
    comments_count: int = Field(..., description='The number of comments on the post', alias='commentsCount')
    timestamp: str = Field(..., description='The timestamp when the post was published')
    caption: str | None = Field(None, description='The post caption')
    alt: str | None = Field(None, description='The post alt text')


class InstagramPosts(RootModel):
    """Root model for list of InstagramPosts."""

    root: list[InstagramPost]


class LinkedInProfile(BaseModel):
    """LinkedIn Profile Pydantic model."""

    url: str = Field(..., description='The URL of the LinkedIn profile')
    full_name: str = Field(..., description='Full name of the person', alias='fullName')
    headline: str | None = Field(None, description='Professional headline')
    summary: str | None = Field(None, description='Profile summary or about section')
    current_company: str | None = Field(None, description='Current company name', alias='currentCompany')
    current_position: str | None = Field(None, description='Current job title', alias='currentPosition')
    location: str | None = Field(None, description='Location information')
    industry: str | None = Field(None, description='Industry or field of work')


class LinkedInProfiles(RootModel):
    """Root model for list of LinkedInProfiles."""

    root: list[LinkedInProfile]