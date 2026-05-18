from openai import OpenAI
from config import OPENAI_API_KEY

def get_summaries(articles, time_context="the last few hours"):
    """
    Uses OpenAI to curate and summarize a list of articles.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("ERROR: OpenAI API key is missing or invalid.")
        return None

    if not articles:
        return "No new gaming news at this time."

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Prepare the prompt
    prompt = f"You are a helpful and enthusiastic gaming news AI agent. Curate, summarize, and format the following gaming news articles collected over {time_context}.\n\n"
    prompt += "Instructions:\n"
    prompt += "- Pick only the most important or interesting news from this list. Ignore minor updates or fluff.\n"
    prompt += "- Provide a catchy headline for the update.\n"
    prompt += "- Write a concise, engaging summary for each important item, including the source and a link.\n"
    prompt += "- Format the output in clean Markdown.\n"
    prompt += "- If there's no major news, simply state that there haven't been any significant updates.\n\n"
    
    prompt += "### Raw Articles:\n"
    for i, art in enumerate(articles[:20]): # Limit to top 20 to avoid exceeding token limits
        prompt += f"{i+1}. [{art['source']}] {art['title']} - {art['link']}\n"
        prompt += f"Summary snippet: {art['summary'][:300]}...\n\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using gpt-4o-mini for cost efficiency and good performance
            messages=[
                {"role": "system", "content": "You are a professional gaming journalist and AI news curator for a Microsoft Teams channel."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
