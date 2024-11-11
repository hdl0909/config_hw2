# Описание
Эта программа на Python создает граф зависимостей для указанного пакета .NET (nupkg) в формате PlantUML. Генерация графа позволяет визуализировать зависимости основного пакета и его подзависимостей.
# Установка
1.Установка программы и переход в директорию
```
git clone <URL репозитория>
cd <директория проекта>
```
2.Вывести в виде графа, имея сгенерированный код в формате PlantUML, можно на https://www.plantuml.com/plantuml/uml
3.Убедитесь, что у вас установлен python
4.Создайте и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```
5.Установите необходимы зависимости для тестов
```
pip install pytest
```
# Запуск визуализатора
С готовым конфигурационным файлом config.csv выполнить следующую команду
```
python VisualizationGraph.py
```
# Выходные данные
Программа сгененерирует код в формате PlantUML в указанный текстовый файл
## Пример
![image](https://github.com/user-attachments/assets/d5278087-9e80-4846-9eb3-0fd901126889)
# Тесты
```
pytest -v
```
![image](https://github.com/user-attachments/assets/31cd90e4-5523-432d-b222-e2bf90bfebda)
