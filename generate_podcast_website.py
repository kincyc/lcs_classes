import json
import re

# Load JSON data
with open('podcast_episodes.json', 'r') as file:
    podcasts = json.load(file)

# Process each podcast episode
for podcast in podcasts:
    # Extract episode number from the title
    episode_number = re.search(r'(\d+)\s*:', podcast['title'])
    if episode_number:
        episode_number = int(episode_number.group(1))  # Convert to integer
    else:
        episode_number = None
    
    # Generate the LCS link
    lcs_link = f"https://lcspodcast.com/{episode_number}" if episode_number else None
    
    # Remove the LCS link from the description
    podcast['description'] = re.sub(r'https://lcspodcast\.com/\d+', '', podcast['description']).strip()
    
    # Add new attributes
    podcast['lcs_link'] = lcs_link
    podcast['episode'] = episode_number

# Sort podcasts by episode number
podcasts.sort(key=lambda x: (x['episode'] is None, x['episode']))

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
    episode_range_start = podcasts[i]["episode"]
    episode_range_end = podcasts[min(i + 9, len(podcasts) - 1)]["episode"]

    html_content += f'''
        <div class="card mb-4">
            <div class="card-header episode-title" data-toggle="collapse" data-target="#episodes-{i//10}" aria-expanded="false" aria-controls="episodes-{i//10}">
                Episodes {episode_range_start} - {episode_range_end} - {episode_titles}
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
                        <div class="desktop-links">
                            <a href="{podcast["link"]}" class="btn btn-primary" target="_blank">Link</a>
                            <a href="podcasts://podcast.apple.com/us/podcast/id{podcast_id}?i={episode_id}" class="btn btn-secondary" target="_blank">Podcast</a>
                            <a href="{podcast["lcs_link"]}" class="btn btn-info" target="_blank">Learncraft</a>
                        </div>
                        <div class="mobile-links d-none">
                            <a href="{podcast["link"]}" class="btn btn-primary" target="_blank">Podcast</a>
                            <a href="{podcast["lcs_link"]}" class="btn btn-info" target="_blank">Learncraft</a>
                        </div>
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
        // Function to detect mobile browser
        function isMobileBrowser() {
            return /Mobi|Android/i.test(navigator.userAgent);
        }

        $(document).ready(function(){
            $(".episode-title").click(function(){
                var target = $(this).data("target");
                $(target).collapse('toggle');
            });

            // Toggle links based on browser type
            if (isMobileBrowser()) {
                $('.desktop-links').addClass('d-none');
                $('.mobile-links').removeClass('d-none');
            } else {
                $('.mobile-links').addClass('d-none');
                $('.desktop-links').removeClass('d-none');
            }
        });
    </script>
</body>
</html>
'''

# Write the HTML content to a file
with open('index.html', 'w') as file:
    file.write(html_content)

print('Static website generated: index.html')