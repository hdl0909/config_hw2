import argparse
import requests

def get_package_info_and_dependencies(package_name, repository_url):
    """Получает информацию о пакете, его версиях и зависимостях из NuGet."""
    # Получаем информацию о пакете
    package_info_url = f"{repository_url}/registration5-semver1/{package_name}/index.json"
    response = requests.get(package_info_url)

    if response.status_code != 200:
        print(f"Ошибка при получении данных для пакета {package_name}: {response.status_code}")
        return None

    package_info = response.json()
    dependencies = {}

    # Для каждой версии получаем зависимости
    for item in package_info['items']:
        for version in item['items']:
            version_number = version['catalogEntry']['version']
            dep_url = version['catalogEntry']  # URL для получения дополнительных данных о пакете
            
            # Здесь нужно использовать сам URL из catalogEntry, который вы получили в предыдущем запросе
            dep_response = requests.get(version['catalogEntry']['@id'])

            if dep_response.status_code == 200:
                # Проверяем, что ответ является JSON
                try:
                    dep_data = dep_response.json()
                except ValueError:
                    print(f"Ошибка: ответ не является корректным JSON для версии {version_number}.")
                    continue
                
                deps = dep_data.get('dependencies', [])
                dependencies[version_number] = deps
            else:
                print(f"Ошибка при получении зависимостей для версии {version_number}: {dep_response.status_code}")

    return package_info, dependencies




def recursive_dependencies(package_name, version, repository_url, depth):
    """Рекурсивно получает все зависимости с учетом глубины."""
    if depth < 0:
        return {}

    dependencies = {}
    deps = get_package_info_and_dependencies(package_name, repository_url)[1].get(version, [])
    
    dependencies[version] = deps

    for dep in deps:
        dep_name = dep['id']
        dep_version = dep['version']
        if dep_name not in dependencies:
            nested_deps = recursive_dependencies(dep_name, dep_version, repository_url, depth - 1)
            dependencies.update(nested_deps)

    return dependencies

def generate_plantuml(dependencies):
    """Генерирует код PlantUML для визуализации зависимостей."""
    plantuml_code = "@startuml\n"
    
    for version, deps in dependencies.items():
        for dep in deps:
            plantuml_code += f"'{version}' --> '{dep['id']} {dep['version']}'\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def main():
    ''' parser = argparse.ArgumentParser(description="Визуализатор зависимостей .NET пакета в формате PlantUML")
    parser.add_argument('--path', required=True, help='Путь к программе для визуализации графов')
    parser.add_argument('--package', required=True, help='Имя анализируемого пакета')
    parser.add_argument('--output', required=True, help='Путь к файлу-результату в виде кода')
    parser.add_argument('--depth', type=int, required=True, help='Максимальная глубина анализа зависимостей')
    parser.add_argument('--repo-url', required=True, help='URL-адрес репозитория')

    args = parser.parse_args()

    package_info, dependencies = get_package_info_and_dependencies(args.package, args.repo_url) '''
    
    path = input("Введите путь к программе для визуализации графов: ")
    package = input("Введите имя анализируемого пакета: ")
    output = input("Введите путь к файлу-результату в виде кода: ")
    depth = int(input("Введите максимальную глубину анализа зависимостей: "))
    repo_url = input("Введите URL-адрес репозитория: ")

    package_info, dependencies = get_package_info_and_dependencies(package, repo_url)
    
    if not package_info:
        return

    # Получаем зависимости для всех версий пакета
    all_dependencies = {}
    for version in dependencies:
        #dep_data = recursive_dependencies(args.package, version, args.repo_url, args.depth)
        dep_data = recursive_dependencies(package, version, repo_url, depth)
        all_dependencies.update(dep_data)
        
    if all_dependencies:
        plantuml_code = generate_plantuml(all_dependencies)
        
        # Выводим код на экран
        print(plantuml_code)

        # Сохраняем в файл
        #with open(args.output, 'w') as file:
        with open(output, 'w') as file:
            file.write(plantuml_code)
        #print(f"Код PlantUML сохранен в {args.output}")
        print(f"Код PlantUML сохранен в {output}")
    else:
        print("Зависимости не найдены.")

if __name__ == "__main__":
    main()
