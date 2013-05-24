from wheezy.validation import Validator
from wheezy.validation.rules import length, required

upimage_validator = Validator({
    'author': [length(max=10)],
    'title': [length(max=20)],
    'message': [length(min=0, max=512)],
    'img': [required(message_template='<span class="red">画像が未選択です</span>')],
    'delkey': [length(max=20)],
})

reply_validator = Validator({
    'parent_id': [required(message_template='<span class="red">返信先IDがありません</span>')],
    'author': [length(max=10)],
    'message': [length(min=3, max=512), required(message_template='<span class="red">メッセージ内容を3文字以上入れてください</span>')],
#    'img': [required(message_template='<span class="red">画像が未選択です</span>')],
    'delkey': [length(max=20)],
})

delete_validator = Validator({
    'id': [required(message_template='<span class="red">削除対象となるIDがありません</span>')],
    'delkey': [required(message_template='<span class="red">削除キーを指定してください</span>')],
})


