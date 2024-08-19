import os

def generate_show_template(table, dbname):
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
                <table class="table table-striped">
                    <tbody>
                        {''.join([f'<tr><th>{col.capitalize()}</th><td>{{{{ $data->{col} }}}}</td></tr>' if not table.columns[col].foreign_keys else f'<tr><th>{col.capitalize()}</th><td>{{{{ $data->{col}->related_model_name }}}}</td></tr>' for col in table.columns.keys() if col not in ['id', 'created_at', 'updated_at']])}
                    </tbody>
                </table>
            </div>
            <div class="card-footer text-end">
                <a href="{{{{ route('{table.name}.index') }}}}" class="btn btn-secondary"><i class="bi bi-chevront-left"></i>Back</a>
                <a href="{{{{ route('{table.name}.edit', $data->id) }}}}" class="btn btn-warning">Edit</a>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{{{ $data->id }}}}">Delete</button>
            </div>
        </div>
        <div class="modal fade" id="deleteModal{{{{ $data->id }}}}" tabindex="-1" aria-labelledby="deleteModalLabel{{{{ $data->id }}}}" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteModalLabel{{{{ $data->id }}}}>Confirm Delete</h5>
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

    output_dir = os.path.join(os.path.dirname(__file__), '../output/'+dbname+'/resources/views/{table.name}'.format(table=table))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, 'show.blade.php'), "w") as file:
        file.write(template)