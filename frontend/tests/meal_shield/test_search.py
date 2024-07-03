from unittest.mock import MagicMock, patch

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from meal_shield.detail import display_recipe_detail_entrypoint
from meal_shield.search import (
    fetch_recipe_detail,
    search_recipe_entrypoint,
    validate_input_data,
)

@pytest.fixture
def mock_response_success():
    return {
        'recipes': [
            {
                'recipe_title': 'イチゴケーキ',
                'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=11756033&p=1714165191',
                'recipe_ingredients': ['卵', '砂糖', 'バター'],
                'recipe_url': 'https://cookpad.com/recipe/7813040',
            },
            {
                'recipe_title': 'いちごけーき',
                'recipe_image_url': 'https://img.cpcdn.com/recipes/7781284/894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495&p=1711003018',
                'recipe_ingredients': ['卵', '牛乳', 'バニラ'],
                'recipe_url': 'https://cookpad.com/recipe/7781284',
            },
        ]
    }

@pytest.fixture
def mock_response_failure():
    return {'error': 'Not Found'}

@patch('requests.get')
@patch('streamlit.error')
def test_fetch_recipe_detail_success(mock_st_error, mock_get, mock_response_success):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_success

    recipe_name = 'ケーキ'
    allergies = ['卵', '乳']
    result = fetch_recipe_detail(recipe_name, allergies)

    assert result == mock_response_success
    mock_st_error.assert_not_called()

@patch('requests.get')
@patch('streamlit.error')
def test_fetch_recipe_detail_failure(mock_st_error, mock_get, mock_response_failure):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = mock_response_failure

    recipe_name = 'ケーキ'
    allergies = ['卵', '乳']
    result = fetch_recipe_detail(recipe_name, allergies)

    assert result is None
    mock_st_error.assert_called_once_with('エラーが発生しました: 404')

at = AppTest.from_file('src/meal_shield/app.py')
at.secrets['WORD'] = 'Foobar'
assert not at.exception

@pytest.fixture
def setup_session_state():
    st.session_state.clear()
    yield
    st.session_state.clear()

@pytest.fixture
def mock_streamlit():
    with patch('streamlit.error') as mock_error, \
         patch('streamlit.session_state', create=True) as mock_session_state, \
         patch('streamlit.experimental_rerun') as mock_rerun:
        mock_session_state.__delitem__ = MagicMock()
        mock_session_state.page = 'initial'  # Ensure 'page' exists for deletion
        yield mock_error, mock_session_state, mock_rerun

@patch('requests.get')
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_no_recipe_name(mock_fetch, mock_get, mock_streamlit):
    mock_error, mock_session_state, mock_rerun = mock_streamlit
    mock_session_state.page = '検索結果'
    mock_session_state.recipes = [{'status': 'error'}]
    mock_session_state.allergy_list = ['卵', '乳']
    mock_fetch.return_value = [{'status': 'error'}]

    validate_input_data('', ['卵', '乳'])

    mock_error.assert_called_once_with('レシピが入力されていません.')
    mock_session_state.__delitem__.assert_called_once_with('page')
    mock_rerun.assert_called_once()

@patch('requests.get')
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_no_allergies_list(mock_fetch, mock_get, mock_streamlit):
    mock_error, mock_session_state, mock_rerun = mock_streamlit
    mock_session_state.page = '検索結果'
    mock_session_state.recipes = [{'status': 'error'}]
    mock_session_state.allergy_list = []
    mock_fetch.return_value = [{'status': 'error'}]

    validate_input_data('ケーキ', [])

    mock_error.assert_called_once_with('アレルギー品目が入力されていません.')
    mock_session_state.__delitem__.assert_called_once_with('page')
    mock_rerun.assert_called_once()

@patch('requests.get')
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_no_recipes(mock_fetch, mock_get, mock_streamlit):
    mock_error, mock_session_state, mock_rerun = mock_streamlit
    mock_session_state.page = '検索結果'
    mock_session_state.recipes = [{'status': 'error'}]
    mock_session_state.allergy_list = ['卵', '乳']
    mock_fetch.return_value = [{'status': 'error'}]

    validate_input_data('ケーキ', ['卵', '乳'])

    mock_error.assert_called_once_with('検索結果が存在しません.')
    mock_session_state.__delitem__.assert_called_once_with('page')
    mock_rerun.assert_called_once()

@patch('requests.get')
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_valid_input(mock_fetch, mock_get, mock_streamlit):
    mock_error, mock_session_state, mock_rerun = mock_streamlit
    mock_session_state.page = '検索結果'
    mock_session_state.recipes = [{'status': 'success'}]
    mock_session_state.allergy_list = ['卵', '牛乳']
    mock_fetch.return_value = [{'status': 'success'}]

    validate_input_data('ケーキ', ['卵', '乳'])

    mock_error.assert_not_called()
    mock_session_state.__delitem__.assert_not_called()
    mock_rerun.assert_not_called()
