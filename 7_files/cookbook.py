class CookBook():
    def __init__(self):
        self.cook_book = {}

    def prt_book(self):
        for dish in self.cook_book.keys():
            print(dish)
            ingredients_lst = self.cook_book[dish]
            for ingredient in ingredients_lst:
                print(f"{ingredient['ingredient_name']:<30} "
                      f"{ingredient['quantity']:5} "
                      f"{ingredient['measure']:<10}")

        return

    def make_cook_book(self, file_name):
        # Формирование словаря блюд

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
        
        with open(file_name, encoding='UTF-8') as f:
            file_lst = f.readlines()

        i = 0

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
                self.cook_book[dish] = ingredients_lst

            i += 1
        return 
    

    def get_dish_ingredients(self, dish):
        # Получение ингредиента и его количества из словаря
        dish_ingredients = self.cook_book[dish]
        result = []
        for ingredient in dish_ingredients:
            result.append(
                (ingredient['ingredient_name'],
                ingredient['quantity'],
                ingredient['measure'])
            )
        return result


def get_shop_list_by_dishes(cook_book, dishes, person_count):
    # Формирование списка продуктов в виде словаря
    dict_out = {}
    for dish in dishes:
        ingredients = cook_book.get_dish_ingredients(dish)
        for ingredient, quantity, measure in ingredients:
            if ingredient in dict_out:
                dict_out[ingredient]['quantity'] += quantity * person_count
            else:
                dict_out[ingredient] = {
                    'measure': measure,
                    'quantity': quantity * person_count,
                }
    return dict_out


def main():
    f_name = r'./files/recipes.txt'
    book = CookBook()
    book.make_cook_book(f_name)
    for k, v in book.cook_book.items():
        print(k)
        print(*v, sep='\n')

    persons = 5
    dishes_lst = ['Омлет', 'Утка по-пекински', 'Фахитос']

    print((f'\nСписок продуктов '
           f'для приготовления {len(dishes_lst)} блюд'))
    print(f'({", ".join(dishes_lst)})')
    print(f'на {persons} человек:\n')

    dish_out = {}
    for dish in dishes_lst:
        ingredients = book.get_dish_ingredients(dish)
        for ingredient, quantity, measure in ingredients:
            if ingredient in dish_out:
                dish_out[ingredient]['quantity'] += quantity * persons
            else:
                dish_out[ingredient] = {
                    'measure': measure,
                    'quantity': quantity * persons,
                }
    for k, v in dish_out.items():
        print(k, v)

if __name__ == "__main__":
    main()
