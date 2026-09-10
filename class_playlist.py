class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, name, duration):
        self.songs.append({
            "name": name,
            "duration": duration
        })

    def remove_song(self, name):
        for index, song in enumerate(self.songs):
            if song["name"] == name:
                del self.songs[index]
                return True
        return False

    def total_duration(self):
        return sum(song["duration"] for song in self.songs)

    def __len__(self):
        return len(self.songs)

    def show_songs(self):
        if not self.songs:
            print("Плейлист пуст.")
            return

        for number, song in enumerate(self.songs, start=1):
            print(f'{number}. {song["name"]} — {song["duration"]} сек.')


def main():
    playlist = Playlist()

    while True:
        print("\nМеню:")
        print("1. Добавить песню")
        print("2. Удалить песню")
        print("3. Узнать общую продолжительность")
        print("4. Узнать количество песен")
        print("5. Показать все песни")
        print("0. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            name = input("Название песни: ").strip()

            if not name:
                print("Название не должно быть пустым.")
                continue

            try:
                duration = int(input("Продолжительность в секундах: "))
            except ValueError:
                print("Введите целое число.")
                continue

            if duration <= 0:
                print("Продолжительность должна быть больше нуля.")
                continue

            playlist.add_song(name, duration)
            print("Песня добавлена.")

        elif choice == "2":
            name = input("Название песни для удаления: ").strip()

            if playlist.remove_song(name):
                print("Песня удалена.")
            else:
                print("Песня с таким названием не найдена.")

        elif choice == "3":
            print(
                "Общая продолжительность:",
                playlist.total_duration(),
                "сек."
            )

        elif choice == "4":
            print("Количество песен:", len(playlist))

        elif choice == "5":
            playlist.show_songs()

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Неизвестная команда. Выберите пункт от 0 до 5.")


if __name__ == "__main__":
    main()
