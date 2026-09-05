import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm
import re

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)\

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode='w') as outfile:
        json.dump(enriched_posts, outfile, indent=4)



def extract_json_string(text: str) -> str:
    """Extract JSON object from LLM output with possible extra text."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise OutputParserException("Could not extract valid JSON from the response.")

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = ''' I will give you a list of tags. You need to unify them with the following requirements:

    1. Tags are unified and merged to create a shorter, cleaner list.
        - Ex 1: "Jobseekers", "Job Hunting" → "Job Search"
        - Ex 2: "Motivation", "Inspiration", "Drive" → "Motivation"
        - Ex 3: "Personal Growth", "Personal Development", "Self Improvement" → "Self Improvement"
        - Ex 4: "Scam Alert", "Job Scams" → "Scams"

    2. Tags should be grouped into broader categories where possible:
        - Tech-related tags like "Python", "MachineLearning", "FrontendDeveloper", "Robotics", etc. can be grouped under "Tech" or "Software Development" or similar.
        - Internship-related terms like "bharatintern", "#Internship" → "Internship"
        - Project-related terms like "Tkinter", "MPC", "bharatintern", "Capstone", etc. should be grouped under "Projects".
        - Mental health-related terms like "toxic masculinity", "MentalHealth", "MCP" → "Mental Health"

    3. Do **not** include any tags that contain a `#` (hashtag). Strip them or discard them.

    4. Each tag must use **Title Case** (e.g., "Motivation", "Job Search").

    5. Output must be a valid **JSON object**, with **no preamble**, explanation, or formatting text around it.

    6. The output JSON should be a mapping of original tags to unified tags.
        - Example:
          ```json
          {{{{
            "Jobseekers": "Job Search",
            "Job Hunting": "Job Search",
            "Motivation": "Motivation"
          }}}}
          ```

    Here is the list of tags:
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'tags': unique_tags_list})
    print("LLM response for tag unification:\n", response.content)

    try:
        json_parser = JsonOutputParser()
        cleaned_text = extract_json_string(response.content)
        res = json_parser.parse(cleaned_text)
        if not isinstance(res, dict):
            raise OutputParserException("Parsed response is not a dict.")
        return res
    except Exception as e:
        raise OutputParserException("Context too big. Unable to parse jobs.") from e


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON file. No preamble.
    2. JSON object should have exactly 3 keys : line_count, language and tags
    3. tags is an array of text tags. Extract maximum two tags.
    4. Do **not** include any tags that contain a `#` (hashtag). Strip them or discard them.
    5. Language should be English or Hinglish (Hinglish mean Hindi + English)
    6. No tag should have a proper noun contained.
    
    Here is the actual post on which you need to perform the task:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        cleaned_text = extract_json_string(response.content)
        res = json_parser.parse(cleaned_text)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")

//commenenenenennenenenenent
