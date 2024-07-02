from streamlit.testing.v1 import AppTest

from meal_shield.display_recipi import display_recipi


def test_display():
    at = AppTest.from_file('tests/meal_shield/show_wrapper.py').run()
    at.secrets['WORD'] = 'Foobar'
    at.run()
    # テスト実行ちゅに例外が発生しないか確認
    assert not at.exception
    # テスト用データ
    selected_allergies = ['卵', 'ピーナッツ']
    recipi_name = 'ケーキ'
    result = [
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

    # display_recipi関数を呼び出し
    display_recipi(selected_allergies, recipi_name, result)
    # 生成されたボタンを押す
    button_key = f'{recipi_name}_0'
    at.button(key=button_key).click().run()
    # ページがdetailsであることを確認する
    assert at.session_state.page == 'details'
    # 選択されたアイテムがあることを確認
    assert at.session_state.selected_item is not None
    # タイトルがイチゴケーキか確認
    assert at.session_state.selected_item['recipe_title'] == 'イチゴケーキ'
