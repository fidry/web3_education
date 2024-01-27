# lst = [1, 2, 3, 4, 5]
# filtred_lst = list(filter(lambda x: x % 2, lst))
# print(filtred_lst)

# res = list(map(lambda x: x + 1, lst))
# print(res)


def foo(lst: list = []):
    lst.append(1)
    print(lst)


foo()  # [1]
foo()  # [1, 1]
foo()  # [1, 1, 1]
