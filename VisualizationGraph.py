import requests

def input_package_info():
    package_name = input("Введите имя анализируемого пакета: ").lower()
    max_depth = int(input("Введите максимальную глубину анализа зависимостей: "))
    result_file_path = input("Введите путь для записи кода PlantUML: ")
    return package_name, max_depth, result_file_path 

def fetch_package_dependencies(package_name):
    url = f"https://api.nuget.org/v3/registration5-semver1/{package_name}/index.json"
    response = requests.get(url)
  
    dependencies = []
    
    if response.status_code == 200:
        data = response.json()

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

def build_dependency_graph(package_name, max_depth, current_depth=0, graph=None, visited=None):
    if graph is None:
        graph = []
    if visited is None:
        visited = set()
    
    if current_depth >= max_depth:
        return graph

    dependencies = fetch_package_dependencies(package_name)
    
    for dep in dependencies:
        # Создаем строку для проверки и добавления в граф
        dependency_str = f"\"{package_name}\" -> \"{dep['id']}\" : \"{dep['range']}\""
        
        # Проверяем, если зависимость уже была добавлена, чтобы избежать дублирования
        if dependency_str not in visited:
            graph.append(dependency_str)
            visited.add(dependency_str)
            # Рекурсивно обрабатываем зависимости
            build_dependency_graph(dep['id'], max_depth, current_depth + 1, graph, visited)

    return graph

def generate_plantuml(dependency_graph):
    plantuml_code = "@startuml\n"
    plantuml_code += "\n".join(dependency_graph)
    plantuml_code += "\n@enduml"
    return plantuml_code

def main():
    package_name, max_depth, result_file_path = input_package_info()
    dependency_graph = build_dependency_graph(package_name, max_depth)
    plantuml_code = generate_plantuml(dependency_graph)

    with open(result_file_path, 'w') as f:
        f.write(plantuml_code)

if __name__ == "__main__":
    main()
