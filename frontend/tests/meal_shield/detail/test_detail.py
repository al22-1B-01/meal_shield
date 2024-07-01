import pytest
import streamlit as st
from unittest.mock import MagicMock, patch
from meal_shield.detail import show_details

@pytest.fixture
def setup_session_state():
    st.session_state = MagicMock()
    st.session_state.selected_item = {
        'recipe_title': 'イチゴケーキ',
        'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/'
        '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117'
        '56033&p=1714165191',
        'recipe_ingredients': ['卵', '砂糖', 'バター'],
        'recipe_url': 'https://cookpad.com/recipe/7813040',
    }

def test_show_details_with_selected_item(setup_session_state):
    with patch('streamlit.image') as mock_image, \
        patch('streamlit.write') as mock_write, \
        patch('streamlit.button') as mock_button:
        
        mock_button.return_value = False
        show_details()
        
        mock_image.assert_called_once_with(
            'https://img.cpcdn.com/recipes/7813040/'
            '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117'
            '56033&p=1714165191',
            width=300
            )
        mock_write.assert_any_call(
            "### [イチゴケーキ](https://cookpad.com/recipe/7813040)"
            )
        mock_write.assert_any_call("材料: 卵, 砂糖, バター")

def test_show_details_without_selected_item(setup_session_state):
    st.session_state.selected_item = None
    
    with patch('streamlit.write') as mock_write, \
        patch('streamlit.button') as mock_button:
        
        mock_button.return_value = False
        show_details()
        
        mock_write.assert_any_call(
            '詳細を表示するレシピが選択されていません。'
            )

