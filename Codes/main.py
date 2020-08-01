from flask import Flask, request
import utils

main = Flask(__name__)

@app.route('/encrypt/text', methods=['POST'])
def encrypt_text():
    prikey_t = request.form['prikey']
    thirdkey_t = request.form['thirdkey']
    passphrase = request.form['passphrase']
    message = request.form['message']
    sign_check = request.form ['sign_check']

    status, prikey, thirdkey = utils.load_key(thirdkey_t, prikey_t, passphrase)
    if not status: return False, '密钥错误'
    enc_message = utils.encrypt_text(prikey, thirdkey, message, sign_check)
    return True, enc_message