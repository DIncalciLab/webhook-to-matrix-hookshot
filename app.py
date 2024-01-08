import requests
from flask import Flask, request, make_response
from config import url

app = Flask(__name__)

@app.route("/webhook/slack/<hook>", methods=['POST'])
def slack(hook):
    plain = []
    incoming = request.json
    app.logger.debug(f'Got incoming /slack hook: {incoming} ')

    attachments = incoming.get('attachments', [])
    username = str(incoming.get('username', ''))

    for attachment in attachments:
        color = str(attachment.get('color', '')).lower()
        title = str(attachment.get('title', ''))
        title_link = str(attachment.get('title_link', ''))
        text = str(attachment.get('text', ''))
        footer = str(attachment.get('footer', ''))
        fields = attachment.get('fields', [])

        if title and title_link:
            formatted = f"### [{title}]({title_link})" if title_link else f"## {title}"
            plain.append(formatted)
        if text:
            plain.append(text)

        for field in fields:
            title = str(field.get('title', ''))
            value = str(field.get('value', ''))
            if title and value:
                plain.append(f"**{title}**: {value}")

        if footer:
            plain.append(footer)

    assembled_message = "\n".join(plain)

    if username:
        json = {"text": plain, "username": username}
    else:
        json = {"text": plain}

    app.logger.debug(f'Sending hookshot:{json}')
    r = requests.post(url + hook, json=json)

    response = make_response('ok', 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(port=9080, debug=True)
