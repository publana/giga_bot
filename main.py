import streamlit as st
from gigachat_api import get_access_token, send_prompt_and_get_response

st.markdown('<style> .chat_message { color: red; } </style>', unsafe_allow_html=True)
st.title('Giga :) Bot')

if 'access_token' not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast('Токен успешно получен')
    except Exception as e:
        st.toast(f'Ошибка получения токена: {e}')

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'ai', 'content': 'Даня, я тебя внимательно слушаю ...'}]

for msg in st.session_state.messages:
    if msg.get('is_image'):
        st.chat_message(msg['role']).image(msg['content'])
    else:
        st.chat_message(msg['role']).write(msg['content'])

if user_prompt := st.chat_input():
    st.chat_message('user').write(user_prompt)
    st.session_state.messages.append({'role': 'user', 'content': user_prompt})

    with st.spinner('В процессе ...'):
        response, is_image = send_prompt_and_get_response(user_prompt, st.session_state.access_token)

        if is_image:
            st.chat_message('ai').image(response)
            st.session_state.messages.append({'role': 'ai', 'content': response, 'is_image': True})
        else:
            st.chat_message('ai').write(response)
            st.session_state.messages.append({'role': 'ai', 'content': response})

#   для запуска чатбота выполнить в терминале:  streamlit run main.py
#   или в EditConfugurations для main.py указать во вкладке InterpreterOptions:  -m streamlit run

