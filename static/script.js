// for toggle dark and light modes
const toggle = document.getElementById('modes').children[0];

toggle.addEventListener('click', () => {
	var logos = document.querySelectorAll('.chatBUt'); // index 0 is darkmode
	var everything = document.querySelectorAll('.light-mode');
	for (let i = 0; i < everything.length; i++) {
		everything[i].classList.remove('light-mode');
		everything[i].classList.add('dark-mode');
		logos[0].classList.remove('hidden');
		logos[1].classList.add('hidden');
	}

	if (everything.length == 0) {
		everything = document.querySelectorAll('.dark-mode');
		for (let i = 0; i < everything.length; i++) {
			everything[i].classList.remove('dark-mode');
			everything[i].classList.add('light-mode');
			logos[0].classList.add('hidden');
			logos[1].classList.remove('hidden');
		}
	}
});


const textbox = document.getElementById('textbox');
const buttonContainer = document.getElementById('buttons-container');
const buttons = buttonContainer.querySelectorAll('button');
const sendBtn = document.getElementById('send-button');
const intro = document.querySelector('.intro');
const chatbox = document.querySelector('main');
const chatMessages = document.querySelector('.convo-wrapper');

textbox.addEventListener("input", (e) => {
	if (textbox.value.trim() === "") {
		buttonContainer.classList.remove('hidden');
	} else {
		buttonContainer.classList.add('hidden');
	}
});

textbox.addEventListener('input', function() {
	this.rows = this.value.split('\n').length;
});

sendBtn.addEventListener('click', sendMessage);

textbox.addEventListener("keydown", (event) => {
	if(event.key != 'Enter') return;
	if(event.shiftKey) return;
	event.preventDefault();
	sendBtn.click()
});

buttons.forEach(function(button) {
	button.addEventListener('click', () => {
		textbox.value = button.textContent;
		sendBtn.click();
	});
});

// functions
function sendMessage() {
	let message = trimPreserveNewlines(textbox.value);
	
	if (message.length != 0) {
		// do sending of message here
		let userLi = createUserChat(message);
		chatMessages.appendChild(userLi);
		smoothScrollToBottom(chatbox, 1);
		let botLi, delay = 500;
		
		// create the response
		$.when(
			$.get("/get", {msg: message}, function(response_message){
				botLi = createBotChat(response_message);
				delay += response_message.length / 2;
			})
		).then(function() {
			setTimeout(function() {
				chatMessages.appendChild(botLi);
				smoothScrollToBottom(chatbox, 1);
			}, delay);
		})
		// setTimeout(function() {
		// 	$.post("/get", {msg: message}, function(result) {
		// 		if (result.score < 0.4) {

		// 		} else {
		// 			botLi = createBotChat(result.)
		// 		}
		// 	});
		// })

		buttonContainer.classList.add('hidden');
		chatbox.classList.remove('hidden');
		intro.classList.add('hidden');
	}
	
	resetTextbox();
}

function resetTextbox() {
	textbox.value = "";
	textbox.rows = 1;
}

function clickBtn(button) {
	button.click();
}

function createUserChat(chat) {
	return createLiHTML(chat, 'user', `<i class="ri-user-line"></i>`);
}

function createBotChat(chat) {
	return createLiHTML(chat, 'bot', `<i class="ri-robot-3-line"></i>`);
}

function createLiHTML(chat, type, icon) {
	let li = document.createElement('li');
	li.classList.add(type);
	let chatElement = document.createElement('div');
	chatElement.classList.add('chat');

	// inside the chat
	const lines = chat.split('\n');
	const paragraphs = lines.map(line => `<p>${line}</p>`);
	const paragraph = paragraphs.join('');
	let iconElement = document.createElement('div');
	iconElement.classList.add('icon');
	iconElement.innerHTML = icon;
	chatElement.innerHTML = paragraph;
	
	// put it all together
	li.appendChild(chatElement);
	li.appendChild(iconElement);

	// li.innerHTML = `<div class="chat">${chat}</div><div class="icon"></div>`
	return li;
}

function trimPreserveNewlines(text) {
    // Trim leading and trailing whitespace
    text = text.trim();

    // Replace leading and trailing whitespace for each line
    text = text.replace(/^\s+|\s+$/g, '');

    return text;
}

function smoothScrollToBottom(element, speed) {
	const start = element.scrollTop;
	const end = element.scrollHeight - element.clientHeight;
	const distance = end - start;
	const duration = distance / speed;
	let startTime = null;

	function animateScroll(timestamp) {
		if (!startTime) startTime = timestamp;
		const elapsed = timestamp - startTime;
		const progress = elapsed / duration;
		element.scrollTop = start + distance * progress;
		if (elapsed < duration) {
			requestAnimationFrame(animateScroll);
		} else {
			element.scrollTop = end;
		}
	}

	requestAnimationFrame(animateScroll);
	// chatbox.scrollTop = chatbox.scrollHeight;
}