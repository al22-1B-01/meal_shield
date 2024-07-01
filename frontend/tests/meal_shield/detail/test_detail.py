from streamlit.testing.v1 import AppTest

def detail_test():
    at = AppTest.from_file('meal_shield.detail.py').run()
    at.secrets['WORD'] = 'Foobar'
    
    at.run()
    assert not at.exception
    
    at.text_input('word').input('Bazbat').run()
    assert at.warning[0].value == 'Try again'
    
    at.run()
    at.button('検索結果画面に戻る').click.run()
    assert st.session_state.page == '検索結果'
    assert st.session_state.selected_item is not None

    
