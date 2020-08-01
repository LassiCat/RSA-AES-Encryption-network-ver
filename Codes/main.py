from flask import Flask, request
import utils

main = Flask(__name__)


def load_key(_request):
    prikey_t = _request['prikey']
    thirdkey_t = _request['thirdkey']
    passphrase = _request['passphrase']

    return utils.load_key(thirdkey_t, prikey_t, passphrase)

@main.route('/encrypt/text', methods=['POST'])
def encrypt_text():
    status, prikey, thirdkey = load_key(request.form)
    message = request.form['message']
    sign_check = request.form ['sign_check']

    if not status: return {'status': False, 'msg': '密钥错误'}
    enc_message = utils.encrypt_text(prikey, thirdkey, message, sign_check)
    return {'status': True, 'msg': enc_message}

@main.route('/decrypt/text', methods=['POST'])
def decrypt():
    status, prikey, thirdkey = load_key(request.form)
    enc_message = request.form['message']

    if not status: return False, '密钥错误'

    _, status, message = utils.decrypt_text(prikey, thirdkey, enc_message)

    if   status == -2: return {'status': False, 'sig': False, 'msg': '密文损坏'}
    elif status == -1: return {'status': False, 'sig': False, 'msg': '密文无效'}
    elif status ==  0: return {'status': True, 'sig': True, 'msg': message}
    elif status ==  1: return {'status': True, 'sig': False, 'msg': message}