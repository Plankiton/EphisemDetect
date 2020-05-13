from ephisem_detect import prepar_data
from json import dumps

data = {}
for slice_type in ['middle', 'bottom', 'top']:
    print(f':: Preparing {slice_type}')
    data[slice_type] = prepar_data(slice_type = slice_type, slices_dir = 'static/slices')
with open('static/data.json', 'w') as file:
    file.write(dumps(data))
