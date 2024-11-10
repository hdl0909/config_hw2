import unittest
from unittest.mock import patch, MagicMock
import requests
import os

# Импортируем функции, которые будем тестировать
from VisualizationGraph import (
    input_package_info,
    fetch_package_dependencies,
    build_dependency_graph,
    generate_plantuml
)

class TestDependencyAnalyzer(unittest.TestCase):
    
    @patch('builtins.input', side_effect=["TestPackage", "2", "output.txt"])
    def test_input_package_info(self, mock_input):
        package_name, max_depth, result_file_path = input_package_info()
        self.assertEqual(package_name, "testpackage")
        self.assertEqual(max_depth, 2)
        self.assertEqual(result_file_path, "output.txt")

    @patch('requests.get')
    def test_fetch_package_dependencies(self, mock_get):
        # Настраиваем mock-ответ от requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "items": [
                        {
                            "catalogEntry": {
                                "dependencyGroups": [
                                    {
                                        "dependencies": [
                                            {"id": "Dep1", "range": "1.0.0"},
                                            {"id": "Dep2", "range": "2.0.0"}
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        dependencies = fetch_package_dependencies("TestPackage")
        self.assertEqual(len(dependencies), 2)
        self.assertEqual(dependencies[0]["id"], "Dep1")
        self.assertEqual(dependencies[0]["range"], "1.0.0")
        self.assertEqual(dependencies[1]["id"], "Dep2")
        self.assertEqual(dependencies[1]["range"], "2.0.0")

    @patch('VisualizationGraph.fetch_package_dependencies')
    def test_build_dependency_graph(self, mock_fetch_dependencies):
        # Настраиваем mock-ответ от fetch_package_dependencies
        mock_fetch_dependencies.side_effect = [
            [{"id": "Dep1", "range": "1.0.0"}],  # Первый вызов
            []  # Второй вызов для "Dep1" (нет подзависимостей)
        ]
        
        graph = build_dependency_graph("TestPackage", max_depth=2)
        
        self.assertEqual(len(graph), 1)
        self.assertEqual(graph[0], "'TestPackage' --> 'Dep1'")

    def test_generate_plantuml(self):
        # Проверяем, что функция возвращает корректный PlantUML код
        graph = ["'TestPackage' --> 'Dep1'", "'Dep1' --> 'Dep2'"]
        plantuml_code = generate_plantuml(graph)
        expected_code = "@startuml\n'TestPackage' --> 'Dep1'\n'Dep1' --> 'Dep2'\n@enduml"
        self.assertEqual(plantuml_code, expected_code)

    @patch('VisualizationGraph.open', new_callable=unittest.mock.mock_open)
    @patch('VisualizationGraph.input_package_info')
    @patch('VisualizationGraph.build_dependency_graph')
    @patch('VisualizationGraph.generate_plantuml')
    def test_main(self, mock_generate_plantuml, mock_build_dependency_graph, mock_input_package_info, mock_open):
        # Настраиваем возвращаемые значения для mock-функций
        mock_input_package_info.return_value = ("TestPackage", 2, "output.txt")
        mock_build_dependency_graph.return_value = ["'TestPackage' --> 'Dep1'"]
        mock_generate_plantuml.return_value = "@startuml\n'TestPackage' --> 'Dep1'\n@enduml"
        
        # Запускаем main и проверяем, что файл был записан корректно
        from VisualizationGraph import main
        main()

        mock_open.assert_called_once_with("output.txt", 'w')
        mock_open().write.assert_called_once_with("@startuml\n'TestPackage' --> 'Dep1'\n@enduml")


if __name__ == "__main__":
    unittest.main()
