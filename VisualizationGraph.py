import requests
import os

def input_package_info():
    package_name = input("Введите имя анализируемого пакета: ").lower()
    max_depth = int(input("Введите максимальную глубину анализа зависимостей: "))
    result_file_path = input("Введите путь для записи кода PlantUML: ")
    return package_name, max_depth, result_file_path 

def fetch_package_dependencies(package_name):
    # URL для получения метаданных пакета
    url = f"https://api.nuget.org/v3/registration5-semver1/{package_name}/index.json"
    response = requests.get(url)
  
    dependencies = []
    
    if response.status_code == 200:
        data = response.json()

        # Проход по группам зависимостей
        for root in data['items']:
            for groups in root.get('items', []):
                for group in groups['catalogEntry'].get('dependencyGroups', []):
                    if 'dependencies' in group:
                        for dependency in group['dependencies']:
                            dependencies.append({
                                'id': dependency['id'],
                                'range': dependency['range']
                            })
    return dependencies

def build_dependency_graph(package_name, max_depth, current_depth=0, graph=None):
    if graph is None:
        graph = []
    
    if current_depth >= max_depth:
        return graph

    # Получаем зависимости текущего пакета
    dependencies = fetch_package_dependencies(package_name)
    
    for dep in dependencies:
        # Добавляем связь в граф
        graph.append(f"'{package_name}' --> '{dep['id']}'")
        # Рекурсивно получаем зависимости для подзависимостей
        build_dependency_graph(dep['id'], max_depth, current_depth + 1, graph)

    return graph

def generate_plantuml(dependency_graph):
    """Генерирует код PlantUML для визуализации зависимостей."""
    plantuml_code = "@startuml\n"
    plantuml_code += "\n".join(dependency_graph)
    plantuml_code += "\n@enduml"
    return plantuml_code

def main():
    # Получаем информацию о пакете от пользователя
    package_name, max_depth, result_file_path = input_package_info()

    # Генерация графа зависимостей
    dependency_graph = build_dependency_graph(package_name, max_depth)

    # Генерация кода PlantUML
    plantuml_code = generate_plantuml(dependency_graph)

    with open(result_file_path, 'w') as f:
        f.write(plantuml_code)

if __name__ == "__main__":
    main()
