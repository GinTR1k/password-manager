from password_manager.models.password import PasswordModel
from password_manager.vault import Vault


def main():
    # Создание нового хранилища паролей
    vault = Vault()
    vault.create('privet')

    # Проверяем, что оно пустое
    print(f'Хранилище паролей содержит {len(vault.passwords)} паролей: {vault.passwords}')

    # Создаем пароли для гугла
    vault.add_password(PasswordModel(name='Google Russia', url='google.ru', password='qwerty12345'))
    vault.add_password(PasswordModel(name='Google', url='google.com', password='qwerty12345'))
    print('Было создано 2 пароля\n')

    # Проверяем хранилище
    print(
        f'Хранилище паролей содержит {len(vault.passwords)} паролей:',
        '\n' + '\n'.join([password.json() for password in vault.passwords]) + '\n',
    )

    # Ищем пароли
    print(
        'Результат поиска пароля по "google":',
        '\n' + '\n'.join([password.json() for password in vault.find_passwords('google')]) + '\n',
    )
    print(
        'Результат поиска пароля по "google.com":',
        '\n' + '\n'.join([password.json() for password in vault.find_passwords('google.com')]) + '\n',
    )
    print(
        'Результат поиска пароля по "russia":',
        '\n' + '\n'.join([password.json() for password in vault.find_passwords('russia')]) + '\n',
    )

    # Удаление пароля "google.com"
    vault.delete_password(vault.find_passwords('google.com')[0].key)
    print('Удален пароль "google.com"\n')

    # Проверяем хранилище
    print(
        f'Хранилище паролей содержит {len(vault.passwords)} паролей:',
        '\n' + '\n'.join([password.json() for password in vault.passwords]) + '\n',
    )

    # Обновляем пароль
    f = vault.find_passwords('google')[0]
    f.note = 'Google Global for all'
    vault.update_password(f)
    print(f'Обновили пароль {f.name}\n')

    # Проверяем хранилище
    print(
        f'Хранилище паролей содержит {len(vault.passwords)} паролей:',
        '\n' + '\n'.join([password.json() for password in vault.passwords]) + '\n',
    )

    # Заново открываем существующее хранилище
    vault = Vault()
    vault.unlock('privet')
    print('Открыли существующее хранилище')
    print(
        f'Хранилище паролей содержит {len(vault.passwords)} паролей:',
        '\n' + '\n'.join([password.json() for password in vault.passwords]) + '\n',
    )


if __name__ == '__main__':
    main()
