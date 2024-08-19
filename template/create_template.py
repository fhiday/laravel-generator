import os

def generate_create_template(table, dbname):
    template = f"""@extends('layouts.app')

@section('content')
    <div class="container">
        
        @if (session('success'))
            <div class="alert alert-success">
                {{{{ session('success') }}}}
            </div>
        @endif
        <div class="card mb-4">
            <div class="card-body">
                <form action="{{{{ route('{table.name}.store') }}}}" method="POST">
                    @csrf
                    {''.join([f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><input type="{get_input_type(table.columns[col])}" name="{col}" id="{col}" class="form-control" required></div>' if not table.columns[col].foreign_keys else f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><select name="{col}" id="{col}" class="form-control" required> <option value="">Select {col.capitalize()}</option>  {get_foreign_key_select(table.columns[col])} </select></div>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                    <a href="{{{{ route('{table.name}.index') }}}}" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </a>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
@endsection
"""

    output_dir = os.path.join(os.path.dirname(__file__), '../output/'+dbname+'/resources/views/{table.name}'.format(table=table))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, 'create.blade.php'), "w") as file:
        file.write(template)

def get_input_type(column):
    if column.type == 'integer':
        return 'number'
    elif column.type == 'string':
        return 'text'
    elif column.type == 'text':
        return 'textarea'
    elif column.type == 'date':
        return 'date'
    elif column.type == 'boolean':
        return 'checkbox'
    else:
        return 'text'
    
    
def get_foreign_key_select(col):
    if not col.foreign_keys:
        return f'<option value="{{{{ $item->{col.name} }}}}">{{{{ $item->{col.name} }}}}</option>'
    else:
        fk = next(iter(col.foreign_keys))
        return f'@foreach(${fk.column.table.name} as ${fk.column.table.name}_items) \n <option value="{{{{ ${fk.column.table.name}_items->{fk.column.name} }}}}">{{{{ ${fk.column.table.name}_items->{fk.column.name} }}}}</option> \n @endforeach'
    
def get_foreign_key_select_edit(col):
    if not col.foreign_keys:
        return f'<option value="{{{{ $data->{col.name} }}}}">{{{{ $data->{col.name} }}}}</option>'
    else:
        fk = next(iter(col.foreign_keys))
  