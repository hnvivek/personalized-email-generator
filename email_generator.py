import os
import gradio as gr
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def generate_email(sender_background, sender_skills, sender_experience, recipient_name,
                   recipient_profile, recipient_awards, recipient_recent_post):
    # Set system prompt to guide the assistant
    system_prompt = """You are an expert email writer and career coach who helps craft highly effective, personalized outreach emails for Cinema job seekers. Your emails are tailored to the recipient and position, highlighting the sender's qualifications, experience, and passion in an engaging way.

    When given the following inputs:
    - Sender's background info (film school, degree, relevant experience, career goals)
    - Sender's skills and experience
    - Recipient's name and profile info (job title, company, industry, any other relevant details)
    - Recipient's recent awards
    - Recipient's recent post

    Generate a personalized outreach email with the following elements:
    - Engaging subject line
    - Proper salutation using recipient's name
    - Brief intro stating and appreciating their work and the reason for reaching out
    - Mention recipient's recent achievements and posts to show genuine interest and 
    you follow their work
    - Highlight sender's relevant qualifications, experience, and passion for the field
    - Express strong interest in potential opportunities to work with/for the recipient, especially Assistant Director of Photography roles
    - Closing paragraph reiterating interest, providing contact info, and thanking them for their time and consideration
    - Professional sign-off with sender's full name

    Write in a confident yet respectful tone, keeping the email concise (under 250 words) and make it look like written by a human, not generated. Aim to pique the recipient's interest and open the door to further conversation."""

    # Set user prompt
    user_prompt = f"""
    Write a personalized outreach email using the following inputs:

    Sender Info: {sender_background}
    Sender Skills: {sender_skills}
    Sender Experience: {sender_experience}

    Recipient Info:
    Name: {recipient_name}
    Profile: {recipient_profile}
    Recent Awards: {recipient_awards}
    Recent Post: {recipient_recent_post}

    Express interest in opportunities based on the sender's background.
    """

    # Call OpenAI's API to generate the email
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model="gpt-4o",
    )

    # Access the content of the response correctly
    email_content = chat_completion.choices[0].message.content
    return email_content


# Gradio interface
def gradio_interface(sender_background, sender_skills, sender_experience, recipient_name,
                     recipient_profile, recipient_awards, recipient_recent_post):
    return generate_email(sender_background, sender_skills, sender_experience,
                          recipient_name, recipient_profile, recipient_awards,
                          recipient_recent_post)


# Create Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Personalized Outreach Email Generator")

    with gr.Row():
        # Sender Information Block
        with gr.Column():
            gr.Markdown("## Sender Information")
            sender_input = gr.Textbox(label="Sender Background Info (Bio/Resume)",
                                      placeholder="Enter your background information...")
            skills_input = gr.Textbox(label="Sender Skills",
                                      placeholder="Enter relevant skills...")
            experience_input = gr.Textbox(label="Sender Experience",
                                          placeholder="Enter your relevant experience...")

    with gr.Row():
        # Recipient Information Block
        with gr.Column():
            gr.Markdown("## Recipient Information")
            recipient_name_input = gr.Textbox(label="Recipient Name",
                                              placeholder="Enter the recipient's name...")
            recipient_profile_input = gr.Textbox(label="Recipient Profile Info",
                                                 placeholder="Enter the recipient's profile info (e.g., recent work, projects)...")
            recipient_awards_input = gr.Textbox(label="Recipient Recent Awards",
                                                placeholder="Enter recipient's recent awards...")
            recipient_post_input = gr.Textbox(label="Recipient Recent Post",
                                              placeholder="Enter recipient's recent post or notable work...")

    generate_button = gr.Button("Generate Email")
    output_email = gr.Textbox(label="Generated Email",
                              placeholder="Your generated email will appear here...",
                              interactive=True)

    generate_button.click(gradio_interface,
                          inputs=[sender_input, skills_input, experience_input,
                                  recipient_name_input, recipient_profile_input,
                                  recipient_awards_input, recipient_post_input],
                          outputs=output_email)



    generate_button.click(gradio_interface,
                          inputs=[sender_input, skills_input, experience_input,
                                  recipient_name_input, recipient_profile_input,
                                  recipient_awards_input, recipient_post_input],
                          outputs=output_email)


# Launch the Gradio app
if __name__ == "__main__":
    demo.launch(share=True)