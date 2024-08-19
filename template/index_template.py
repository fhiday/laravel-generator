import os

def generate_index_template(table, dbname):
    def get_foreign_key_column(col):
        if not col.foreign_keys:
            return col.name
        else:
            fk = next(iter(col.foreign_keys))
            return f"{fk.column.table.name}->{fk.column.name}"
        

    template = f"""@extends('layouts.app')

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
                <a href="{{{{ route('{table.name}.index') }}}}" class="btn btn-secondary btn-sm mb-3">
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
                                        {''.join([f'<td>{{{{ $item->{col} }}}}</td>' if not table.columns[col].foreign_keys else f'<td>{{{{ $item->{get_foreign_key_column(table.columns[col])} }}}}</td>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                @can('{table.name}-list')
                                                    <a href="{{{{ route('{table.name}.show', $item->id) }}}}" class="btn btn-primary btn-sm">Show</a>
                                                @endcan
                                                @can('{table.name}-edit')
                                                    <a href="{{{{ route('{table.name}.edit', $item->id) }}}}" class="btn btn-warning btn-sm">Edit</a>
                                                @endcan
                                                @can('{table.name}-delete')
                                                    <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{{{ $item->id }}}}">Delete</button>
                                                @endcan
                                            </div>
                                            <div class="modal fade" id="deleteModal{{{{ $item->id }}}}" tabindex="-1" aria-labelledby="deleteModalLabel{{{{ $item->id }}}}" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="deleteModalLabel{{{{ $item->id }}}}>Confirm Delete</h5>
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

    output_dir = os.path.join(os.path.dirname(__file__), '../output/'+dbname+'/resources/views/{table.name}'.format(table=table))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, 'index.blade.php'), "w") as file:
        file.write(template)