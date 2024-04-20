import requests

APP_ID = "1409987012979008"
APP_SECRET = "53c91e6169ef89599c17fea5f79c4758"
DISPLAY_NAME = "LAHacks2024"
OATH_REDIRECT_URL = "https://danielbonkowsky.github.io/lahacks24-authenticator/"

redirected_url = "https://danielbonkowsky.github.io/lahacks24-authenticator/?code=AQC3ozkpyKtMSLwZKO23cb8I82hzCwhNuNVOdMfdcaX-hRO8308GygLsDmrzFNf1GkmAUrSkJLhtl0agd4Huf5L09qPZoXAJ8e7T8Ys8swxDmambOoOgTEObyXXTtpmoyYVWMsp4C1c7ERJiBR5-VQJXha4hzmwIf43MCKO1VQ6SbJqfuc1NBBWdAnEBwUTUwLVQIIlxFw0DN-tc83SalOlfsEPhzVDAoa0jVzXq0ZHwtg#_"

code = (redirected_url.split("code=")[1])

code = code[:len(code)-2]

print(code)