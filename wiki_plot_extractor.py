"""
-This program retrieves and stores film plot summaries from Wikipedia. 
-Users are prompted to enter a film title and the program attempts to fetch the plot summary from Wikipedia. 
-If successful, the information is saved into a JSON file.

- Be aware that some film titles may not be immediately recognised due to Wikipedia pages with the same name.
- For example, it is required to type 'The Shining (film)' rather than 'The Shining' to retrieve the specific plot summary.
"""

import os
import pandas as pd
import wikipediaapi
import json

# Set filename for JSON file
plots = "wiki_plots.json"

# Define columns for DataFrame
columns = ['Story ID', 'Film Title', 'Wikipedia Plot Summary']

# Check if the file already exists
if os.path.exists(plots):
    # Load existing JSON file into DataFrame
    with open(plots, 'r') as file:
        stories_data = json.load(file)
    stories_df = pd.DataFrame(stories_data)
else:
    # Create empty DataFrame if the file doesn't exist
    stories_df = pd.DataFrame(columns=columns)

def get_plot_text(film_title):
    # Example information to facilitate Wikipedia API requests
    user_agent = 'StoryGenerator (https://example.org/storygen/; storygen@example.org)'
    headers = {'User-Agent': user_agent}
    
    # Initialize Wikipedia API with the specified language and headers
    wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)
    
    # Attempt to get the page corresponding to the film title
    page_py = wiki_wiki.page(film_title)
    if not page_py.exists():
        print(f"The Wikipedia page for '{film_title}' does not exist.")
        return None
    else:
        sections = page_py.sections
        plot_section = None
        
    # Search for a section titled 'Plot' in the page
    for section in sections:
        if section.title.lower() == 'plot':
            plot_section = section
            break
    if plot_section:
        return plot_section.text
    return None

def generate_new_id():
    # Generate a new unique ID for each story entry in format 'WK-901', 'WK-902' etc
    if not stories_df.empty:
        last_story_id = stories_df['Story ID'].iloc[-1]
        last_id_number = int(last_story_id.split('-')[1])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 901 # Start numbering from 901 if DataFrame is empty
    new_story_id = "WK-" + str(new_id_number)
    return new_story_id

# Loop to get film title and IMDB rating from user until valid inputs are provided
while True:
    film_title = input("Enter the title of the film: ")
    if film_title.strip():
        wiki_plot = get_plot_text(film_title)
        if wiki_plot is not None:
            break
        else:
            print(f"Error: Plot section not found for the film '{film_title}'. Please enter a correct film title.")
    else:
        print("Error: A film title is required.")

# Add the new row to the DataFrame
new_row = {'Story ID': generate_new_id(),
           'Film Title': film_title,
           'Wikipedia Plot Summary': wiki_plot}
stories_df = pd.concat([stories_df, pd.DataFrame([new_row], columns=columns)], ignore_index=True)

# Convert the DataFrame to a list of dictionaries and write it to a JSON file
stories_list = stories_df.to_dict('records')
with open(plots, 'w') as file:
    json.dump(stories_list, file, indent=4)

# Print success messages to the user
print("The script executed successfully.")
print(f"A plot summary of '{film_title}' was saved to the JSON file '{plots}' in the specified format.")
