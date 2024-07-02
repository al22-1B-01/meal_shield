from unittest.mock import MagicMock, patch

import pytest
import streamlit as st

from meal_shield.display_recipe import display_recipe


# pytestのフィクスチャを定義
@pytest.fixture
def setup_session_state():
    st.session_state = MagicMock()
    st.session_state.page = ''
    st.session_state.selected_item = None


# display_recipe関数のテスト
def test_display_recipe(setup_session_state):
    # テスト用データ
    selected_allergies = ['卵', 'ピーナッツ']
    recipe_name = 'ケーキ'
    recipes = [
        {
            'recipe_title': 'イチゴケーキ',
            'recipe_image_url': (
                'https://img.cpcdn.com/recipes/7813040/'
                '894x1461s/952f6a9105c7b1d250853791cc4b08fd?/'
                'u=11756033&p=1714165191'
            ),
            'recipe_ingredients': ['卵', '砂糖', 'バター'],
            'recipe_url': 'https://cookpad.com/recipe/7813040',
        },
        {
            'recipe_title': 'いちごけーき',
            'recipe_image_url': (
                'https://img.cpcdn.com/recipes/7781284/'
                '894x1461s/9b37148a4668a565830b9514d3af1a74?'
                'u=9240495&p=1711003018'
            ),
            'recipe_ingredients': ['卵', '牛乳', 'バニラ'],
            'recipe_url': 'https://cookpad.com/recipe/7781284',
        },
    ]

    # モック化
    with patch('streamlit.title') as mock_title, patch(
        'streamlit.markdown'
    ) as mock_markdown, patch('streamlit.write') as mock_write, patch(
        'streamlit.image'
    ) as mock_image, patch(
        'streamlit.button'
    ) as mock_button, patch(
        'streamlit.rerun'
    ) as mock_rerun:
        # ボタンのクリック動作を設定
        mock_button.side_effect = lambda label, key=None: key == f'{recipe_name}_0'

        # 関数を呼び出し
        display_recipe(selected_allergies, recipe_name, recipes)

        # 関数の動作を検証
        mock_title.assert_any_call('選択されたアレルギー品目')
        mock_markdown.assert_any_call(
            """
    <div
    style='border: 1px solid #ddd; padding:
    10px; border-radius: 5px; background-color: #f9f9f9;'
    >
    卵, ピーナッツ
    </div>
    """,
            unsafe_allow_html=True,
        )

        mock_title.assert_any_call('料理名')
        mock_markdown.assert_any_call(
            """
    <div
    style='border: 1px solid #ddd; padding:
    10px; border-radius: 5px; background-color: #f9f9f9;'
    >
    ケーキ
    </div>
    """,
            unsafe_allow_html=True,
        )

        for index, item in enumerate(recipes):
            mock_write.assert_any_call(f"{index + 1}位  {item['recipe_title']}")
            mock_image.assert_any_call(item['recipe_image_url'], width=300)

        # ボタンがクリックされたか、セッションの状態が更新されたかを確認
        assert st.session_state.page == 'details'
        assert st.session_state.selected_item == recipes[0]

        mock_rerun.assert_called_once()
