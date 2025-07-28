from functions.get_files_info import get_files_info

current_directory_result = get_files_info("calculator", ".")
print(current_directory_result)
print()

pkg_directory_result = get_files_info("calculator", "pkg")
print(pkg_directory_result)
print()

bin_result = get_files_info("calculator", "/bin")
print(bin_result)
print()

parent_result = get_files_info("calculator", "../")
print(parent_result)
print()

print("Success!")
