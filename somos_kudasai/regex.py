import re


main_url = re.compile( r'^https?://somoskudasai.com/?$' )
article_url = re.compile( r'^https://somoskudasai.com/noticias/(?P<category>.+)/.+/?$' )
review_url = re.compile( r'^https://somoskudasai.com/resenas/.+/?$' )
