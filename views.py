import os
from sqlalchemy import inspect

def generate_view(table):
    os.makedirs(f"output/resources/views/{table.name}", exist_ok=True)
    
    # Template view index
    index_template = f"""@extends('layouts.app')

@section('content')
    <div class="container">
        
        @if (session('success'))
            <div class="alert alert-success">
                {{{{ session('success') }}}}
            </div>
        @endif
        @can('{table.name}-create')
        <a href="{{{{ route('{table.name}.create') }}}}" class="btn btn-primary mb-3">Create New</a>
        @endcan
        <form action="" method="GET">
            <div class="input-group mb-3">
                <input type="text" name="search" class="form-control" placeholder="Search...">
                <button class="btn btn-primary" type="submit">Search</button>
            </div>
        </form>
        @if ($data->isEmpty())
            <div class="alert alert-warning">No data available.</div>
            @if(Request::input('search'))
                <a href="{{{{ route('{table.name}.create') }}}}" class="btn btn-secondary btn-sm mb-3">
                <i class="bi bi-chevron-left"></i> Back
                </a>
            @endif
        @else
            <div class="card mb-4">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead class="thead-light">
                                <tr>
                                    {''.join([f'<th>{col}</th>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($data as $item)
                                    <tr>
                                        {''.join([f'<td>{{{{ $item->{col} }}}}</td>' if not table.columns[col].foreign_keys else f'<td>{{ $item->{col}->related_model_name }}</td>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                                        <td>
                                            @can('{table.name}-edit')
                                            <a href="{{{{ route('{table.name}.edit', $item->id) }}}}" class="btn btn-warning btn-sm">Edit</a>
                                            @endcan
                                            @can('{table.name}-delete')
                                            <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{{{ $item->id }}}}">Delete</button>
                                            @endcan
                                            <div class="modal fade" id="deleteModal{{{{ $item->id }}}}" tabindex="-1" aria-labelledby="deleteModalLabel{{{{ $item->id }}}}" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="deleteModalLabel{{{{ $item->id }}}}">Confirm Delete</h5>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Are you sure you want to delete this item?
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                                            <form action="{{{{ route('{table.name}.destroy', $item->id) }}}}" method="POST" style="display:inline;">
                                                                @csrf
                                                                @method('DELETE')
                                                                <button type="submit" class="btn btn-danger">Delete</button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    {{{{ $data->links('pagination::bootstrap-5') }}}}
                </div>
            </div>
        @endif
    </div>
@endsection
"""
    with open(f"output/resources/views/{table.name}/index.blade.php", "w") as file:
        file.write(index_template)
    
    # Template view create
    create_template = f"""@extends('layouts.app')

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
                    {''.join([f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><input type="{get_input_type(table.columns[col])}" name="{col}" id="{col}" class="form-control" required></div>' if not table.columns[col].foreign_keys else f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><select name="{col}" id="{col}" class="form-control" required> {col}_options </select></div>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
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
    with open(f"output/resources/views/{table.name}/create.blade.php", "w") as file:
        file.write(create_template)
    
    # Template view edit
    edit_template = f"""@extends('layouts.app')

@section('content')
    <div class="container">
       
        @if (session('success'))
            <div class="alert alert-success">
                {{{{ session('success') }}}}
            </div>
        @endif
        <div class="card mb-4">
            <div class="card-body">
                <form action="{{{{ route('{table.name}.update', $data->id) }}}}" method="POST">
                    @csrf
                    @method('PATCH')
                    {''.join([f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><input type="{get_input_type(table.columns[col])}" name="{col}" id="{col}" class="form-control" value="{{{{ $data->{col} }}}}" required></div>' if not table.columns[col].foreign_keys else f'<div class="mb-3"><label for="{col}" class="form-label">{col.capitalize()}</label><select name="{col}" id="{col}" class="form-control" required> {col}_options </select></div>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                    <a href="{{{{ route('{table.name}.index') }}}}" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </a>
                    <button type="submit" class="btn btn-primary">Update</button>
                </form>
            </div>
        </div>
    </div>
@endsection
"""
    with open(f"output/resources/views/{table.name}/edit.blade.php", "w") as file:
        file.write(edit_template)
    
    # Template view show
    show_template = f"""@extends('layouts.app')

@section('content')
    <div class="container">
        
        @if (session('success'))
            <div class="alert alert-success">
                {{{{ session('success') }}}}
            </div>
        @endif
        <div class="card mb-4">
            <div class="card-body">
                {''.join([f'<p><strong>{col.capitalize()}:</strong> {{{{ $data->{col} }}}}</p>' if not table.columns[col].foreign_keys else f'<p><strong>{col.capitalize()}:</strong> {{{{ $data->{col}->related_model_name }}}}</p>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
            </div>
        </div>
        <a href="{{{{ route('{table.name}.edit', $data->id) }}}}" class="btn btn-warning">Edit</a>
        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{{{ $data->id }}}}">Delete</button>
        <div class="modal fade" id="deleteModal{{{{ $data->id }}}}" tabindex="-1" aria-labelledby="deleteModalLabel{{{{ $data->id }}}}" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteModalLabel{{{{ $data->id }}}}">Confirm Delete</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete this item?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <form action="{{{{ route('{table.name}.destroy', $data->id) }}}}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection
"""
    with open(f"output/resources/views/{table.name}/show.blade.php", "w") as file:
        file.write(show_template)

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