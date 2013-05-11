from wheezy.validation import Validator
from wheezy.validation.rules import length, required

upimage_validator = Validator({
    'author': [length(max=20)],
    'message': [length(min=0, max=512)],
    'img': [required(message_template='<span class="red">未入力</span>')],
    'delkey': [length(max=20)],
})


