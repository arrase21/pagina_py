# def dos_sumas(nums, target):
#     dic = {}
#     for i, num in enumerate(nums):
#         if num in dic:
#             return [dic[num], i]
#         else:
#             dic[target - num] = i
#
#
# nums = [3, 2, 4, 50]
# target = 54
# print(dos_sumas(nums, target))


# def palindromo(palabra):
#     return palabra == palabra[::-1]
#
#
# palabra = input("Ingrese palabra: ")
# if palabra == palabra[::-1]:
#     print("Es palindromo")
# else:
#     print("No es palindromo")


numero = int(input("Ingrese un numero=> "))
numero2 = int(input("Ingresa hasta donde mirar la tabla => "))
for i in range(1, numero2 + 1):
    resultado = i * numero
    print(f"{i} x {numero} = {resultado}")
