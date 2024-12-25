def make_cook_book(file_name):
    # Формирование словаря блюд
    i = 0
    book = {}
    file_lst = read_cook_book(file_name)

    while i < len(file_lst):
        if file_lst[i].strip():
            dish = file_lst[i].strip()
            i += 1
            ingredients_number = int(file_lst[i])
            i += 1
            ingredients_lst = []
            for j in range(i, i+ingredients_number):
                ingredients_lst.append(make_ingredient_dict(file_lst[j]))
                i += 1
            book[dish] = ingredients_lst

        i += 1
    return book


def read_cook_book(file_name):
    # Формирование списка строк из текстового файла
    with open(file_name, encoding='UTF-8') as f:
        lst = f.readlines()
    return lst


def make_ingredient_dict(string, delimiter='|'):
    # Формирование словаря ингредиента из строки
    ingredient_name, quantity, measure = string.split(delimiter)
    ingredient_name = ingredient_name.strip()
    quantity = int(quantity.strip())
    measure = measure.strip().replace('\n', '')
    return {
        'ingredient_name': ingredient_name,
        'quantity': quantity,
        'measure': measure,
    }


def get_dish_ingredients(dish_ingredients):
    # Получение ингредиента и его количества из словаря
    result = []
    for ingredient in dish_ingredients:
        result.append(
            (ingredient['ingredient_name'],
             ingredient['quantity'],
             ingredient['measure'])
        )
    return result


def get_shop_list_by_dishes(dishes, person_count):
    # Формирование списка продуктов в виде словаря
    dict_out = {}
    for dish in dishes:
        ingredients = get_dish_ingredients(cook_book[dish])
        for ingredient, quantity, measure in ingredients:
            if ingredient in dict_out:
                dict_out[ingredient]['quantity'] += quantity * person_count
            else:
                dict_out[ingredient] = {
                    'measure': measure,
                    'quantity': quantity * person_count,
                }
    return dict_out


filename = './files/recipes.txt'
cook_book = make_cook_book(filename)
print('Кулинарная книга:')

for k, v in cook_book.items():
    print(k)
    print(*v, sep='\n')

persons = 5
dishes_lst = ['Омлет', 'Утка по-пекински', 'Фахитос']
print((f'\nСписок продуктов'
       f'для приготовления {len(dishes_lst)} блюд'))
print(f'({", ".join(dishes_lst)})')
print(f'на {persons} человек:\n')

product_dict = get_shop_list_by_dishes(dishes_lst, 5)
for k, v in product_dict.items():
    print(k, v)
    # print(v, sep='\n')
# for product, qty in sorted(product_dict.items()):
#     print((f'{product}: {qty["quantity"]} {qty["measure"]}'))
