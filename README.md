# BlockList
**BlockList** - приложение, которое позволяет распознать ники с фото и найти их в базе данных, вручную добавлять/обновлять/удалять/искать записи из чёрного списка.
Создано, чтобы облегчить поиск игроков, которые когда-либо мешали игре.

![image](https://github.com/iamzimin/BlackList/assets/94135768/35c24158-1e28-4c98-a404-ddcafa0f1cbe)


В базе хранятся такие поля, как:
- Ник
- Количество заблокированных игр
- Причина блокировки


В списке игроки отмечены:
- красным (количество "Заблокированных игр" больше 0)
- жёлтым (количество "Заблокированных игр" равно 0)
При нажатии "Игра" у всех игроков вычитается 1 из данного поля.

Для более гибкой настройки присутствует config файл.



## Скачать скомпилированную версию BlockList.exe
> https://github.com/iamzimin/BlackList/releases/latest


## Установка
1. ```git pull https://github.com/iamzimin/BlackList.git```
2. Скачайте [Tesseract OCR.exe](https://github.com/UB-Mannheim/tesseract/wiki) и установите в папку репозитория
3. Установите необходимые библиотеки 
```pip install -r requirements.txt```
4. Запустите blackList.py

При необходимости можно скомпилировать проект
```python setup.py build```
