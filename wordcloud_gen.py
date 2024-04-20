from wordcloud import WordCloud
from PIL import Image
import numpy as np

# Sample text
text = "hello hello world world python python python data data science word random hello daniel goldfish asdf asjlkj jasklfjlk asdjls asljkdf sajk"

# Generate word cloud
wordcloud = WordCloud(width = 1000, height = 250, 
                background_color ='white', 
                min_font_size = 10).generate(text)

# Convert the word cloud to an image
image_array = wordcloud.to_array()

# Convert the image array to a PIL image
image = Image.fromarray(image_array)

# Save the image to a file
image.save('wordcloud.png')
