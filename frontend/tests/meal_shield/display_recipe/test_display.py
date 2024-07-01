from streamlit.testing.v1 import AppTest
from meal_shield.display_recipi import display_recipi


def test_display():
    at = AppTest.from_file('tests/meal_shield/show.py').run()
    at.secrets['WORD'] = 'Foobar'
    
    at.run()
    assert not at.exception
    
    at.run()
    
    selected_allergies = ['卵', 'ピーナッツ']
    recipi_name = 'ケーキ'
    result = [
        {
            'recipe_title': 'イチゴケーキ',
            'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/'
                                '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=11756033&p=1714165191',
            'recipe_ingredients': ['卵', '砂糖', 'バター'],
            'recipe_url': 'https://cookpad.com/recipe/7813040',
        },
        {
            'recipe_title': 'いちごけーき',
            'recipe_image_url': 'https://img.cpcdn.com/recipes/7781284/'
                                '894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495&p=1711003018',
            'recipe_ingredients': ['卵', '牛乳', 'バニラ'],
            'recipe_url': 'https://cookpad.com/recipe/7781284',
        },
    ]
    
    display_recipi(selected_allergies, recipi_name, result)
    
    button_key = f'ケーキ_0'  
    at.button(key=button_key).click().run()
    
    assert at.session_state.page == 'details'
    assert at.session_state.selected_item is not None
    assert at.session_state.selected_item['recipe_title'] == 'イチゴケーキ'
    
