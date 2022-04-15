from getpass import getpass
from time import sleep
from typing import Collection

import pandas as pd
from tabulate import tabulate

from password_manager.exceptions import MasterPasswordError
from password_manager.models.password import PasswordModel
from password_manager.vault import Vault


class Application:
    def __init__(self):
        self.__vault = Vault()

    def run(self):
        if self.__vault.does_vault_file_exists():
            self.unlock_vault()
        else:
            self.create_vault()

        self._main()

    def unlock_vault(self):
        while True:
            master_password = getpass('Вы пытаетесь открыть существующее хранилище, введите мастер-пароль:\n> ')
            try:
                self.__vault.unlock(master_password)
                print('Хранилище открыто!')
                return
            except MasterPasswordError:
                print('Неверно введен мастер-пароль!')
            finally:
                del master_password

            sleep(0.001)

    def create_vault(self):
        print('Вы создаете новое хранилище...')
        sleep(0.001)

        while True:
            master_password = getpass('Придумайте мастер-пароль:\n>  ')

            if len(master_password) < 4:
                print('Мастер-пароль должен быть не менее 4 символов\n')
                sleep(0.001)
                continue

            master_password2 = getpass('Повторите мастер-пароль:\n>  ')

            if master_password != master_password2:
                print('Мастер-пароли не совпадают!')
                del master_password
                del master_password2
                sleep(0.001)
                continue

            self.__vault.create(master_password)
            print('Хранилище создано!')

            del master_password
            del master_password2

            return

    def _password_list(self):
        print('[Список паролей]')

        if not self.__vault.passwords:
            print('Паролей нет')
            return

        self.pretty_print_passwords(self.__vault.passwords)

    def _search_password(self):
        if not self.__vault.passwords:
            print('Паролей нет')
            return

        while True:
            print('[Поиск пароля]')
            print('Если вы хотите отменить текущее действие, нажмите CTRL+C\n')

            try:
                search = input('Введите название, сайт или примечание:\n> ')
            except KeyboardInterrupt:
                break

            if not search:
                self._password_list()
                continue

            search_result = self.__vault.find_passwords(search)
            self.pretty_print_passwords(search_result)

    def _create_password(self):
        password = PasswordModel()

        while True:
            print('[Добавление пароля]')
            print('Если вы хотите отменить текущее действие, нажмите CTRL+C\n')

            try:
                password.name = input('Название пароля (обязательно):\n> ')
            except KeyboardInterrupt:
                print('Добавление пароля отменено.')
                return

            if password.name:
                break

            print('Название пароля не может быть пустым.')

        while True:
            try:
                password.password = input('Пароль (обязательно):\n> ')
            except KeyboardInterrupt:
                print('Добавление пароля отменено.')
                return

            if password.password:
                break

            print('Пароль не может быть пустым')

        try:
            password.url = input('Адрес сайта, где можно использовать пароль:\n> ')
        except KeyboardInterrupt:
            print('Добавление пароля отменено.')
            return

        try:
            password.note = input('Дополнительная информация по паролю:\n> ')
        except KeyboardInterrupt:
            print('Добавление пароля отменено.')
            return

        self.__vault.add_password(password)

        print('Пароль успешно создан!')

    def update_password(self):
        if not self.__vault.passwords:
            print('Паролей нет')
            return

        while True:
            print('[Редактирование пароля]')
            print('Если вы хотите отменить текущее действие, нажмите CTRL+C\n')

            try:
                search = input('Введите название, сайт или примечание:\n> ')
            except KeyboardInterrupt:
                break

            passwords = self.__vault.find_passwords(search) if search else self.__vault.passwords

            if not passwords:
                print('Паролей не найдено.\n')
                continue

            self.pretty_print_passwords(passwords)

            while True:
                print('Если вы хотите отменить текущее действие (повторить поиск или выйти), нажмите CTRL+C\n')
                try:
                    password_index = input(f'Введите номер пароля (цифра в первой колонке, 0-{len(passwords) -1}):\n> ')
                except KeyboardInterrupt:
                    password_index = None
                    break

                try:
                    password_index = int(password_index)
                except ValueError:
                    print('Извините, введите число.\n')
                    continue

                if not 0 <= password_index < len(passwords):
                    print(f'Выберите число от 0 до {len(passwords) -1} включительно.\n')
                    continue

                break

            if password_index is None:
                continue

            password = passwords[password_index]
            self.pretty_print_passwords([password])

            try:
                input('Вы хотите отредактировать этот пароль? (Enter - да, CTRL+C - нет)\n> ')
            except KeyboardInterrupt:
                continue

            try:
                password.name = input(
                    f'Название пароля (Enter - оставить без изменений):\n[{password.name}] > '
                ) or password.name
            except KeyboardInterrupt:
                print('Изменение пароля отменено.\n')
                continue

            try:
                password.password = input(
                    f'Пароль (Enter - оставить без изменений):\n[{password.password}] > '
                ) or password.password
            except KeyboardInterrupt:
                print('Изменение пароля отменено.\n')
                continue

            try:
                password.url = input(
                    f'Адрес сайта, где можно использовать пароль (Enter - оставить без изменений):\n[{password.url}] > '
                )
            except KeyboardInterrupt:
                print('Изменение пароля отменено.\n')
                continue

            try:
                password.note = input(
                    f'Дополнительная информация по паролю (Enter - оставить без изменений):\n[{password.note}] > ',
                )
            except KeyboardInterrupt:
                print('Изменение пароля отменено.\n')
                continue

            self.__vault.update_password(password)
            print('Пароль отредактирован!')
            return

    def _delete_password(self):
        if not self.__vault.passwords:
            print('Паролей нет')
            return

        while True:
            print('[Удаление пароля]')
            print('Если вы хотите отменить текущее действие, нажмите CTRL+C\n')

            try:
                search = input('Введите название, сайт или примечание:\n> ')
            except KeyboardInterrupt:
                break

            passwords = self.__vault.find_passwords(search) if search else self.__vault.passwords

            if not passwords:
                print('Паролей не найдено.\n')
                continue

            self.pretty_print_passwords(passwords)

            while True:
                print('Если вы хотите отменить текущее действие (повторить поиск или выйти), нажмите CTRL+C\n')
                try:
                    password_index = input(f'Введите номер пароля (цифра в первой колонке, 0-{len(passwords) -1}):\n> ')
                except KeyboardInterrupt:
                    password_index = None
                    break

                try:
                    password_index = int(password_index)
                except ValueError:
                    print('Извините, введите число.\n')
                    continue

                if not 0 <= password_index < len(passwords):
                    print(f'Выберите число от 0 до {len(passwords) -1} включительно.\n')
                    continue

                break

            if password_index is None:
                continue

            password = passwords[password_index]
            self.pretty_print_passwords([password])

            try:
                input('Вы хотите удалить этот пароль? (Enter - да, CTRL+C - нет)\n> ')
            except KeyboardInterrupt:
                continue

            self.__vault.delete_password(password.key)
            print('Пароль удален!')
            return

    def _main(self):
        while True:
            print('\n[Главное меню] Выберите действие:')
            print('0 - Выход')
            print('1 - Посмотреть пароли')
            print('2 - Найти пароль')
            print('3 - Редактировать пароль')
            print('4 - Создать пароль')
            print('5 - Удалить пароль')

            user_input = input('> ')
            print()

            try:
                user_input = int(user_input)
            except ValueError:
                print('Извините, введите число.')
                continue

            match user_input:
                case 0:
                    break
                case 1:
                    self._password_list()
                case 2:
                    self._search_password()
                case 3:
                    self.update_password()
                case 4:
                    self._create_password()
                case 5:
                    self._delete_password()
                case _:
                    print('Выберите число от 0 до 5 включительно.')
                    continue

    @staticmethod
    def pretty_print_passwords(passwords: Collection[PasswordModel]):
        df = pd.DataFrame(
            (password.dict().values() for password in passwords),
            columns=(
                'key',
                'Название',
                'Пароль',
                'Сайт',
                'Примечание',
                'Создано',
                'Отредактировано',
            ),
        )
        del df['key']
        print(tabulate(df, headers='keys', tablefmt='psql'))
        print()


if __name__ == '__main__':
    app = Application()

    try:
        app.run()
    except KeyboardInterrupt:
        pass
