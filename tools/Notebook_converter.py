import nbformat
import re
import os
from nbconvert.exporters import PythonExporter
from traitlets.config import Config


def found_string_in_cell(cell_content, string_to_find):
    """
    :param cell_content: input cell of the notebook to be modified
    :param string_to_find: string to be searched in the input cell's content
    :return: True if string_to_find found in cell_content, False otherwise
    """
    return string_to_find in cell_content


def modify_notebook(input_notebook):
    """ Function to modify path to datafiles, remove use of ipywidgets and replace value
    from ipywdigets by default for converted files """

    new_notebook = nbformat.read(input_notebook, as_version=4)

    all_cells = new_notebook['cells']

    # check if matplotlib is already imported in the notebook
    # if not add it to create plots when modifying the cell's content
    check_import_matplotlib = any(['import matplotlib' in all_cells[i]['source']
                                   for i in range(len(all_cells))
                                   if not ('tags' in all_cells[i]['metadata']
                                           and 'remove_cell' in all_cells[i]['metadata']['tags'])]
                                  )

    for cell_index in range(len(all_cells)):
        # ignore cells marked as "to be removed" when converting
        if 'tags' in all_cells[cell_index]['metadata'] and \
                'remove_cell' in all_cells[cell_index]['metadata']['tags']:
            continue
        else:
            # Convert to dictionary to modify content
            content_to_modify = all_cells[cell_index] #  dict(all_cells[cell_index])

            # add 'import matplotlib.pyplot as plt'
            if 'tags' in all_cells[cell_index]['metadata'] \
                    and 'import_cell' in all_cells[cell_index]['metadata']['tags'] and \
                    not check_import_matplotlib:
                content_to_modify['source'] += '\n' + 'import matplotlib.pyplot as plt' + '\n'

            #
            if 'tags' in all_cells[cell_index]['metadata'] \
                    and 'ipywidgets_data_cell' in all_cells[cell_index]['metadata']['tags']:

                value_of_source = content_to_modify['source'].split('\n')
                for line_index, line in enumerate(value_of_source):
                    if 'method' in line:
                        # lm stands for Levenberg-Marquardt
                        value_of_source[line_index] = "=".join([line.split('=')[0], "'lm',"])
                    elif 'steps' in line:
                        value_of_source[line_index] = "=".join([line.split('=')[0], str(100) + ','])

                content_to_modify['source'] = "\n".join(map(str, value_of_source))

            if 'path_to_data' in content_to_modify['source']:
                value_of_source = content_to_modify['source'].split('\n')
                for line_index, line in enumerate(value_of_source):
                    result = re.search(r'^path_to_data', line)
                    if result:
                        new_line = line.split('=')
                        new_line[-1] = " '../data/'"
                        value_of_source[line_index] = "=".join(new_line)
                content_to_modify['source'] = "\n".join(map(str, value_of_source))

        # Convert to dictionary to modify content
        new_notebook['cells'][cell_index] = nbformat.from_dict(content_to_modify)

    # add 'plt.show()' to display plots when running Python scripts
    all_cells[-1]['source'] += '\n' + 'plt.show()' + '\n'

    return new_notebook


# --------------------------------------------------
# Create configuration for converted Python scripts
config_for_converting = Config()

# convert to Python scripts
config_for_converting.NbConvertApp.export_format = 'script'

# remove empty cells
config_for_converting.RegexRemovePreprocessor.patterns = [r'\s*\Z']

# remove input and output prompts
config_for_converting.TemplateExporter.exclude_input_prompt = True
config_for_converting.TemplateExporter.exclude_output_prompt = True

# configure tag removal: "remove_cell" is a tag present in the cells of the
# notebooks which have to be ignored when converting
config_for_converting.TagRemovePreprocessor.enabled = True
config_for_converting.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)

# configure exporter
config_for_converting.Exporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

# --------------------------------------------------
# loop over notebooks
path = os.path.abspath(os.path.dirname(__file__))
path_to_notebooks = os.path.join(path, '../docs/examples/')

# list notebooks to convert to Python scripts
list_notebooks = [f for f in os.listdir(path_to_notebooks) if os.path.splitext(f)[-1] == '.ipynb']

# folder to store converted files
output_directory = os.path.join(path_to_notebooks, './python_scripts')

for item in list_notebooks:
    new_notebook = modify_notebook(path_to_notebooks + item)

    python_exporter = PythonExporter(config=config_for_converting)
    (body, resources) = python_exporter.from_notebook_node(new_notebook)

    python_filename = os.path.splitext(item)[0] + '.py'

    with open(os.path.join(output_directory, python_filename), 'w') as fout:
        fout.write(body)
