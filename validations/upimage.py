from wheezy.validation import Validator
from wheezy.validation.rules import length, required

upimage_validator = Validator({
    'author': [length(max=10)],
    'title': [length(max=14)],
    'message': [length(min=0, max=512)],
    'img': [required(message_template='<span class="red">画像が未選択です</span>')],
    'delkey': [length(max=20)],
})


