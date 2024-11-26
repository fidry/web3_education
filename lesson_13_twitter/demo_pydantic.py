from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    field_validator,
    model_validator,
    EmailStr,
    RootModel
)
# pip install 'pydantic[email]'


# ----------------------------------------------------------------------------------------


# class City(BaseModel):
#     city_id: int
#     name: str
#     population: int


# input_json_1 = '''
#     {
#         "city_id": 123,
#         "name": "Amsterdam",
#         "population": 1000000
#     }
# '''

# input_json_2 = '''
#     {
#         "city_id": 123,
#         "name": "Amsterdam",
#         "population": "1000000"
#     }
# '''

# input_json_3 = '''
#     {
#         "city_id": 123,
#         "name": "Amsterdam",
#         "population": "lalala"
#     }
# '''

# city_1 = City.model_validate_json(input_json_1)
# print(city_1)
# print(city_1.city_id)
# print(city_1.name)
# print(city_1.population)

# city_2 = City.model_validate_json(input_json_2)
# print(city_2)
# print(city_2.city_id)
# print(city_2.name)
# print(city_2.population)
# print(city_2.population)

# city_3 = City.model_validate_json(input_json_3)
# try:
#     city_3 = City.model_validate_json(input_json_3)
# except ValidationError as err:
#     print(err.json())

# ----------------------------------------------------------------------------------------


# class Tag(BaseModel):
#     id: int
#     tag: str
#
#
# class City(BaseModel):
#     city_id: int
#     name: str
#     tags: list[Tag]
#
#
# input_json_4 = '''
#     {
#         "city_id": 123,
#         "name": "Amsterdam",
#         "tags": [
#             {
#                 "id": 1,
#                 "tag": "nice :)"
#             },
#             {
#                 "id": 2,
#                 "tag": "very nice :)"
#             }
#         ]
#     }
# '''
#
# city_4 = City.model_validate_json(input_json_4)
# print(city_4)
# print(city_4.tags)
# print(city_4.tags[0])
# print(city_4.tags[0].tag)

# tag = city_4.tags[0]
# print(tag)
# print(tag.model_dump_json())


# ----------------------------------------------------------------------------------------


# class City(BaseModel):
#     city_id: int
#     name: str = Field(alias='cityFullName')
#
#
# input_json_5 = '''
#     {
#         "city_id": 123,
#         "cityFullName": "Amsterdam"
#     }
# '''
#
# city_5 = City.model_validate_json(input_json_5)
# print(city_5)
# print(city_5.city_id)
# print(city_5.name)
#
# print(city_5.model_dump_json())
# print(city_5.model_dump_json(by_alias=True))
# print(city_5.model_dump_json(by_alias=True, exclude={'city_id'}))


# ----------------------------------------------------------------------------------------


# class UserWithoutPassword(BaseModel):
#     name: str
#     email: str
#
#
# class User(UserWithoutPassword):
#     password: str


# ----------------------------------------------------------------------------------------


# class City(BaseModel):
#     city_id: int
#     name: str = Field(alias='cityFullName')
#
#     @field_validator('name')
#     def name_should_be_capitalize(cls, v: str) -> str:
#         if not v[0].isupper():
#             raise ValueError('Name need to be capitalize')
#         return v
#
#
# input_json_6 = '''
#     {
#         "city_id": 123,
#         "cityFullName": "amsterdam"
#     }
# '''
#
# city_6 = City.model_validate_json(input_json_6)
# print(city_6)
# print(city_6.city_id)
# print(city_6.name)


# ----------------------------------------------------------------------------------------


# class City(BaseModel):
#     city_id: int
#     name: str = Field(alias='cityFullName')
#
#     @model_validator(mode='before')
#     def name_should_be_capitalize(cls, data: ...) -> ...:
#         print('data:', data)
#
#         if isinstance(data, dict):
#             assert (
#                     'city_id' in data
#             ), 'city_id should be included'
#
#         return data
#
#
# input_json_6 = '''
#     {
#         "city_id": 123,
#         "cityFullName": "Amsterdam"
#     }
# '''
#
# city_6 = City.model_validate_json(input_json_6)
# print(city_6)


# ----------------------------------------------------------------------------------------

# '''
# Работа с объектами, а не со строками
# '''
#
# input_json_7 = {
#     'BMW': {
#         'color': 'black',
#         'dealer': 'bmw@gmail.com',
#     },
#     'mercedes': {
#         'color': 'white',
#         'dealer': 'mercedes@gmail.com',
#     },
#     'audi': {
#         'color': 'red',
#         'dealer': 'audi@gmail.com',
#     },
# }
#
#
# class CarModel(BaseModel):
#     color: str
#     dealer: EmailStr
#
#
# class CarsModel(RootModel[dict[str, CarModel]]):
#     pass
#
#
# '''
# Класс RootModel в Pydantic используется для создания моделей,
# которые непосредственно представляют собой базовые типы данных (например, списки, словари и т.д.),
# а не объекты с атрибутами.
# Оно позволяет вам определять схемы, в которых верхний уровень структуры JSON не является объектом с именованными полями,
# а представляет собой коллекцию значений.
#
# Эта модель теперь наследует от RootModel, где указывается,
# что корнем модели является словарь с ключами строкового типа и значениями типа UserModel.
# '''
#
#
# cars = CarsModel.model_validate(input_json_7)
# print(cars)
# print(cars.root)
# print(list(cars.root.keys()))
# print(cars.root['BMW'].dealer)


# ----------------------------------------------------------------------------------------
# '''
# Пример с вложенным списком
# '''
#
#
# class Item(BaseModel):
#     name: str
#     value: int
#
#
# class ItemsModel(RootModel[list[Item]]):
#     pass
#
#
# input_json_8 = [
#     {"name": "item1", "value": 100},
#     {"name": "item2", "value": 200}
# ]
#
# items = ItemsModel.model_validate(input_json_8).root
# print(items)
