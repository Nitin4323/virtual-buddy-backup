css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 70px;
  max-height: 70px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
.admin-badge {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: left;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        width: fit-content;
}
.admin-badge:hover {
    background-color: #45a049;
    cursor: pointer;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://st3.depositphotos.com/8950810/17657/v/450/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQGW3_vCjLXY7Q/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1683635482765?e=1738800000&v=beta&t=-fYDBvBI25NYPcCl6N-91L2giqGpOq3HITRZH7UG9jM">
    </div>    
</div>
'''

header = """
    <div style="display: flex; align-items: center;">
        <h1 style="display: inline;">Virtual Buddy</h1>
        <div class="avatar">
        <img src="https://st3.depositphotos.com/8950810/17657/v/450/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>  
    </div>
    """
