import requests
import os
import sys

def input_package_info():
    if len(sys.argv) < 4:
        print("Использование: python <path_to_script> <package_name> <result_file_path> <max_depth>")
        sys.exit(1)

    package_name = sys.argv[1]
    result_file_path = sys.argv[2]
    max_depth = int(sys.argv[3])
    return package_name, max_depth, result_file_path

def fetch_package_dependencies(package_name, max_depth, current_depth=0):
    url = f"https://api.nuget.org/v3/registration5-semver1/{package_name}/index.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        dependencies = []

        # Проход по группам зависимостей
        for root in data['items']:
            for groups in root['items']:
                for group in groups['catalogEntry'].get('dependencyGroups', []):
                    if 'dependencies' in group:
                        for dependency in group['dependencies']:
                            dependencies.append({
                                'id': dependency['id'],
                                'range': dependency['range']
                            })

        # Если текущая глубина меньше максимальной, рекурсивно ищем зависимости
        '''if current_depth < max_depth:
            for dep in dependencies:
                # Рекурсивно извлекаем зависимости для каждой найденной
                sub_dependencies = fetch_package_dependencies(dep['id'], max_depth, current_depth + 1)
                dependencies.extend(sub_dependencies)'''

    return dependencies

def generate_plantuml(dependencies):
    """Генерирует код PlantUML для визуализации зависимостей."""
    plantuml_code = "@startuml\n"
    
    for dep in dependencies:
        plantuml_code += f"'{dep['id']}' --> '{dep['range']}'\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def main():
    # Получаем информацию о пакете от пользователя
    package_name, max_depth, result_file_path = input_package_info()

    # Извлекаем зависимости из API NuGet
    dependencies = fetch_package_dependencies(package_name, max_depth)

    # Генерация кода PlantUML
    plantuml_code = generate_plantuml(dependencies)

    # Запись кода в файл
    with open(result_file_path, 'w') as f:
        f.write(plantuml_code)

if __name__ == "__main__":
    main()
