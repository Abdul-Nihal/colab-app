const socket = io();
        let username;

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('connected', (data) => {
            console.log(data.message);
        });

        socket.on('username_set', (data) => {
            console.log("Username set:", data.username);
            username = data.username;
            document.getElementById('user-section').style.display = 'none';
            document.getElementById('editor-section').style.display = 'block';

        });

        socket.on('username_error', (data) => {
            alert(data.message);
        });

        socket.on('text_update', (data) => {
            if (data.user != username){
                document.getElementById('text-area').value = data.text;
            }
        });

        socket.on('text_error', (data) => {
            alert(data.message);
        });

        socket.on('user_list_update', (data) => {
            const userList = document.getElementById('user-list');
            userList.innerHTML = '';

            data.users.forEach(user => {
                const userItem = document.createElement('li');
                userItem.textContent = user.name || "Anonymous";
                userList.appendChild(userItem);
            });
        });


        function setUsername() {
            const usernameInput = document.getElementById('username-input');
            username = usernameInput.value;
            socket.emit('set_username', { username: username });
            usernameInput.value = ''; // Clear input field
        }

        function textChanged() {
            const text = document.getElementById('text-area').value;
            socket.emit('text_change', { text: text });
        }