import json
import re

# Load JSON data
with open('podcast_episodes.json', 'r') as file:
    podcasts = json.load(file)

# Process each podcast episode
for podcast in podcasts:
    # Extract episode number from the title
    episode_number = re.search(r'(\d+):', podcast['title'])
    if episode_number:
        episode_number = episode_number.group(1)
    else:
        episode_number = None
    
    # Generate the LCS link
    lcs_link = f"https://lcspodcast.com/{episode_number}" if episode_number else None
    
    # Remove the LCS link from the description
    podcast['description'] = re.sub(r'https://lcspodcast\.com/\d+', '', podcast['description']).strip()
    
    # Add new attributes
    podcast['lcs_link'] = lcs_link
    podcast['episode'] = episode_number

# Generate HTML content
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Podcast Episodes</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .episode-title {
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1>Podcast Episodes</h1>
'''

# Create folding panels for every 10 episodes
for i in range(0, len(podcasts), 10):
    episode_titles = ", ".join([podcast["title"].split(": ", 1)[1] for podcast in podcasts[i:i+10]])

    html_content += f'''
        <div class="card mb-4">
            <div class="card-header episode-title" data-toggle="collapse" data-target="#episodes-{i//10}" aria-expanded="false" aria-controls="episodes-{i//10}">
                Episodes {i + 1} - {min(i + 10, len(podcasts))} - {episode_titles}
            </div>
            <div id="episodes-{i//10}" class="collapse">
    '''

    for podcast in podcasts[i:i+10]:
        podcast_id = podcast['link'].split('id')[1].split('?')[0]
        episode_id = podcast['link'].split('?i=')[1]

        html_content += f'''
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">{podcast["title"]}</h5>
                        <p class="card-text">{podcast["description"]}</p>
                        <a href="{podcast["link"]}" class="btn btn-primary" target="_blank">Open Link</a>
                        <a href="podcasts://podcast.apple.com/us/podcast/id{podcast_id}?i={episode_id}" class="btn btn-secondary" target="_blank">Podcasts App</a>
                        <a href="{podcast["lcs_link"]}" class="btn btn-info" target="_blank">LCS</a>
                    </div>
                </div>
        '''
    
    html_content += '''
            </div>
        </div>
    '''

html_content += '''
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        $(document).ready(function(){
            $(".episode-title").click(function(){
                var target = $(this).data("target");
                $(target).collapse('toggle');
            });
        });
    </script>
</body>
</html>
'''

# Write the HTML content to a file
with open('index.html', 'w') as file:
    file.write(html_content)

print('Static website generated: index.html')