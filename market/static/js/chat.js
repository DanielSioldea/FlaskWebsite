class ChatBox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chat-window'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.message = [];
    }

    display() {
        const { chatBox, sendButton } = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key === 'Enter') {
                this.onSendButton(chatBox)
            }
        })
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text = textField.value;
        if (text === "") {
            return;
        }

        console.log("sending message: ", text);

        let msg1 = { name: 'User', message: text }
        this.message.push(msg1);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: "Dr. D", message: r.answer };
                this.message.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''
            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });

    }

    updateChatText(chatbox) {
        var html = '';
        this.message.slice().reverse().forEach(function (item, index) {
            if (item.name === "Dr. D") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            }
            else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}

const chatbox = new ChatBox();
chatbox.display();