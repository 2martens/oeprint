import json

from client.config import Config

__author__ = "Jim Martens"


class DataStorage:
    """
    Holds the data which is synchronized with the server.
    """
    def __init__(self):
        self._config = Config()
        self._file = self._config.get('Data', 'file')
        self._rawData = self._load_file()
        self._processedData = self._process_data()

    def get_configurations(self) -> dict:
        """
        Returns the configurations.
        """
        return self._processedData.get("configurations")

    def get_materials(self) -> dict:
        """
        Returns the materials.
        """
        return self._processedData.get("materials")

    def get_material(self, name):
        for material in self._processedData.get("materials"):
            result = self._processedData.get("materials")[material].get_material(name)
            if result is not None:
                return result
        return None

    def get_raw_material(self, materials : dict, name):
        for material in materials:
            result = materials[material].get_material(name)
            if result is not None:
                return result
        return None

    def _process_data(self) -> dict:
        """
        Processes the raw JSON data and transforms it into Python objects.
        """
        raw_materials = self._rawData["materials"]
        final_materials = {}

        for material in raw_materials:
            # TODO change this to proper handling of the pages
            new_material = Material(material["name"], material["filename"])
            for sub_material in material["children"]:
                self._process_submaterial(new_material, sub_material)
            final_materials[new_material.get_name()] = new_material

        raw_configurations = self._rawData["configurations"]
        final_configurations = {}

        for configuration in raw_configurations:
            new_configuration = Configuration(configuration["name"])
            materials = configuration["materials"]
            for material in materials:
                name = material["name"]
                amount = material["amount"]
                new_configuration.add_material(self.get_raw_material(final_materials, name), amount)
            final_configurations[new_configuration.get_name()] = new_configuration

        # second run to process the sub configurations
        for configuration in raw_configurations:
            current_configuration = final_configurations[configuration["name"]] # type: Configuration
            for sub_configuration in configuration["configurations"]:
                current_configuration.add_configuration(
                    final_configurations[sub_configuration["name"]],
                    sub_configuration["amount"]
                )

        data = {
            "configurations": final_configurations,
            "materials": final_materials
        }

        return data

    def _process_submaterial(self, new_material, sub_material):
        new_sub_material = Material(sub_material["name"], sub_material["filename"])
        new_material.add_material(new_sub_material)
        for material in sub_material["children"]:
            self._process_submaterial(new_sub_material, material)

    def _load_file(self):
        with open(self._file, 'r', encoding='utf-8') as file:
            return json.load(file)


class Configuration:
    """
    Represents a configuration.
    """

    def __init__(self, name: str):
        """
        Initializes a configuration.
        :param name: the name
        """
        self._name = name
        self._configurations = []
        self._configPrintAmounts = {}
        self._materials = []
        self._materialPrintAmounts = {}

    def get_name(self) -> str:
        """
        Returns the name of this configuration.
        """
        return self._name

    def get_configurations(self) -> list:
        """
        Returns the child configurations.
        """
        return self._configurations

    def get_config_print_amounts(self) -> dict:
        """
        Returns the print amounts for all child configurations.
        """
        return self._configPrintAmounts

    def add_configuration(self, configuration: 'Configuration', print_amount: int = 1):
        """
        Adds a configuration.
        :param configuration: to be added configuration
        :param print_amount: how often the new configuration should be printed
        """
        self._configurations.append(configuration)
        self._configPrintAmounts[configuration.get_name()] = print_amount

    def set_config_print_amount(self, configuration: 'Configuration', print_amount: int) -> bool:
        """
        Sets the print amount for given configuration (must be added already).
        :param configuration: configuration with new print amount
        :param print_amount: new print amount
        """

        if self._configurations.count(configuration) > 0:
            self._configPrintAmounts[configuration.get_name()] = print_amount
            return True
        else:
            return False

    def remove_configuration(self, configuration: 'Configuration') -> bool:
        """
        Removes given configuration if existing.
        :param configuration: to be removed configuration
        """
        try:
            self._configurations.remove(configuration)
            del self._configPrintAmounts[configuration.get_name()]
            return True
        except ValueError:
            return False
        except KeyError:
            return False

    def get_materials(self) -> list:
        """
        Returns the materials.
        :return: materials
        """
        return self._materials

    def get_material_print_amounts(self) -> dict:
        """
        Returns the print amounts for all materials.
        :return: print amounts of materials
        """
        return self._materialPrintAmounts

    def add_material(self, material: 'Material', print_amount: int = 1):
        """
        Adds a material
        :param material: to be added material
        :param print_amount: how often should be material be printed
        """
        self._materials.append(material)
        self._materialPrintAmounts[material.get_name()] = print_amount

    def set_material_print_amount(self, material: 'Material', print_amount: int) -> bool:
        """
        Sets the print amount for given material (must be added already).
        :param material: material with new print amount
        :param print_amount: new print amount
        """

        if self._materials.count(material) > 0:
            self._materialPrintAmounts[material.get_name()] = print_amount
            return True
        else:
            return False

    def remove_material(self, material: 'Material') -> bool:
        """
        Removes given material if existing.
        :param material: to be removed material
        """
        try:
            self._materials.remove(material)
            del self._materialPrintAmounts[material.get_name()]
            return True
        except ValueError:
            return False
        except KeyError:
            return False


class Material:
    """
    Represents a material.
    """

    def __init__(self, name: str, filename: str, pages: list = None):
        """
        Initializes a material
        :param name: the name of the material
        :param filename: the filename for this material
        :param pages: the page numbers for this material
        """
        self._materials = []
        self._name = name
        self._filename = filename
        self._pages = pages

    def get_name(self) -> str:
        """
        Returns the name of this material.
        """
        return self._name

    def get_filename(self) -> str:
        """
        Returns the filename for this material.
        """
        return self._filename

    def get_pages(self) -> list:
        """
        Returns the page numbers for this material.
        """
        return self._pages

    def get_materials(self) -> list:
        """
        Returns the child materials.
        """
        return self._materials

    def get_material(self, name):
        if self._name == name:
            return self
        for material in self.get_materials():
            result = material.get_material(name)
            if result is not None:
                return result
        return None

    def add_material(self, material: 'Material'):
        """
        Adds a material.
        :param material: to be added material
        """
        self._materials.append(material)

    def remove_material(self, material: 'Material') -> bool:
        """
        Removes given material if existing.
        :param material: to be removed material
        """
        try:
            self._materials.remove(material)
            return True
        except ValueError:
            return False
