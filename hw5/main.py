import re

email_regexp = re.compile(r"^[\w.]+?@(\w+?)[.](\w+?)$")


def check_email(email):
    li = re.split(r'@', email)
    if len(li) > 2:
        return False
    before_at_check = re.match(r"^[\w.]+?$", li[0])
    after_at_check = re.match(r"^(\w+?)[.](\w+?)$", li[1])
    full_check = email_regexp.match(email)
    return bool(before_at_check) and bool(after_at_check) and bool(full_check)


if __name__ == "__main__":
    email = input("Введите email для проверки:")
    print(check_email(email))
