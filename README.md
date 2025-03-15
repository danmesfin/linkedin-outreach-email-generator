# LinkedIn Outreach Email Generator

## Overview
The LinkedIn Outreach Email Generator is an efficient and powerful Apify actor designed to automate the process of crafting personalized outreach emails for LinkedIn profiles. Whether you're looking to network, offer a job opportunity, propose collaboration, or initiate a sales conversation, this tool utilizes OpenAI's GPT models to generate contextually relevant and tailored outreach messages based on the profile URLs you provide.

the actor allows you to specify the purpose of your outreach and add personalized messages for each recipient, streamlining your LinkedIn outreach strategy.

## Features
- Personalized Outreach Emails: Automatically generate customized outreach emails based on LinkedIn profile information.
- OpenAI Integration: Leverage GPT-4 models (gpt-4o and gpt-4o-mini) for advanced language generation and personalization.
- Flexible Outreach Purpose: Choose from predefined outreach purposes, including networking, job opportunities, collaboration, sales, partnerships, or others.
- Customizable Message: Add a custom message to enhance the outreach and provide specific context to each email.
- Debug Mode: Option to enable debug mode for advanced troubleshooting and detailed output.

## How It Works
- Provide LinkedIn Profile URLs: Enter the list of LinkedIn profile URLs you want to target for outreach. These profiles will be the basis for generating your outreach emails.

- Choose Outreach Purpose: Select the purpose of your outreach (e.g., networking, job opportunity, collaboration, etc.) from the provided options.

- Add Custom Message: If you want to include additional context or specific points in your outreach emails, you can enter them in the custom message field.

- Select OpenAI Model: Choose which OpenAI model you wish to use for email generation. Currently, you can select from:
gpt-4o (default model)
gpt-4o-mini
- Run the Actor: Once the input is set up, run the actor to generate personalized outreach emails based on the provided LinkedIn profiles and outreach context.

### Input 
   ```
   {
  "customMessage": "write invitation for interview at Nike for fullstack application as John Mike from Nike Hiring manager. use no placeholder",
  "debug": false,
  "profileUrls": [
    "https://www.linkedin.com/in/danielmesfin"
  ],
  "outreachPurpose": "networking",
  "modelName": "gpt-4o-mini"
}

```

### output 
```
[
    {
        "profileUrl": "https://www.linkedin.com/in/danielmesfin",
        "outreachEmail": "Subject: Exciting Opportunity at Nike!\n\nDear Daniel Mesfin,\n\nI hope this message finds you well. My name is John Mike, and I am the Hiring Manager at Nike. I came across your profile, and I was impressed by your extensive experience as a Fullstack Developer, particularly your engagement with AI and Blockchain technologies at Hire Armada. \n\nAt Nike, we are looking for innovative and skilled individuals to join our team, and I believe your background aligns perfectly with our vision. We are currently seeking talented Fullstack Developers who are passionate about transforming the digital landscape within our esteemed brand.\n\nI would love the opportunity to discuss your experiences further and explore how you can contribute to our team. Would you be available for a brief interview in the coming days? \n\nThank you for considering this opportunity, and I look forward to connecting soon!\n\nBest regards,\n\nJohn Mike  \nHiring Manager  \nNike"
    }
]
```
