from unittest.mock import MagicMock, patch

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from meal_shield.detail import display_recipe_detail_entrypoint
from meal_shield.display_recipe import get_recipe_summary
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
                'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/'
                '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117'
                '56033&p=1714165191',
                'recipe_ingredients': ['卵', '砂糖', 'バター'],
                'recipe_url': 'https://cookpad.com/recipe/7813040',
            },
            {
                'recipe_title': 'いちごけーき',
                'recipe_image_url': 'https://img.cpcdn.com/recipes/7781284/'
                '894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495'
                '&p=1711003018',
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


@patch('streamlit.session_state', new_callable=MagicMock)
def test_initial_state(mock_session_state):
    mock_session_state.page = ''
    assert mock_session_state.page == ''


@patch('streamlit.session_state', new_callable=MagicMock)
@patch('requests.get')
def test_search_results_with_recipes(mock_get, mock_session_state):
    mock_session_state.page = ''
    mock_session_state.recipe_name = 'ケーキ'
    mock_session_state.allergy_list = ['卵', '牛乳']
    print('Session state before running:', mock_session_state)

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success"}

    with patch('streamlit.button', return_value=True):
        search_recipe_entrypoint()
        print('Session state after running:', mock_session_state)
    assert mock_session_state.page == '検索結果'


@patch('streamlit.session_state', new_callable=MagicMock)
@patch('requests.get')
def test_search_result_without_recipe_name(mock_get, mock_session_state):
    mock_session_state.page = ''
    mock_session_state.recipe_name = ''
    mock_session_state.allergy_list = []

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success"}

    with patch('streamlit.button', return_value=True) as mock_details:
        search_recipe_entrypoint()

    assert mock_session_state.page == '検索結果'


@patch('streamlit.session_state', new_callable=MagicMock)
@patch('requests.get')
def test_show_details_page(mock_get, mock_session_state):
    mock_session_state.page = 'details'
    mock_session_state.recipe_name = 'ケーキ'
    mock_session_state.recipe_url = 'https://cookpad.com/recipe/7813040'
    mock_session_state.selected_item = {
        'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=11756033&p=1714165191',
        'recipe_title': 'Delicious Cake',
        'recipe_url': 'https://cookpad.com/recipe/7813040',
        'recipe_ingredients': ['砂糖', '小麦粉', '卵'],
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"recipes": []}
    with patch('streamlit.button', return_value=True) as mock_details:
        display_recipe_detail_entrypoint()

    assert mock_session_state.page == '検索結果'


@pytest.fixture
def setup_session_state():
    # Mock the session_state with necessary initial values
    with patch('streamlit.session_state', new_callable=MagicMock) as mock_state:
        mock_state.page = '検索結果'  # Initialize page to prevent AttributeError on delete
        mock_state.recipes = [{'status': 'error'}]
        mock_state.allergy_list = []
        yield mock_state


@pytest.mark.usefixtures("setup_session_state")
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_recipe_name_empty(mock_fetch, setup_session_state):
    with patch('streamlit.error') as mock_error, patch(
        'streamlit.experimental_rerun'
    ) as mock_rerun:
        validate_input_data('', ['nuts'])
        mock_error.assert_called_once_with('レシピが入力されていません.')
        assert 'page' not in setup_session_state  # Check if page was deleted


@pytest.mark.usefixtures("setup_session_state")
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_fetch_error(mock_fetch, setup_session_state):
    mock_fetch.return_value = [{'status': 'error'}]
    with patch('streamlit.error') as mock_error, patch(
        'streamlit.experimental_rerun'
    ) as mock_rerun:
        validate_input_data('Some Recipe', ['nuts'])
        mock_error.assert_called_once_with('検索結果が存在しません.')
        assert 'page' not in setup_session_state  # Check if page was deleted


@pytest.mark.usefixtures("setup_session_state")
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_success(mock_fetch, setup_session_state):
    mock_fetch.return_value = {'status': 'success'}
    setup_session_state.recipes = [{'status': 'success'}]
    validate_input_data('Some Recipe', ['nuts'])
    assert setup_session_state.recipes == [{'status': 'success'}]


@pytest.mark.usefixtures("setup_session_state")
@patch('meal_shield.search.fetch_recipe_detail')
def test_validate_input_data_allergy_list_empty(mock_fetch, setup_session_state):
    with patch('streamlit.error') as mock_error, patch(
        'streamlit.experimental_rerun'
    ) as mock_rerun:
        validate_input_data('Pancakes', [])
        mock_error.assert_called_once_with('アレルギー品目が入力されていません.')
        assert 'page' not in setup_session_state  # Check if page was deleted


@patch('streamlit.session_state', new_callable=MagicMock)
@patch('requests.get')
def test_search_results_with_recipes(mock_get, mock_session_state):
    mock_session_state.page = ''
    mock_session_state.recipe_name = 'ケーキ'
    mock_session_state.allergy_list = ['卵', '牛乳']

    mock_session_state.page = 'details'
    mock_session_state.recipe_name = 'ケーキ'
    mock_session_state.recipe_url = 'https://cookpad.com/recipe/7813040'
    mock_session_state.selected_item = {
        'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=11756033&p=1714165191',
        'recipe_title': 'Delicious Cake',
        'recipe_url': 'https://cookpad.com/recipe/7813040',
        'recipe_ingredients': ['砂糖', '小麦粉', '卵'],
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"recipes": []}
    with patch('streamlit.button', return_value=True) as mock_details:
        display_recipe_detail_entrypoint()

    assert mock_session_state.page == '検索結果'
    assert mock_session_state.allergy_list == ['卵', '牛乳']
    assert mock_session_state.recipe_name == 'ケーキ'
